# Information Disclosure

## Summary

* [General Recon](#general-recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/information-disclosure

* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/README

<br>

## General Recon

* Map out the application with the following steps for example:

    * Walk through the entire functionality of the application as a regular user would.  Make a note of every request, parameters/input fields, cookies and interesting headers that are being used.  ( Burp Suite’s site map can be helpful here to keep track of all the endpoints/data that were found and/or a spreadsheet can help ).

    * Check the source code of the application and identify any JavaScript files, comments or any other resources that were not already discovered to see if they leak any internal system/sensitive information.

    * Use enumeration tools to discover more content such as hidden directories, parameters, or files.  These resources may disclose some sensitive functionality. Some tools to use are Burp Pro’s (Discover Content), gobuster, ffuf , etc.

<br>

## What is information disclosure?

* Information disclosure, also known as information leakage, is when a website unintentionally reveals sensitive information to its users. Depending on the context, websites may leak all kinds of information to a potential attacker, including: 
    
    * Data about other users, such as usernames or financial information 

    * Sensitive commercial or business data 

    * Technical details about the website and its infrastructure 

* The dangers of leaking sensitive user or business data are obvious but disclosing technical information can sometimes be just as serious. Although some of this information will be of limited use, it can potentially be a starting point for exposing an additional attack surface, which may contain other interesting vulnerabilities. The knowledge that you can gather could even provide the missing piece of the puzzle when trying to construct complex, high-severity attacks. 

* Occasionally, sensitive information might be carelessly leaked to users who are simply browsing the website in a normal fashion. More commonly, however, an attacker needs to elicit the information disclosure by interacting with the website in unexpected or malicious ways. They will then carefully study the website's responses to try and identify interesting behavior. 

<br>

## Cheat Sheet

<br>

More details can be found here - https://portswigger.net/web-security/information-disclosure/exploiting

<br>


* Sensitive information can be found even without explicitly looking for it.  Sometimes when probing for other vulnerabilities there is a specific error message, notable difference in the response or a subtly time delay in the application’s response.  This information is important to note down and further engineer informative responses.

<br>

* Check out the common files for web crawlers:  /robots.txt or /sitemap.xml

<br>

* Directly Listing - Web servers can be configured to automatically list the contents of directories that do not have an index page present.

   * For example:  If you see a path such as this ->  /resources/static/files/23.jpg

   * Look under all the folders to see if there is a listing of other existing resources:

      * /resources
      * /resources/static
      * /resources/static/files

<br>

* Submit unexpected characters into parameters, cookies, or headers, and analyze the affect it has on the application.  Maybe this discloses a stack trace or an overly verbose error message.


![Stack Trace](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/Information%20Disclosure/Images/StackTrace1.png)

<br><br>

* Burp Pro has a “Search” functionality under the “Engagement Tools” that can help to identify any sensitive information in the responses of a specific target domain.  We can search for some keywords such as password, secret, key, etc.

<br>

* Look for keywords that are often contained in error messages: error, invalid, stack, not found, SQL, access, etc.  Sometimes the error messages will not be rendered to the screen, look at the raw responses.

<br>

* When a server handles files with a particular extension, such as .php, it will typically execute the code, rather than simply sending it to the client as text. However, in some situations, you can trick a website into returning the contents of the file instead.  Appending a tilde (~) to the filename or adding a different file extension.

* Example:  test.php~

<br>

* Use the HTTP method TRACE when submitting requests, as this can reveal sensitive debugging information that can be used to exploit the application.


![Trace](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/Information%20Disclosure/Images/ID-1.png)

<br><br><br>

* Information disclosure in version control history:

    * There is a /.git endpoint that can be found by using the Discover Content feature in the Engagement Tools

    * At this point we can download the entire directory using { wget –r https://.../path/to/file } and follow the steps on the screenshot to obtain the admin password.


![Version Control](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/Information%20Disclosure/Images/ID-2.png)

<br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet.
