# Business Logic Vulnerabilities

## Summary

* [General Recon for Business Logic Vulnerabilities](#recon)
  
* [Portswigger Labs Cheat Sheet / Payloads](#cheat-sheet)

<br>

## Resources

* https://portswigger.net/web-security/logic-flaws
  
* https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/README
  
* https://owasp.org/www-community/vulnerabilities/Business_logic_vulnerability

<br>

## Recon

* Logic flaw vulnerabilities are different than other vulnerabilities such as SQL Injection, there isn’t a common signature to identify Logic Flaws, as there is for SQLi. 

* It requires walking through the entire application and all it’s functionalities and determine if there is a defect in the logic that was implemented in the application.

* Generally, a programmer may have reasoned, “If A happens, then B must be the case, so I will do C.” But there wasn’t any consideration for, “But what if X occurs?”.

* There are 12 different Logic Flaw examples on the Web Hacker’s Handbook 2, that shows some real-world examples where logic flaws can happen.  An overview of some of those examples will be below.

<br>

### Logic Flaw Examples / Concepts

* Remove parameters/cookies/query strings in each of the requests one at a time and analyze the responses.  This ensures that all relevant code paths within the application are reached.

* In multistage processes attempt to “force browse” and submit requests in different orders and analyze the responses.  Think of the assumptions that may have been made.

* In a funds transfer application for example, try submitting negative values or very large values.  Analyze the affects it has on the application.

* In any situation where sensitive values are adjusted based on user controllable criteria, analyze if this is a one-time process or if these values change based on further actions by the user. 
    * Example: Getting a discount after a minimum total is reached, then removing items to lower that amount, while still using the discount

* Sometimes an escape character is used to escape malicious characters to protect against certain vulnerabilities such as command injection.  We can inject our own escape character \ to neutralize the escape character that is used for defense.
   * For example, injecting the following payload ( ; ls ) results in ( \\; ls ).  
   * However, if we inject the following payload ( \\; ls ) then the application will still insert an escape character, but it will be neutralized ( \\\\; ls ).

* Identify any instances where the application either truncates, strips out, encodes or decodes user supplied data.  Determine if malicious strings can be derived.

* Identify cases where the application is storing information in a static manner as opposed to per-thread/per-session based.
    * Examples:  There is an endpoint that holds error messages that contain user info (not session based), so a user can potentially see details for another user.  Race conditions in login functionalities, where static values are used to determine the user in the backend, so its possible for a user to see another user’s data upon logging in.

<br>

---
---

<br>

## Cheat Sheet

<br>

### Excessive trust in client-side controls and High-level logic flaw

* Use a Web Proxy to bypass any client-side restrictions implemented on the application.  We can change the values for critical parameters and potentially break the logic of the application.  
   
   * For example, changing the price of an item on our shopping cart to an arbitrary value.  

   * Another example, change the quantity value of an item purchased to a negative number, which may bring the total price of our shopping cart order down.

<br><br>

### Low-level logic flaw

* Manipulate a numeric input field so that its value reaches a very large number.  Analyze how the application responds, maybe there is a limit and once it is reached, it may be reverted back to zero or a negative number.  Depending on the context, this logic flaw can be very critical.

   * For example, if the total price of a shopping cart reverts back to 0 then this can be bad for the application/company.

<br><br>

### Inconsistent handling of exceptional input

* Similar to the previous point, by submitting a very large value to an input field, the application may truncate the value to a certain character size limit.  Depending on the context this can be used to bypass some restrictions on the application.

* When using the Exploit Server in the labs, this is an example of the submitted payload for the email client:

   * GGGGGG@dontwannacry.com.exploit-0af9002f03ad294781cd9cd301d3009d.exploit-server.net
    
   * For example, if the application allows users to register an account try to submit a very large value for the email address.  The application may truncate the email after confirmation and set it as GGGGGG@dontwannacry.com in the application.

<br><br>

### Inconsistent security controls

* After registering an account on an application.  Identify if there are any “Update email” functionality available.  Use this functionality and identify if the application requires verification on the new email address specified before fully updating our email address.  If it does not, then we can update our email to an arbitrary value and potential bypass some access controls.

<br><br>

### Weak isolation on dual-use endpoint

* Remove parameters completely from requests and analyze how the application responds.  This can potentially bypass some restrictions or logic that the application is using.  

    * For example, in a “change password” functionality, remove the “current-password” parameter if there is one.

<br><br>

### Insufficient workflow validation and Authentication bypass via flawed state machine

* When going through a workflow/functionality, skip a step and see how the application responds.  We may be able to bypass a critical step in the process.  
    
    * For example, in a “Cart checkout” workflow, skip the "checkout" step and go straight to the “order confirmation” step. 
    
    * Another example, if after logging into an application you must select a “role”.  Drop all of the requests after logging into the application and analyze how the application responds, we may be able to bypass some access control related functions, since our “role” was never selected.  This is essentially a “force browse” bypass.

<br><br>

### Flawed enforcement of business rules

* If the application has 2 coupons that can be used to get a discount on an order, but these coupons should only be allowed to use once per order, try submitting them one after another in the same purchase order and analyze how the application responds.  This may bypass some flawed logic on the application.

<br><br>

### Infinite money logic flaw

* If the application offers a coupon code that can be used when submitting an order, check if this coupon can be used an infinite number of times once per order.
   
   * For example, we can purchase a gift card and use the coupon code when purchasing it, and when redeeming the gift card, we earn a profit.  An “Infinite money logic flaw” can be exploited here, if the coupon can be used many times.  If using Burp Intruder, the Max Concurrent Requests configuration should be set to 1, as the order of the requests will be important.  See lab/document details.

<br><br>

### Authentication bypass via encryption oracle

* One last example not discussed here (see lab) - [Encryption Oracle](https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle)

<br><br><br>

### Pending to complete labs that are missing from cheat sheet:

* All labs in this category are completed and referenced in cheat sheet.
