# JWT Attacks

## Summary

* [Recon for JWT Attacks](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the complete labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon

* JWT Burp Extension:  https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts


<br><br>

## Cheat Sheet

<br><br>

### __JWT authentication bypass via unverified signature.__

* The application is not properly verifying the signature of the JWT Token.  Simply manipulate the JWT's payload and use it to attack the application.

* Use the JWT Editor Burp extension to easily manipulate the JWT tokens.  Changing the value of the "sub" key in the payload section, will gain us access to the admin account.

![jwt1](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/JWT%20Attacks/Images/Picture1.png)

<br><br>

### __JWT authentication bypass via flawed signature verification.__

* The application is trusting the algorithm sent in the header of the JWT Token.  Change the "alg" key in the header to the value of "none".  To bypass dis-allow list validations, it may be required to obfuscate the value "none" -> "NonE", etc. 

* When using the JWT Token in the attack, omit the entire Signature of the token but leave the preceding dot "." at the end 

![jwt2](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/JWT%20Attacks/Images/Picture2.png)

<br><br>

### __JWT authentication bypass via weak signing key.__

* The application is using a weak secret to both sign and verify tokens.  The secret can be brute forced using a tool like "hashcat".  Once the secret is cracked, we can use it to create our own key (Symmertric Key) using Burp's JWT Editor Keys and use it to sign our tampered tokens to attack the application.

* How to create Symmetric key with the known secret?

    * Go to the "JWT Editor Keys" tab and select the option "New Symmetric Key"
    
    * Base64 encode the known secret and include it within the "k" key's value of the generated symmetric key^.
    

* Important:  For the lab, this exploit works when the algorithm the application is using to sign the JWT token is Symmetric like - "HS256"

* The following wordlist can be used for brute forcing - https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list

* See lab/document for more details.

<br><br>

### __JWT authentication bypass via jwk header injection.__

* The server supports the JSON Web Key (JWK) header, which provides an embedded JSON object representing the key.  The server fails to ensure the key is coming from a trusted source.  The original JWT Token used in the application is using the RS256 algorithm.

* Using Burp's JWT Editor Keys, we can create a new RSA key to use in our attack.  

* Manipulate the JWT payload, then sign the tampered token using that same RSA key we created, ensure to also select the option that updates the "alg", "typ" and "kid" parameters automatically.

* Burp has the option to use the "Embedded JWK" attack method, which will automatically update the header with the JWK key and we can choose to use the RSA key we created. Now that the JWT Token is signed with our own private RSA Key, when the server uses the public key in the JWK header we injected, the verification will succeed and the exploit will work.

* Important:  For the lab, this exploit works when the algorithm the application is using to sign the JWT token is Asymmetric like - "RS256"

* See lab document for more details.

<br><br>

### __JWT authentication bypass via jku header injection.__

* The server supports the JSON Web Key Set URL (JKU) header, which provides a URL from which servers can fetch a set of keys containing the correct key.  The server fails to check that the provided URL is coming from a trusted domain.  The original JWT Token used in the application is using the RS256 algorithm.  Using Burp's JWT Editor Keys, we can create a new RSA key to use in our attack.  

* We can place the new created RSA key within Burp's Exploit Server to host the key.

    * Go to the "JWT Editor Keys" tab and right click on the created RSA key and select the option "Copy Public Key as JWK".
    
    * Inject it within a JSON "keys" array in the Exploit server, for example: 

```json
{
    "keys": [
      {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "b1d95cf1c2a9",
        "n": "sfVWMUmmiXR_7K1SRWoqQ"
      }
    ]
}
```

* In Burp Repeater, change the "kid" value of the JWT token we are manipulating so that it matches the same value of the key we generated, then inject the "jku" header that points to the Exploit Server's URL that is hosting the RSA key^.

* Finally, when manipulating the JWT Token, sign it with our generated RSA key.  Now that the JWT Token is signed with our own private RSA Key, when the server reaches out to the URL within the JKU header it will grab the public key with the same "kid" value and use it to verify the token which will now succeed.

* Important:  For the lab, this exploit works when the algorithm the application is using to sign the JWT token is Asymmetric like - "RS256"

* See lab document for more details.

<br><br>

### __JWT authentication bypass via kid header path traversal.__

* The "kid" header, which is a String that indicates the key that was used to digitally sign the JWT, is vulnerable to a path traversal attack.  The server is using a Symmetric Key (algorithm "HS256") to sign the token, which means a single key is used to both sign and verify the token.  

* If we can point the "kid" header to the /dev/null file, this will return an empty String.  Example:

    * "kid": "../../../../../../../dev/null" 

* Then use Burp JWT Editor Keys to create a new Symmetric Key and change the "k" value to "AA==", which is a base64 encoded null byte.  Sign the tampered JWT Token with this new Symmetric Key and use a path traversal payload in the "kid" header to attack the application. Essentially the same "key" is being used here to both sign and verify the token so the exploit will work.

* Important:  For the lab, this exploit works when the algorithm the application is using to sign the JWT token is Symmetric like - "HS256"

<br><br>

### __Algorithm Confusion - Public Key Exposed.__

* The server is using the "alg" header to determine which algorithm to use when verifying the token, however only the RS256 or HS256 is allowed.  Originally the JWT Token is using the RS256 token (2 different keys) to sign and verify the token.  The exact public key used to verify the token is being exposed within the application's webroot.  

* We can use this same exposed key to generate a new Symmetric Key using Burp's JWT Editor Keys tab.  Use this generated Symmetric Key to sign the tampered JWT Token, while also changing the "alg" to the value of "HS256".  Since the algorithm "HS256" uses the same key to both verify and sign the token this exploit will work, as the server will fetch the same key, we used to sign the token, to verify the signature.

* See the steps in the section/document for more details.

<br><br>

### __Algorithm Confusion - Public Key Not Exposed.__

* See the steps in the section/document for more details.

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet or attached document.
