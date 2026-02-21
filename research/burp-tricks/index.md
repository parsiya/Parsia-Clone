---
title: "Burp Tips and Tricks"
draft: false
toc: true
comments: false
categories:
- Research
tags:
- Burp
wip: true
snippet: "Small Burp Tips and Tricks."
---

# Sharing Burp Projects without Secrets with Hackvertor
You want to share a Burp project with others without sharing tokens and secrets.

1. Install [Hackvertor][hackvertor] (you probably already have it).
2. Create a Hackvertor global variable.
    1. Click the `Hackvertor` in the menu bar (not the tab).
    2. Select `Global variables`
    3. Create a new variable named `token` (or anything really).
3. You can also create a global variable in the Hackvertor tab like this:
    1. `<@set_token ('true')>1234</@set_token>`
4. In Repeater, use `<@get_token/>` for the token.
5. When you're ready to share, modify the value of the global variable(s) from step 2 to some random value.
6. Create a copy of the project with just Repeater (or the tools you want to share).
    1. Click the project menu item.
    2. Select `Save copy`.
    3. Select the tools.
7. ???
8. Profit.

[hackvertor]: https://github.com/hackvertor/hackvertor

## Custom Action
You can create a custom Repeater action that replaces the value of the `Authorization`
header with `Bearer <@get_token/>`.

```java
var req = requestResponse.request();
var newHeader = HttpHeader.httpHeader("Authorization", "Bearer <@get_token/>");
var modifiedReq = req.withHeader(newHeader);
httpEditor.requestPane().set(modifiedReq);
```

There is one snag here:

1. We have to manually run the custom action for each repeater tab.
2. Repeater actions have a `Auto-Run on Send` setting but it has to be enabled
   for each repeater tab individually. If you enable it for my repeater tab, it's not
   automatically enabled for all others.

My current workflow is:

1. Set a hotkey for `Run last used custom action`. For me it's `ctrl+shift+e`.
2. I've created a macro on my keyboard set to `fn+r`. When I press it on a
   request, it does the following with 50ms delay between key presses:
    1. `ctrl+r` to send the request to Repeater.
    2. `ctrl+shift+r` to switch to Repeater.
    3. `ctrl+shift+e` to run the last used custom action.
    4. `ctrl+space` to send the request.

This works for the most part, but if I use any other action, I need to go and
run the custom action above once so it becomes the `last used custom action`.

Having a "default custom action" that is shared between repeater tabs will help
here because I can enable `Auto-Run on Send` and then send a request to repeater
and send it with one key and not have to worry about what the last used action
was.

## Details
Recently, I was testing an API at work. Unsurprisingly, this API used an
~~AAD token~~ Entra ID token which is just a JWT.

Hint: If you get such a token, drop it into http://jwt.ms (it's a Microsoft
website) and the claims section will give a lot more info that the other site.

I had all the APIs mapped up in nice tab groups in Burp and I wanted to share it
with my team members so they can easily start poking the API. But I did not
want to share my token.

First I created a Hackvertor global variable. Click the `Hackvertor` in the
menu. There's also a Hackvertor tab, don't confuse these. Menu is the one on
top.

{{< imgcap title="Hackvertor menu" src="token-01.png" >}}

Then select `Global variable`.

{{< imgcap title="Global variable" src="token-02.png" >}}

Now you can create a new global variable. Let's name it `token` and assign it a
"real" value.

{{< imgcap title="Create the token global variable" src="token-03.png" >}}

You can also create a global variable in the Hackvertor tab like this:
`<@set_token ('true')>1234</@set_token>`.

Use the Hackvertor variable in Repeater. You can reference a variable
like this `<@get_{variable_name}/>` which in our case will be `<@get_token/>`.

{{< imgcap title="Sample API request using the variable" src="token-04.png" >}}

After the API was mapped, I change the value of the `token` to something random.
You can also completely delete the variable and ask your team members to create
it again, but updating a value is easier.

Then I clicked the `Project` menu item and selected `Save copy`.

{{< imgcap title="Save copy" src="token-05.png" >}}

This allows us to create a copy of the project with just the Repeater tab.

And now you can share the project without any secrets.

![](token-06-oprah.jpg)

## Other Benefits
This also works with secrets. Assume you have a client secret for getting a
token, you can share the APIs without the token using the same method.

This is also useful when tokens expire. Now you do not have to replace them in
Burp Repeater/Scanner for older tabs. You can just update it in Hackvertor.

## Limitations
This was done for a token that was valid for 24 hours and I was getting the
token using a different method that was not a web API, so I did not need to do
any automation. I mean, you could do automation, but I don't think it's worth it
for something you need to do once a day for a few weeks.

A lot of folks automatically update their tokens using Burp macros. There are
many blog posts showing how to do this. It looks like it's possible to update a
Hackvertor variable from an extension, but I have not looked into this.

See this [discussion on Twitter][twt] about updating a custom Hackvertor tag
from a Python script. Adding the gist from that Tweet here, too:
https://gist.github.com/fransr/34a17f59c71d4d525c41284766a48ebe.

[twt]: https://twitter.com/fransrosen/status/1361594153268871168