# Settings

Settings update: post request with base64 encoded data

Decoded base64 in the data element:

Changing the username does not make it go another user :(

But the modified email stays there in the settings. hmm.

Same as user-uuid

``` xml
<user>
  <username>username@email.com</username>
  <PushtoTalk>1</PushtoTalk>
  <AutoAcceptChat>0</AutoAcceptChat>
  <AutoAcceptFriend>0</AutoAcceptFriend>
  <SaveReminder>1</SaveReminder>
  <ShowHistory>1</ShowHistory>
  <TabbedChat>1</TabbedChat>
  <CloseWarning>1</CloseWarning>
  <user-uuid>RZR_00...</user-uuid>
  <Shortcut-CW-key>Ctrl+Tab</Shortcut-CW-key>
  <Shortcut-PTT-key></Shortcut-PTT-key>
  <HotkeyMicMute>1</HotkeyMicMute>
  <HotkeyAnswerCall></HotkeyAnswerCall>
  <HotkeyRejectCall></HotkeyRejectCall>
  <ActiveAlphaLevel>255</ActiveAlphaLevel>
  <InactiveAlphaLevel>127</InactiveAlphaLevel>
  <HideOfflineFriends>0</HideOfflineFriends>
  <ShowGame>1</ShowGame>
  <IsNotifyFriendsWhenIWatchStream>1</IsNotifyFriendsWhenIWatchStream>
  <IsFriendWatchStreamNotify>1</IsFriendWatchStreamNotify>
  <IsStreamLiveNotify>1</IsStreamLiveNotify>
  <OnlineNotify>1</OnlineNotify>
  <FriendGameNotify>1</FriendGameNotify>
  <MsgNotify>1</MsgNotify>
  <RequestNotify>1</RequestNotify>
  <EnableOverlay>1</EnableOverlay>
  <InGameOnlineNotify>0</InGameOnlineNotify>
  <InGameFriendGameNotify>0</InGameFriendGameNotify>
  <InGameMsgNotify>0</InGameMsgNotify>
  <InGameGroupMsgNotify>1</InGameGroupMsgNotify>
  <InGameRequestNotify>0</InGameRequestNotify>
  <InGameFriendWatchStreamNotify>0</InGameFriendWatchStreamNotify>
  <InGameStreamLiveNotify>0</InGameStreamLiveNotify>
  <PlaySoundReqIn>1</PlaySoundReqIn>
  <PlaySoundFriendsOnline>1</PlaySoundFriendsOnline>
  <PlaySoundVoiceCallIn>1</PlaySoundVoiceCallIn>
  <PlaySoundMsgIn>1</PlaySoundMsgIn>
  <IsPlaySoundStreamLive>1</IsPlaySoundStreamLive>
  <IsPlaySoundFriendWatchStream>1</IsPlaySoundFriendWatchStream>
  <IsPlaySoundFriendPlayGame>1</IsPlaySoundFriendPlayGame>
  <IsAlwaysShowCommunityTutorial>0</IsAlwaysShowCommunityTutorial>
  <chatpos>0|0|0|0</chatpos>
  <FacebookToken></FacebookToken>
  <FacebookName></FacebookName>
  <FacebookID></FacebookID>
  <ChatInfoOnlineStatus>1</ChatInfoOnlineStatus>
  <ChatInfoStartAudio>1</ChatInfoStartAudio>
  <ChatInfoKickBan>1</ChatInfoKickBan>
  <ChatInfoJoinChannel>1</ChatInfoJoinChannel>
  <ChatInfoChannelMute>1</ChatInfoChannelMute>
  <ChatInfoTypingStatus>1</ChatInfoTypingStatus>
  <ChatColorNameRemote>-15954932</ChatColorNameRemote>
  <ChatColorMessage>-1</ChatColorMessage>
  <ChatHotkeyEnable>0</ChatHotkeyEnable>
  <VoiceCallHotkey>0</VoiceCallHotkey>
  <FileTransferWarning>1</FileTransferWarning>
  <Mobile_RejectCallResponseCode>1</Mobile_RejectCallResponseCode>
  <HotkeyMobileInDeclineSMS>Enter</HotkeyMobileInDeclineSMS>
  <HotkeyMobileInIgnore>Escape</HotkeyMobileInIgnore>
  <HotkeySMSInReply>Enter</HotkeySMSInReply>
  <HotkeySMSInDismiss>Escape</HotkeySMSInDismiss>
  <HotkeyOverlayOnOff>Ctrl+Shift+Tab</HotkeyOverlayOnOff>
  <GSMCallNotification>1</GSMCallNotification>
  <SMSNotification>1</SMSNotification>
  <SMSAutoAppend>1</SMSAutoAppend>
  <SMSMsgSequence></SMSMsgSequence>
  <SMS_CustomMsg0></SMS_CustomMsg0>
  <SMS_CustomMsg1></SMS_CustomMsg1>
  <SMS_CustomMsg2></SMS_CustomMsg2>
  <SMS_CustomMsg3></SMS_CustomMsg3>
  <SMS_CustomMsg4></SMS_CustomMsg4>
  <SMS_CustomMsg5></SMS_CustomMsg5>
  <SMS_CustomMsg6></SMS_CustomMsg6>
  <SMS_CustomMsg7></SMS_CustomMsg7>
  <SMS_CustomMsg8></SMS_CustomMsg8>
  <SMS_CustomMsg9></SMS_CustomMsg9>
  <ChatHistoryLastClearDate>0001-01-01T00:00:00</ChatHistoryLastClearDate>
  <ShowSystrayWarning>1</ShowSystrayWarning>
  <IsShowRecommendedCommunities>0</IsShowRecommendedCommunities>
  <SnapPositions></SnapPositions>
  <Nickname>alert(1)</Nickname>
  <InGameTutorial>0</InGameTutorial>
  <FileTransferReceivePath>C:\Users\x64\Downloads</FileTransferReceivePath>
  <FriendsTabFriendsFilter>All</FriendsTabFriendsFilter>
  <IsPlaySoundAnnouncement>1</IsPlaySoundAnnouncement>
  <IsNotifyAnnouncement>1</IsNotifyAnnouncement>
  <IsNotifyAnnouncementInGame>0</IsNotifyAnnouncementInGame>
  <IsPlaySoundMicEnabled>0</IsPlaySoundMicEnabled>
  <IsFirstTimeRecommendedStreams2>1</IsFirstTimeRecommendedStreams2>
</user>
```


``` xml
POST /1/setting/put HTTP/1.1
Content-Type: application/xml
Host: ecbeta.razerzone.com
Content-Length: 5937
Expect: 100-continue
Connection: close

<COP>
  <User>
    <ID>RZR_...</ID>
    <Token>...</Token>
  </User>
  <Setting>
    <Name>comms-settings.xml</Name>
    <Path>Comms</Path>
    <Data></Data>
    <Encoding>0</Encoding>
  </Setting>
  <Product>
    <Name>Heidi</Name>
    <Version></Version>
  </Product>
</COP>

```


Response to settings update:

``` html
<?xml version='1.0' standalone='yes'?>
<COP>
  <User>
    <ID>RZR_...</ID>
  </User>
  <Setting>
    <Name>comms-settings.xml</Name>
    <Path>Comms</Path>
    <Data>...</Data>
    <UpdateTimestamp>1461391511</UpdateTimestamp>
    <OriginalSize>0</OriginalSize>
    <Encoding>0</Encoding>
  </Setting>
  <Product>
    <Name>Heidi</Name>
    <Version>1.0.0.0</Version>
  </Product>
  <Status>
    <Errno>1</Errno>
    <Message>settings saved</Message>
  </Status>
  <RequestStatus>
    <Errno>1</Errno>
    <Message>settings saved</Message>
    <Timestamp>1461391511</Timestamp>
    <Server>10.178.7.159</Server>
  </RequestStatus>
</COP>
```
