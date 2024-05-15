
# Django-OptimisticBucket
(todolist)This is a Django-based project that implements the Token Bucket algorithm and uses Optimistic Locking to handle concurrency issues.  
#### Rate limiting

Rate limiting is used to protect resources from being over-using or abused by users/bots/applications. It is commonly implemented by social media platforms such as Facebook or Instagram.

Header fields and status codes from the response of a rate-limited server could tell you more information about how it is going to limit your requests. 

| header field | explaination |
|-------------|--------------|
|  X-RateLimit-Limit           | The number of requests allowed during a fixed time window.             |
|  X-Rate-Limit-Remaining           |    The number of remaining requests allowed in the current time window.          |
|  X-Rate-Limit-Reset           |  at the time when the rate-limit requests are reset.  UTC epoch time (in seconds).          |
| Retry-At |  the second before the window resets and requests will be accepted. UTC epoch time (in seconds). |


For example, the following messages would tell the client that you sent too many requests to the server side, and now you are temporarily blocked for an hour, you can try later by then.

```
HTTP/1.1 429 Too Many Requests
Content-Type: text/html
Retry-After: 3600
```


## Flow chart  
![image](/image/flow_chat.png "This is a sample image.")  
