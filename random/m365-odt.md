---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- office
- Windows
title: "Microsoft 365 Office Deployment Tool"
wip: false
snippet: "So you want to only install specific M365 apps."
---

1. Uninstall Microsoft Office 365 from your machine.
2. Go to https://config.office.com/deploymentsettings and create a configuration.
    1. Don't worry if you cannot find your version under `Products > Office Suites`. Choose anything, we will override this.
3. Create a configuration, remove any apps you do not want, there's also some extra configuration that alters the registry which is optional. Download it, let's say it's named `myconfig.xml`.
4. Open the configuration file and replace the value of `<Product ID="...">` with `O365ProPlusRetail`.
    1. So the entire tag will look like `<Product ID="O365ProPlusRetail">`.
5. Download the `Office Deployment Tool` at https://www.microsoft.com/en-us/download/details.aspx?id=49117.
    1. Link might change in the future, if so, just search for it.
6. Run it and it will ask for a path to "extract" files.
7. After extraction it will create a `setup.exe` and a configuration XML file.
8. Run `setup.exe /download myconfig.xml`. It will download the needed files.
9. Run `setup.exe /configure myconfig.xml`. It will only install certain office apps.

Here is my file. `AppSettings` has a bit of configuration like "edit the files in the desktop app instead of the browser." You can safely remove that tag.

```xml
<Configuration ID="e45e4877-2ea5-4172-80a8-c1b8b75a7f72">
  <Add OfficeClientEdition="64" Channel="Current">
    <Product ID="O365ProPlusRetail">
      <Language ID="MatchOS" />
      <ExcludeApp ID="Access" />
      <ExcludeApp ID="Groove" />
      <ExcludeApp ID="Lync" />
      <ExcludeApp ID="Outlook" />
      <ExcludeApp ID="Publisher" />
      <ExcludeApp ID="Teams" />
    </Product>
  </Add>
  <Updates Enabled="TRUE" />
  <RemoveMSI />
  <AppSettings>
    <User Key="software\microsoft\office\16.0\common\toolbars" Name="screentipscheme" Value="2" Type="REG_DWORD" App="office16" Id="L_ShowScreenTips" />
    <User Key="software\microsoft\office\16.0\common\internet" Name="opendirectlyinapp" Value="1" Type="REG_DWORD" App="office16" Id="L_OpenDirectlyInApp" />
    <User Key="software\microsoft\office\16.0\common\internet" Name="opendocumentsreadwritewhilebrowsing" Value="0" Type="REG_DWORD" App="office16" Id="L_OpenOfficedocumentsasreadwritewhilebrowsing" />
    <User Key="software\microsoft\office\16.0\common\internet" Name="allowpng" Value="1" Type="REG_DWORD" App="office16" Id="L_AllowPNGasanoutputformat" />
    <User Key="software\microsoft\office\16.0\common" Name="sendcustomerdata" Value="0" Type="REG_DWORD" App="office16" Id="L_Sendcustomerdata" />
  </AppSettings>
</Configuration>
```

## Modifying Existing Installation
Theoretically, you can alter an existing installation with the same tool and a config that looks a bit different. **But it did not work.** So I had to uninstall and reinstall.

I tried the following config and it did not work. Note, version, ID and language must match what's installed hence I have used `MatchInstalled` and `MatchOS` in the file.

```xml
<Configuration>
  <Remove Version="MatchInstalled">
    <Product ID="O365ProPlusRetail">
      <Language ID="MatchOS" />
      <ExcludeApp ID="Access" />
      <ExcludeApp ID="Bing" />
      <ExcludeApp ID="Groove" />
      <ExcludeApp ID="Lync" />
      <ExcludeApp ID="Publisher" />
      <ExcludeApp ID="Teams" />
      <ExcludeApp ID="Outlook" />
    </Product>
  </Remove>
</Configuration>
```