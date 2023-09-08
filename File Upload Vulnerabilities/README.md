# File Upload Vulnerabilities

## Summary

* [General Recon for File Upload Vulnerabilities](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/file-upload
* https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
* https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files

<br>

## Recon

* Identify any file upload functionalities on the application either direct or indirect accessible functions.  Then use the test cases here from the labs to identify vulnerability on the file upload process.

<br>

## Cheat Sheet

* If you find a file upload functionality on an application, try out the following techniques as described in the labs.  However, much more can be done depending on the which part of the file the application is not validating, how the application is using the file (e.g., interpreters like XML parsers), and where the file is being stored.

* In some cases, uploading the file is enough to cause damage.  However, in other cases the file will need to be “executed” somehow, such as requesting the file using an HTTP request.

* If the uploaded file is available within the Webroot, try submitting HTML/JavaScript file, then view the file.  This may introduce an easy XSS vulnerability.

<br>

### No Protections - Example

* The application has no protections against malicious file uploads and the server is configured to execute these files as code.

* Upload a file with the following properties:

    * File extension:  .php

    * Content-Type header:  application/x-httpd-php

    * File Content:  \<?php echo file_get_contents('/path/to/target/file'); ?\>
 
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

* Now view the uploaded file within the Webroot and we should see the contents of the file specified.  The “viewing” of the file here caused its execution.

<br><br><br>
![File Image](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/File%20Upload%20Vulnerabilities/Images/FileUploads-1.png)

<br><br>

![File Image2](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/File%20Upload%20Vulnerabilities/Images/FileUploads-2.png)

<br><br>

### Content-Type Header Restriction Bypass

* The application is only allowing mime types for - image/jpeg.  However, it is not blocking malicious file types from being uploaded such as .php.  Simply keep the Content-Type header, within the subpart of the request body, with the allowed mime type and upload the .php file to bypass this restriction.


<br>

### Chain multiple vulnerabilities together – directory traversal and malicious file upload

* The application allows the user to upload malicious files, however, the directory that the file is uploaded to, is not configured with execution permissions.  

* If the application is not performing input validation on the value used to determine the location of the uploaded file, we may be able to introduce a directory traversal attack to get the uploaded file into a different directory that has execution permissions.

    * Example Payload

```bash    
../../../file.php
```

<br>

### Overwriting a Configuration File / Extension Rejectlist Bypass

* Servers usually won’t execute files unless they have been configured to do so.  Many servers allow directory level configuration files to be used, which will override global configurations.

* In Apache server, we can upload the following configurations into a file called  -  .htaccess

```bash
AddType application/x-httpd-php .php5
```

* Which will map the file extension .php5 to the executable MIME type application/x-httpd-php.  Now we can upload a file with the .php5 file extension and the server will execute the code as php.  

* This will bypass any reject list validations against files such as - .php.

**The file extension can be any arbitrary value, as long as it is not blocked by the application.**

* Another example for Microsoft IIS servers can be found here - https://portswigger.net/web-security/file-upload#overriding-the-server-configuration

<br>

### Bypass File Extension Allow List


* The null byte injection (%00) may bypass the file extension restriction, as this can alter the intended logic of the application.

    * Example:  If the application is only allowing files that have the extension .png.  We can supply the following filename:

```bash
malicious.php%00.png
```

* More bypass methods: https://portswigger.net/web-security/file-upload#obfuscating-file-extensions


<br>

### Bypass JPEG Signature Validation

* Here the application may be checking that the file's contents begin with a certain byte structure (Magic Numbers).

* Simply inject the malicious code after the beginning bytes of the file to bypass this validation.

* Tools can be used to inject this malicious code in the metadata to avoid "breaking" the file/image.

* More Resources: 

    * https://book.hacktricks.xyz/pentesting-web/file-upload
    * https://onestepcode.com/injecting-php-code-to-jpg/


<br><br>
![File Image3](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/File%20Upload%20Vulnerabilities/Images/FileUploads-3.png)

<br><br>
![File Image4](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/File%20Upload%20Vulnerabilities/Images/FileUploads-4.png)


<br>

### Other methods of exploiting file upload vulnerabilities

* Stored XSS by uploading HTML page with JavaScript

* Exploiting vulnerabilities specific to the parsing or processing of different file formats to cause XXE injection (.doc , .xls)
  
* Using the PUT method to upload files, use the OPTIONS request method to determine what methods are accepted.

   * Link - https://portswigger.net/web-security/file-upload#exploiting-file-upload-vulnerabilities-without-remote-code-execution
 
<br><br>

### Pending to complete labs that are missing from cheat sheet:

* LAB EXPERT Web shell upload via race condition
