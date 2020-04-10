


# Information:
* Topic: CURL
* Date: 2020.03.30
* Summary: A way to execute CURL request through ProxyRotator's proxy. 

# Keywords:
* [CURL, ProxyRotator, Proxy, Requests, Scrape, Webscraping]

# Content:

QUESTION: Is there a way to execute these requests in a less stupid way?  Maybe with CURL?
Or with RUST?
* [Example] (https://ec.haxx.se/usingcurl/usingcurl-proxies)
* http://falcon.proxyrotator.com:51337/?apiKey=PK6CjxFpmJfgosLVaRdDBYQS435A7ZNy
* curl -x 192.168.0.1:8080 http:/example.com/
``` EXAMPLE
curl -U c02ef43b1cf007a6784489d8a5427b70:77be1a39d6cd458ec3438fe4026605cf -x 199.189.86.111:9500 -A "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0" "https://seekingalpha.com/amp/news/3556525-visa-announces-meaningful-deterioration-in-payment-volumes-in-second-half-of-march" --proxy-ntlm 

```
