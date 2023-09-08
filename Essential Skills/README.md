# Essential Skills

* Links:

    * Obfuscating attacks using encodings:  https://portswigger.net/web-security/essential-skills/obfuscating-attacks-using-encodings

    * Using Burp Scanner during manual testing:  https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing

<br><br>

## Summary

* [Obfuscating attacks using encodings](#obfuscating-attacks-using-encodings)

* Using Burp Scanner during manual testing - https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing

<br><br>
 
## Obfuscating attacks using encodings

<br>

* CyberChef can be used to help obfuscate and encode characters as mentioned in this section:

   * https://gchq.github.io/CyberChef/

<br><br>

### Context-specific decoding

* Both clients and servers use a variety of different encodings to pass data between systems.  The exact sequences of decoding steps depends on the context in which the data appears.

    * Example:  A query parameter is typically URL decoded server-side.

    * Example:  The text xontent of an HTML element may be HTML decoded client-side.

* Understanding the context of the targeted input fields can help to idenitfy how the data is being decoded.  With this information it can help us construct payloads that when decoded will represent the same malicious data.

<br><br>

### Decoding discrepancies

* Injection attacks usually involve injecting payloads that have a recognizable patterns, like \<script\> for XSS or SELECT for SQLi.  So websites will often implement defenses to block these requests containing these inputs.

* These kinds of input filters need to decode the input in order to check if the data is safe or not.

* If these filters do not use the same decoding procedures that the back-end server or browser uses then this can enable an attacker to sneak harmful payloads past the filter by applying different encodings that will automatically be removed later. 

    * Example:  Website URL decodes the data once to identify if the input is safe.  However, the back-end server performs double URL decoding.

<br><br>


### Obfuscation via URL encoding

* Any URL-based input is automatically URL decoded server-side before it is assigned to the relevant variables. This means that, as far as most servers are concerned, sequences like %22, %3C, and %3E in a query parameter are synonymous with ", <, and > characters respectively.

* WAFs sometimes can fail to properly URL decode the input when checking it. We may be able to smuggle payload by encoding any characters or words that are blacklisted.

    * Example:  The application is blocking the SELECT statement to prevent SQL injections.

    * Payload:  URL encode SELECT -> %53%45%4C%45%43%54

<br><br>


### Obfuscation via double URL encoding

* Servers may perform 2 rounds of URL decoding, where as the WAF performs only 1 round of URL decoding.  In this scenario we can encode or payload twice to bypass the filters and inject the data to the application.

    * Example: The application is blocking the <> tags to prevent XSS and the WAF URL decodes the injected input only once.

    * Payloads to bypass filter:

        * %253Cimg%2520src%253Dx%2520onerror%253Dalert(1)%253E

        * %25%33%63%25%36%39%25%36%64%25%36%37%25%32%30%25%37%33%25%37%32%25%36%33%25%33%64%25%37%38%25%32%30%25%36%66%25%36%65%25%36%35%25%37%32%25%37%32%25%36%66%25%37%32%25%33%64%25%36%31%25%36%63%25%36%35%25%37%32%25%37%34%25%32%38%25%33%31%25%32%39%25%33%65

<br><br>


### Obfuscation via HTML encoding

* In specific locations within the HTML, such as the content of an element or value of an attribute, browsers will automatically decode those values when they parese the document.

* Alternatively, the reference may be provided using the character's decimal or hex code point, in this case, &#58; and &#x3a; respectively. 

* We can take advantage of this behavior to obfuscate payloads for client-side attacks like XSS, which hides them from server-side checks.

    * Example: The server-side application is checking for the alert() payload and rejecting requests with that input.

    * Payload to bypass filters:  

```javascript
<img src=x onerror="&#x61;lert(1)">
```

* When the browser renders the page, it will decode and execute the injected payload. 

<br><br>


#### Leading zeros

* If your payload still gets blocked after HTML encoding it, you may find that you can evade the filter just by prefixing the code points with a few zeros: 

```javascript
<a href="javascript&#00000000000058;alert(1)">Click me</a>
```

<br><br>


### Obfuscation via XML encoding

* XML is closely related to HTML and also supports character encoding using the same numeric escape sequences. This enables you to include special characters in the text content of elements without breaking the syntax, which can come in handy when testing for XSS via XML-based input, for example. 

* This behavior can be useful to obfuscate payloads which will be decoded server-side instead of client-side by a browser.

    * Example:

```xml
<stockCheck>
    <productId>
        123
    </productId>
    <storeId>
        999 &#x53;ELECT * FROM information_schema.tables
    </storeId>
</stockCheck>
```

<br><br>


### Obfuscation via unicode escaping

* Unicode escape sequences consist of the prefix \u followed by the four-digit hex code for the character. For example, \u003a represents a colon. ES6 also supports a new form of unicode escape using curly braces: \u{3a}. 

* For example, let's say you're trying to exploit DOM XSS where your input is passed to the eval() sink as a string. If your initial attempts are blocked, try escaping one of the characters as follows: 

```javascript
eval("\u0061lert(1)")
```

* As this will remain encoded server-side, it may go undetected until the browser decodes it again. 

* It's also worth noting that the ES6-style unicode escapes also allow optional leading zeros, so some WAFs may be easily fooled using the same technique we used for HTML encodings. For example: 

```javascript
<a href="javascript\u{0000000003a}alert(1)">Click me</a>
```

<br><br>


### Obfuscation via hex escaping

```javascript
val("\x61lert")
```

<br><br>


### Obfuscation via octal escaping

```javascript
eval("\141lert(1)")
```

<br><br>


### Obfuscation via multiple encodings

* It is important to note that you can combine encodings to hide your payloads behind multiple layers of obfuscation. Look at the javascript: URL in the following example:

```javascript
<a href="javascript:&bsol;u0061lert(1)">Click me</a>
```

* Browsers will first HTML decode &bsol;, resulting in a backslash. This has the effect of turning the otherwise arbitrary u0061 characters into the unicode escape \u0061: 

```javascript
<a href="javascript:\u0061lert(1)">Click me</a>
```

* This is then decoded further to form a functioning XSS payload: 

```javascript
<a href="javascript:alert(1)">Click me</a>
```

<br><br>


### Obfuscation via the SQL CHAR() function

* For example, even if SELECT is blacklisted, the following injection initially appears harmless: 

```
CHAR(83)+CHAR(69)+CHAR(76)+CHAR(69)+CHAR(67)+CHAR(84)
```

* However, when this is processed as SQL by the application, it will dynamically construct the SELECT keyword and execute the injected query. 
