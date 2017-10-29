

Login creds are stored in `%AppData%\local\razer\Core\Accounts\RazerLoginData.xml`.

Password is encrypted and stored in base64.

Try to find out how it is stored. The `RazerStorage` DLL might be a good start.

----------------------

Account tokens are stored in xml files at.

`C:\ProgramData\Razer\Core\Accounts`

``` xml
<?xml version="1.0" encoding="utf-8"?>
<RazerAccount xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
  <AdditionalIds xmlns:d2p1="http://schemas.microsoft.com/2003/10/Serialization/Arrays" i:nil="true" />
  <HomeFolder>C:\ProgramData\Razer\Core\Accounts\AM_8640973</HomeFolder>
  <ServerID>RZR_...</ServerID>
  <ServerToken>...</ServerToken>
  <Username>username@email.com</Username>
</RazerAccount>
```

-------------

Logs are enabled:

`C:\ProgramData\Razer\Core\Logs`

-------------

Master Game List - to choose a game to test in game overlay

`C:\ProgramData\Razer\GameScanner\MasterGameList.xml`

-------------
