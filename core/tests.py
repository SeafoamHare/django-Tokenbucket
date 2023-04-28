from django.test import TestCase, RequestFactory
from django.core.cache import cache
from .middleware import OptimisticBucket, optimistic
from django.test import Client
from django.core.cache import caches
import time
from multiprocessing import Process
from django.http import HttpRequest

# Create your tests here.
class TokenBucketTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.rate = 1
        self.capacity = 10
        self.c = Client()

    #Test if Token Bucket can issue tokens correctly when the capacity is sufficient in middleware.
    def test_not_limit_middleware(self):
        caches['default'].clear() # reset caches

        #GET
        resp = self.c.get('/test/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(float(resp['X-RateLimit-Limit']), 1)
        self.assertEqual(float(resp['X-RateLimit-Remaining']), 0)
        self.assertEqual(float(resp['X-RateLimit-Reset']), 1)
        #POST
        resp = self.c.post('/test/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(float(resp['X-RateLimit-Limit']), 1)
        self.assertEqual(float(resp['X-RateLimit-Remaining']), 0)
        self.assertEqual(float(resp['X-RateLimit-Reset']), 1)
    
    #Test if Token Bucket can correctly prevent token issuance when the capacity is insufficient in middleware.
    def test_limit_middleware(self):
        caches['default'].clear() # reset caches

        #GET
        self.c.get('/test/')
        resp = self.c.get('/test/')
        self.assertEqual(resp.status_code, 429)
        self.assertTrue(float(resp['Retry-At']) < 1)

        #POST
        self.c.post('/test/')
        resp = self.c.post('/test/')
        self.assertEqual(resp.status_code, 429)
        self.assertTrue(float(resp['Retry-At']) < 1)

    #Test if Token Bucket can correctly reset the token counter and last refresh time when the capacity limit is reached.
    def test_reset_time(self):
        caches['default'].clear() # reset caches

        #GET
        resp = self.c.get('/test/')
        time.sleep(1)
        resp = self.c.get('/test/')
        self.assertEqual(resp.status_code, 200)

        #POST
        resp = self.c.post('/test/')
        time.sleep(1)
        resp = self.c.post('/test/')
        self.assertEqual(resp.status_code, 200)

    #Test if Token Bucket can correctly handle token issuance on multiple IP addresses.
    def test_diff_ip(self):
        
        caches['default'].clear() # reset caches
        resp1 = self.c.get('/test/',REMOTE_ADDR='192.168.0.1')
        resp2 = self.c.get('/test/',REMOTE_ADDR='127.0.0.1')
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

        #POST
        caches['default'].clear() # reset caches
        resp1 = self.c.post('/test/',REMOTE_ADDR='192.168.0.1')
        resp2 = self.c.post('/test/',REMOTE_ADDR='127.0.0.1')
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    #Test if Token Bucket can correctly limit the request rate for same IP address in the case of multiple concurrent requests.
    def test_optimistic_concurr(self):
        caches['default'].clear() # reset caches
        cache_key = "%s:%s:%s" % ('OptimisticBucket', '192.168.0.1', 'GET')
        time1 = time.time()
        time2 = time.time()
        caches['default'].set(cache_key, {'value':1,'last_refill_time':time1},1)
        caches['default'].set(cache_key, {'value':2,'last_refill_time':time2},1)
        if optimistic(caches['default'],cache_key,time1):
            caches['default'].set(cache_key, {'value':3,'last_refill_time':time1},1)
        resp = caches['default'].get(cache_key)
        self.assertEqual(resp['value'], 2)
        self.assertEqual(resp['last_refill_time'], time2)
