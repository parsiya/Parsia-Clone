# Launch Process
It seems like we cannot launch anything through the service, so there's no local privilege escalation :(

The client launches everything and thus has the same access level as the current user.

However, we may be able to inject data through community chat and change the game paths, that way we can get RCE as normal user.

This is not certain, the big IF is game paths can be modified through injected JS through community chat.

But let's look at how games are launched through the client anyways.


Launch Process is at `GameScannerClient.dll.>	GameScannerClient.GameScannerClient.LaunchProcess(string launchPath, string launchParams)`.

Put a breakpoint on it and start the client. Login and launch one game. I have added `calc.exe` manually before.

``` csharp
private bool LaunchProcess(string launchPath, string launchParams)
{
  Process process = new Process();
  process.StartInfo.WorkingDirectory = Path.GetDirectoryName(launchPath);
  process.StartInfo.FileName = Path.GetFileName(launchPath);
  process.StartInfo.Arguments = launchParams;
  try
  {
    process.Start();
  }
  catch (Exception ex)
  {
    GameScannerClient.LogMessage("LaunchProcess", string.Format("Failed to launch {0} | Reason: {1}", launchPath, ex.ToString()), 0);
    return false;
  }
  return true;
}
```

Now we can look at the call stack to see how we got here.

```
GameScannerClient.dll!Razer.GameScannerClient.GameScannerClient.LaunchProcess(string launchPath, string launchParams) <-- we're here
GameScannerClient.dll!Razer.GameScannerClient.GameScannerClient.RzGSC_LaunchGame(Razer.GameScannerCommon.GameSignature gs)
RazerComms.exe!RazerComms.Model.GamesMgr.LaunchGameAction(RazerComms.Model.Game gameIn)
RazerComms.exe!RazerComms.ViewModel.GamesViewModel.OnLaunchGameCommand(RazerComms.Model.Game inGame)
RazerComms.exe!RazerComms.ViewModel.GamesViewModel.<.ctor>b__1(RazerComms.Model.Game g)
[Native to Managed Transition]
...
GalaSoft.MvvmLight.dll!GalaSoft.MvvmLight.Helpers.WeakAction<RazerComms.Model.Game>.Execute(RazerComms.Model.Game parameter)
GalaSoft.MvvmLight.dll!GalaSoft.MvvmLight.Command.RelayCommand<RazerComms.Model.Game>.Execute(object parameter)
RazerComms.exe!RazerComms.Foundation.CommsRelayCommand<RazerComms.Model.Game>.Execute(object parameter)
...
RazerComms.exe!RazerComms.App.Main() (IL=~0x000C, Native=0x05BA6528+0x53)
```

Essentially at `>	RazerComms.exe!RazerComms.Foundation.CommsRelayCommand<RazerComms.Model.Game>.Execute(object parameter)` a game is passed from the menu.

Each game has a signature. The signature contains items such as a UDID, path, other command line parameters and icon.

Now we need to see if we can add a new game or better modify a game path through community.
