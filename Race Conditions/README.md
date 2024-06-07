# Race Conditions

<br>

## Summary

<!-- MarkdownTOC -->

- [Overview](#overview)
- [Limit overrun race conditions](#limit-overrun-race-conditions)
	- [Detecting and exploiting limit overrun race conditions with Burp Repeater](#detecting-and-exploiting-limit-overrun-race-conditions-with-burp-repeater)
		- [Lab: Limit overrun race conditions](#lab-limit-overrun-race-conditions)
	- [Detecting and exploiting limit overrun race conditions with Turbo Intruder](#detecting-and-exploiting-limit-overrun-race-conditions-with-turbo-intruder)
		- [Lab: Bypassing rate limits via race conditions](#lab-bypassing-rate-limits-via-race-conditions)
- [Hidden multi-step sequences](#hidden-multi-step-sequences)
	- [Methodology](#methodology)
	- [Multi-endpoint race conditions](#multi-endpoint-race-conditions)
	- [Aligning multi-endpoint race windows](#aligning-multi-endpoint-race-windows)
		- [Lab: Multi-endpoint race conditions](#lab-multi-endpoint-race-conditions)
- [Single-endpoint race conditions](#single-endpoint-race-conditions)
	- [Lab: Single-endpoint race conditions](#lab-single-endpoint-race-conditions)
- [Partial construction race conditions](#partial-construction-race-conditions)
	- [Lab: Partial construction race conditions](#lab-partial-construction-race-conditions)
- [Time-sensitive attacks](#time-sensitive-attacks)
	- [Lab: Exploiting time-sensitive vulnerabilities](#lab-exploiting-time-sensitive-vulnerabilities)

<!-- /MarkdownTOC -->



<br><br>

### Overview

* Race conditions are a common type of vulnerability closely related to business logic flaws. They occur when websites process requests concurrently without adequate safeguards. This can lead to multiple distinct threads interacting with the same data at the same time, resulting in a "collision" that causes unintended behavior in the application.

* A race condition attack uses carefully timed requests to cause intentional collisions and exploit this unintended behavior for malicious purposes. The period of time during which a collision is possible is known as the "race window". This could be the fraction of a second between two interactions with the database, for example. 


<br><br>


### Limit overrun race conditions

*  The most well-known type of race condition enables you to exceed some kind of limit imposed by the business logic of the application.

* For example, consider an online store that lets you enter a promotional code during checkout to get a one-time discount on your order. To apply this discount, the application may perform the following high-level steps:

    * Check that you haven't already used this code.
    * Apply the discount to the order total.
    * Update the record in the database to reflect the fact that you've now used this code.

* If we send 2 or more requests concurrently, we can try to abuse the "race window", that is before the application updates the database, in order to use the same discount code more than once.

*  There are many variations of this kind of attack, including:

    * Redeeming a gift card multiple times
    * Rating a product multiple times
    * Withdrawing or transferring cash in excess of your account balance
    * Reusing a single CAPTCHA solution
    * Bypassing an anti-brute-force rate limit

<br>

#### Detecting and exploiting limit overrun race conditions with Burp Repeater

* The process of detecting and exploiting limit overrun race conditions is relatively simple. In high-level terms, all you need to do is:

    * Identify a single-use or rate-limited endpoint that has some kind of security impact or other useful purpose.
    * Issue multiple requests to this endpoint in quick succession to see if you can overrun this limit.

* The primary challenge is timing the requests so that at least two race windows line up, causing a collision. This window is often just milliseconds and can be even shorter. 


Sending requests in parallel - https://portswigger.net/burp/documentation/desktop/tools/repeater/send-group#sending-requests-in-parallel

<br>

##### Lab: Limit overrun race conditions

* This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.

* Use all of the application's available functionality, including using the PROMO code when purchasing an item.

* Send the following request to Burp Repeater (ensure to have added the expensive Jacket into your cart before this step):

```
POST /cart/coupon HTTP/2
Host: 0a77008c045c4af180f9e44f00ac00d1.web-security-academy.net
REDACTED...

csrf=UfjDdxlSAUrINBasJasUgfvqCR&coupon=PROMO20
```

* This^ is the request that is used to process the coupon in our purchase order.  We will use the "single packet" attack to complete around 20-30 requests simultaneously to see if we can exploit the "race window", which is before the application updates the database with info confirming coupon has already been used in the order.

* Send around 20 of the same request to Burp Repeater^ and create a "group" that will include all of the tabs for the same request.

* Finally select the option "Send group in parallel (single-packet attack)", and submit the requests.  This may take a couple of tries, but eventually we were able to submit multiple coupons in the same Order to purchase the Jacket. The coupon is only supposed to be used once per Order, but exploiting a race condition vulnerability allows for a bypass.


<br><br>

#### Detecting and exploiting limit overrun race conditions with Turbo Intruder


<br>

##### Lab: Bypassing rate limits via race conditions


* https://portswigger.net/web-security/race-conditions/lab-race-conditions-bypassing-rate-limits

<br><br>


### Hidden multi-step sequences


*  In practice, a single request may initiate an entire multi-step sequence behind the scenes, transitioning the application through multiple hidden states that it enters and then exits again before request processing is complete. We'll refer to these as "sub-states".

* If you can identify one or more HTTP requests that cause an interaction with the same data, you can potentially abuse these sub-states to expose time-sensitive variations of the kinds of logic flaws that are common in multi-step workflows.


<br>

#### Methodology

* Predict potential collisions

    * Is this endpoint security critical? Many endpoints don't touch critical functionality, so they're not worth testing.
    
    * Is there any collision potential? For a successful collision, you typically need two or more requests that trigger operations on the same record.


* Probe for clues

	* To recognize clues, you first need to benchmark how the endpoint behaves under normal conditions. You can do this in Burp Repeater by grouping all of your requests and using the Send group in sequence (separate connections) option.

	* Next, send the same group of requests at once using the single-packet attack (or last-byte sync if HTTP/2 isn't supported) to minimize network jitter. You can do this in Burp Repeater by selecting the Send group in parallel option.

	* Anything at all can be a clue. Just look for some form of deviation from what you observed during benchmarking.


* Prove the concept

	* Try to understand what's happening, remove superfluous requests, and make sure you can still replicate the effects. 



<br>


#### Multi-endpoint race conditions

* Perhaps the most intuitive form of these race conditions are those that involve sending requests to multiple endpoints at the same time. 

* A variation of this vulnerability can occur when payment validation and order confirmation are performed during the processing of a single request.

* In this case, you can potentially add more items to your basket during the race window between when the payment is validated and when the order is finally confirmed. 


<br>


#### Aligning multi-endpoint race windows

* When testing for multi-endpoint race conditions, you may encounter issues trying to line up the race windows for each request, even if you send them all at exactly the same time using the single-packet technique. 

*  This common problem is primarily caused by the following two factors:

    * Delays introduced by network architecture - For example, there may be a delay whenever the front-end server establishes a new connection to the back-end. The protocol used can also have a major impact.
    
    * Delays introduced by endpoint-specific processing - Different endpoints inherently vary in their processing times, sometimes significantly so, depending on what operations they trigger.

*  Fortunately, there are potential workarounds to both of these issues.

<br>

Connection warming

* One way to do this is by "warming" the connection with one or more inconsequential requests to see if this smoothes out the remaining processing times. In Burp Repeater, you can try adding a GET request for the homepage to the start of your tab group, then using the Send group in sequence (single connection) option.

* If the first request still has a longer processing time, but the rest of the requests are now processed within a short window, you can ignore the apparent delay and continue testing as normal. 

<br>


##### Lab: Multi-endpoint race conditions

* This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price. 

* The 2 main requests that are used to interact with the user's cart are - For example, a POST /cart request adds items to the cart and a POST /cart/checkout request submits your order.

* The state of the user's cart is stored server-side within the user's session cookie.  Any operations on the cart revolve aroung the user's session.  This indicates that there is potential for a collision.

<br>

A summary of the requests that were submitted to benchmark the requests behavior and exploit the lab are below:

(Here we are trying to determine the time it takes to receive the responses)

These requests were sent to Burp Repeater and placed in a Group and processed using the different available configurations

<br>

Send group (Single connection) request:

* POST /cart - 471 millis

* POST /cart/checkout - 173 millis


Send group (Single connection) request: (Here we are "warming" the connection by including the GET request to the beginning of the Group list, the last 2 requests were now processed in similar times)

* GET /academyLabHeader - 447 millis

* POST /cart - 180 millis

* POST /cart/checkout - 174 millis


To solve the lab send the following request in Burp Repeater using the "Send group (parallel)" option: 
(before submitting this payload, ensure that there is a giftcard already in your cart)

* GET /

* POST /cart/checkout

* POST /cart (ensure that the productId parameter is set to 1, as this is the ID for the jacket)


Note:

* Play around with the order of the requests that are submitted in Burp Repeater.  For example, if requests in the order of 1, 2, 3 is not working, try to switch them around like 1, 3, 2.


<br><br>


### Single-endpoint race conditions

* Sending parallel requests with different values to a single endpoint can sometimes trigger powerful race conditions.

* Email address confirmations, or any email-based operations, are generally a good target for single-endpoint race conditions. Emails are often sent in a background thread after the server issues the HTTP response to the client, making race conditions more likely. 

<br>

#### Lab: Single-endpoint race conditions


* https://portswigger.net/web-security/race-conditions/lab-race-conditions-single-endpoint


* The application contains functionality that allows us to update the email address for the user wiener.  The application sends a confirmation email to the email client that is available in the lab.

* There is a race condition vulnerability within this functionality.

* The information that is sent to the email address versus the confirmation message sent in the body of the request are not matching.  For example, the email sent to the address of test123@attacker.com, contains the confirmation message in scope for the email of test987@attacker.com.

* There is a race window between when the website:

    * Kicks off a task that eventually sends an email to the provided address.
     
    * Retrieves data from the database and uses this to render the email template. (The database stores only 1 email address info at a time.  We can confirm this by trying to access an older (not latest) confirmation email request in the client.)


<br>

* Below is a summary of the exploitation steps taken:


Send the following request to Burp Repeater:

* POST /my-account/change-email


* Send around 15 more requests to Burp Repeater for the same endpoint to change the email address.  Make every email address in each request unique.  Group all of the requests and select the "Send group (parallel)" option, then submit requests.

* Next, go to the email client and notice that the confirmation message contains an email address that differs from the email address to which the confirmation message was sent to.  For example, confirmation message contains test555@attacker.com, while the message was sent to the email address test777@attacker.com.  (Note - the email client is meant for us to retrieve all emails sent to any exploit server sub-domain)

<br>

* Now to gain access to the email address - carlos@ginandjuice.shop

* Send 2 requests to repeater for the change email address function - POST /my-account/change-email

* The body payloads for each requests:

	* Request 1 - email=test999%40exploit-0aa1009a0479c5cb8180f74601a100da.exploit-server.net

	* Request 2 - email=carlos@ginandjuice.shop

* Select the option "Send group (parallel)" in Burp Repeater and submit the requests.  This step may need to be initiated many times since the latest email confirmation message needs to contain the value for - carlos@ginandjuice.shop. (This is because in the database there only exists one value at a time.)

* Once the latest email confirmation message contains the value for carlos@ginandjuice.shop process the link and gain access to an admin account.


<br><br>


### Partial construction race conditions


#### Lab: Partial construction race conditions

* https://portswigger.net/web-security/race-conditions/lab-race-conditions-partial-construction

* This lab contains a user registration mechanism. A race condition enables you to bypass email verification and register with an arbitrary email address that you do not own.


<br><br>


### Time-sensitive attacks

*  Sometimes you may not find race conditions, but the techniques for delivering requests with precise timing can still reveal the presence of other vulnerabilities.

* One such example is when high-resolution timestamps are used instead of cryptographically secure random strings to generate security tokens. 


<br>

#### Lab: Exploiting time-sensitive vulnerabilities


* https://portswigger.net/web-security/race-conditions/lab-race-conditions-exploiting-time-sensitive-vulnerabilities

* This lab contains a password reset mechanism. Although it doesn't contain a race condition, you can exploit the mechanism's broken cryptography by sending carefully timed requests.


<br><br><br>

Other Resources:

* https://www.youtube.com/watch?v=xkKZ69jrztA&list=PLzgroH3_jK2hl7uPH4gXq3bbgNLDYXUlR

* https://book.hacktricks.xyz/pentesting-web/race-condition
