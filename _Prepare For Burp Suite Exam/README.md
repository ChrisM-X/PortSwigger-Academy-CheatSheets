### Below is a table to help identify which vulnerabilities to use at each stage in the Burp Suite Exam.

* Stages:

  * Stage 1:  Access any user account.
 
  * Stage 2:  Use your user account to access the admin interface at /admin, perhaps by elevating your privileges or compromising the administrator account.
 
  * Stage 3:  Use the admin interface to read the contents of /home/carlos/secret from the server's filesystem, and submit it using "submit solution".

* Links:

  *  https://portswigger.net/web-security/certification/exam-hints-and-guidance
 
  *  https://portswigger.net/web-security/certification/how-it-works#what-the-exam-involves

* Interactive Exploit - means that the category can be used to target active user sessions.  This is important to keep in mind since the exam details mention that "Each application has up to one active user, who will be logged in either as a user or an administrator.".


<br><br>

| Categories                           | Stage 1 | Stage 2 | Stage 3 | Interactive Exploit? |
|--------------------------------------|---------|---------|---------|----------------------|
| SQL Injection                        |    X    |    X    |         | 
| Authentication                       |    X    |    X    |         |          X
| Directory Traversal                  |         |         |    X    |
| Command Injection                    |         |         |    X    |
| Business Logic Vulnerabilities       |         |    X    |         |
| Information Disclosure               |         |         |         |
| Access Control                       |    X    |    X    |         |
| File Upload Vulnerabilities          |         |         |    X    |   sometimes w/ xss
| Server-Side Request Forgery (SSRF)   |         |    X    |         |
| XXE Injection                        |         |         |    X    |
| Cross-site Scripting (XSS)           |    X    |    X    |         |          X
| Cross-site Request Forgery (CSRF)    |         |    X    |         |          X
| Cross-origin Resource Sharing (CORS) |    X    |    X    |         |          X
| Clickjacking                         |    X    |    X    |         |          X
| DOM-based Vulnerabilities            |    X    |    X    |         |          X
| WebSockets                           |    X    |    X    |         |          X
| Insecure Deserialization             |         |    X    |    X    |
| Server-side Template Injection       |         |         |    X    |
| Web Cache Poisoning                  |    X    |    X    |         |          X
| HTTP Host Header Attacks             |    X    |    X    |         |          X
| HTTP Request Smuggling               |    X    |    X    |         |          X          
| OAuth Authentication                 |    X    |    X    |         |          X
| JWT Attacks                          |    X    |    X    |         |
| Prototype Pollution                  |    X    |    X    |    X    |          X
| Essential Skills                     |         |         |         |
