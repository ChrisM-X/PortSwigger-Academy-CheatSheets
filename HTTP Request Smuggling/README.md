# HTTP Request Smuggling

## Summary 

* [Recon for HTTP Request Smugling](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* [More Practitioner Labs](#note-the-rest-of-the-payloads-for-the-other-practitioner-labs-can-be-found-in-the-sections-of-the-document)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon

* Links:

    * https://portswigger.net/web-security/request-smuggling#how-do-http-request-smuggling-vulnerabilities-arise

    * https://portswigger.net/web-security/request-smuggling/finding

<br><br>

## Tools and Burp Extensions Used:

* HTTP Request Smuggler - https://github.com/portswigger/http-request-smuggler#practice

<br><br><br>

## Cheat Sheet

<br><br>

**Important Notes:** 

* These techniques are only possible using HTTP/1 requests. Browsers and other clients, including Burp, use HTTP/2 by default to communicate with servers that explicitly advertise support for it via ALPN as part of the TLS handshake. As a result, when testing sites with HTTP/2 support, you need to manually switch protocols in Burp Repeater. You can do this from the Request attributes section of the Inspector panel. 

*  When working with "TE.CL" payloads - To send this request is Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

*  When submitting request smuggling payloads it is often required to include an arbitrary body parameter ( x= ) at the end, so that the next normal submitted request does not "break" the smuggled request, as it will be appended to the parameter (For example, this would avoid duplicate headers issues).

  * All of the headers in the smuggled request are important such as the Host, Content-Type and Content-Length.  The values for these headers need to be considered when capturing other user's requests, etc.  

<br><br>

### __Basic CL.TE payload__

* Include both Content-Length (CL) and Transfer-Encoding (TE) headers.

* Here the front-end server is processing the request length using the CL header, which will process the entire body.

* The back-end server receives the same request but uses the TE header to process the request’s length.  Since the terminating byte 0 is provided in the beginning of the body, the rest of the data will be left unprocessed and will remain in the connection queue.  The next request that is submitted will be appended to this left over request data.  So, the back-end server essentially see’s 2 requests in the payload submitted.


![HRS-1](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture1.png)

![HRS-2](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture2.png)

![HRS-3](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture15.png)

<br><br>

### __Basic TE.CL payload__

* Include both Content-Length (CL) and Transfer-Encoding (TE) headers.

* The front-end server is using the TE header to determine the length of the request.  The HTTP request smuggler extension can be used here to automatically update the bytes required.  It will add in the start and end bytes (9d and 0) in this case.

* When the back-end server receives this request, it will use the CL header to determine the length of the request.  Since the value is 4, it will leave the rest of the body unprocessed and will remain in the connection queue.  The next request that is submitted will be appended to the x=1 parameter.  The server here essentially see’s 2 request.

  * Note: To send this request is Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked. 

![HRS-3](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture3.png)

![HRS-4](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture4.png)


<br><br>

### __Basic TE.TE payload (obfuscating TE header)__

* https://portswigger.net/web-security/request-smuggling#te-te-behavior-obfuscating-the-te-header

* In this scenario, both the front-end and back-end servers support the TE header.  We need to submit a payload that will obfuscate the TE header and identify if either of the servers reject the TE header and use the CL header for processing.

* CL.TE payload – the application times-out when using this method, which means the front-end application is using the TE header.

![HRS-5](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture5.png)

* TE.CL payload – the application does not time out and the back-end server processes the request using the CL header.  This is the direction for exploitation since the obfuscated TE header prevented the back-end server from using it.

![HRS-6](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture6.png)

![HRS-1](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture7.png)


<br><br>

### __Confirming CL.TE vulnerability via differential responses__

* A request to GET / endpoint normally returns the home page of the application.  

* A request to a random endpoint like GET /404, will return a 404 Not Found response.

* This behavior will be used to identify if our request smuggling payload worked.

* The payload consists of a smuggled request that will be sent to the /404 endpoint, which would return a 404 error.

* The follow up request will be submitted to the GET / endpoint, however, instead of returning the home page, a 404 error is returned.  Which proves the smuggled payload worked. 


![HRS-8](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture8.png)

![HRS-9](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture9.png)


<br><br>

### __Confirming TE.CL vulnerability via differential responses__

* A request to GET / endpoint normally returns the home page of the application.  

* A request to a random endpoint like GET /404 or POST /404, will return a 404 Not Found response.

* This behavior will be used to identify if our request smuggling payload worked.

* The payload consists of a smuggled request that will be sent to the /404 endpoint, which would return a 404 error.  The CL header contains the value of 4, which covers the data up to the beginning of line 20.

* The follow up request receives a 404 error, even though the request is made to the home page / of the application.  This proves that the payload worked as expected.

![HRS-10](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture10.png)

![HRS-11](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture11.png)


<br><br>

### __Using TE.CL payload to bypass front-end controls__

* The /admin endpoint is only available to local users.

* A TE.CL payload was crafted where the smuggled request will be to the /admin endpoint, the Host header contains the value of localhost.

* Submitting a follow up request will return the normal response to the /admin request.  We can send another request to delete the user, Carlos. 

![HRS-12](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture12.png)

<br><br>

### __Using CL.TE payload to capture other user’s requests__

* We need to identify if there is a request with parameters whose values are being reflected or stored in a response. 

* In this scenario, the application has a blog where users can leave comments that can be viewed in the application.

* The “comment” parameter was intentionally injected last in the payload so the follow request will appear in the application’s UI.  The CL header in the smuggled request payload matters and needs to be adjusted in order to capture all the data in the follow up request.  A lot of trial/error can happen here.

* Since the victim user’s request contains the session cookie header, this will be captured in the smuggled request and can be used to access the application as that user.


![HRS-13](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture13.png)

![HRS-14](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/HTTP%20Request%20Smuggling/Images/Picture14.png)


<br><br>

### Note The rest of the payloads for the other practitioner labs can be found in the sections of the document

   * The following can be found in the attached document:

      * Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

      * Exploiting HTTP request smuggling to reveal front-end request rewriting

      * Exploiting HTTP request smuggling to deliver reflected XSS

      * Response queue poisoning via H2.TE request smuggling

      * H2.CL request smuggling

      * HTTP/2 request smuggling via CRLF injection

      * HTTP/2 request splitting via CRLF injection

      * CL.0 request smuggling
    
      * Exploiting HTTP request smuggling to perform web cache poisoning
    
      * Exploiting HTTP request smuggling to perform web cache deception

<br><br><br>

### Pending to complete labs that are missing from cheat sheet.

* LAB EXPERT Bypassing access controls via HTTP/2 request tunnelling Not solved 

* LAB EXPERT Web cache poisoning via HTTP/2 request tunnelling Not solved 

* LAB EXPERT Client-side desync Not solved 

* LAB EXPERT Browser cache poisoning via client-side desync Not solved 

* LAB EXPERT Server-side pause-based request smuggling Not solved 
