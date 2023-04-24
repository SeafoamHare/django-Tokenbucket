import time
import re
from django.core.cache import caches
from django.http import HttpResponse
import socket
from django.core.exceptions import ImproperlyConfigured
_PERIODS = {
        's': 1,
        'm': 60,
        'h': 60 * 60,
        'd': 24 * 60 * 60,
        }
rate_re = re.compile(r'([\d]+)/([\d]*)([smhd])?')

def _split_rate(rate):
        if isinstance(rate, tuple):
            return rate
        count, multi, period = rate_re.match(rate).groups()
        count = int(count)
        if not period:
            period = 's'
        seconds = _PERIODS[period.lower()]
        if multi:
            seconds = seconds * int(multi)
        return count, seconds

def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    return ip_addr

def optimistic(cache,cache_key,last_refill_time):
    Optimistic_token = cache.get(cache_key)
    if Optimistic_token is not None:
        if Optimistic_token['last_refill_time'] == last_refill_time:
            return True
    return False

class OptimisticBucket:
    
    def __init__(self, rate,):
        self.cache = caches['default']
        self.capacity, self.fill_rate = _split_rate(rate)
        self.tokens = self.capacity
        self.last_update = time.time()
        self.key_prefix = 'OptimisticBucket'
    

    def handle(self,request,tokens):
        now = time.time()
        new_token = 0.0
        ip_address = get_client_ip_address(request)
        # 使用 make_key 函數生成 Cache key，加入 IP 地址和時間戳
        cache_key = "%s:%s:%s" % (self.key_prefix, ip_address, request.method)
        try:
            adds = self.cache.add(cache_key, {'value':self.tokens,'last_refill_time':now}, self.fill_rate)
        except socket.gaierror:  # for redis
            adds = False
        
        cache_token = self.cache.get(cache_key,{'value':self.tokens,'last_refill_time':now})
        if not adds:
            time_passed = now - cache_token['last_refill_time']
            if time_passed >= 0:
                new_token = time_passed / self.fill_rate
            else:
                raise ImproperlyConfigured('time_passed must >= 0')
        new_value = min(self.capacity, cache_token['value'] + new_token)
        

        if tokens <= new_value:
            new_value = new_value - tokens
            if optimistic(self.cache,cache_key,cache_token['last_refill_time']):
                self.cache.set(cache_key,{'value':new_value,'last_refill_time':now}, self.fill_rate)
            return True
        else:
            return False

    
class OptimisticBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response        
        self.token_bucket = OptimisticBucket(rate='1/s')

    def __call__(self, request):
        if not self.token_bucket.handle(request,1):
            return HttpResponse('Rate limit exceeded', status=429)
        response = self.get_response(request)
        return response
