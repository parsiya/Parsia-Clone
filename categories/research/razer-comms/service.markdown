# Razercomms service

The installer requires admin access. While the application runs as normal user.

We need to see if we can do local privilege escalation. It's not going to be a critical vulnerability anyways but will be fun to look at and hopefully we will learn a thing or two about local privilege escalation through app services.

First we need to find out where the service is.

`Services.msc` and then we see the `Razer Game Scanner Service` at `C:\Program Files (x86)\Razer\Razer Services\GSS\GameScannerService.exe`.

![](images/service01.png)

It is run as SYSTEM.

![](images/service02.png)

We can try and see how they connect. The way to get the scanner service to work is to open Razer Comms and then press `Scan` on the last tab (which is `Games`).
We can try and capture local network traffic using RawCap to see if they are using something like .NET Remoting. Be sure to remove IE proxy settings, otherwise you will capture a lot of traffic between apps and Burp.

There's no traffic so they are using something else.

Let's take a look at the binary. Cool it's a .NET binary we can use dnSpy.

Remember to use dnSpy-x86 to open because these are 32-bit apps and although we can decompile them using the 64-bit version of dnSpy we cannot debug.

A little bit of fiddling around in dnSpy and we see the `PipeServer` and `PipeClient` modules in `RazerServiceBase.dll`. It seems like the application and service use named pipes.

Named pipe MSDN link: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365590(v=vs.85).aspx

Some important parts:

```
The server-side function for instantiating a named pipe is CreateNamedPipe.
The server-side function for accepting a connection is ConnectNamedPipe.
A client process connects to a named pipe by using the CreateFile or CallNamedPipe function.
```

Impersonating a Named pipe: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365573(v=vs.85).aspx

```
Impersonation enables the server thread to perform actions on behalf of the client, but within the limits of the client's security context.
A named pipe server thread can call the ImpersonateNamedPipeClient function to assume the access token of the user connected to the client end of the pipe.
```

![](images/service03.png)

To find out all named pipes, we can use the `Pipelist` utility from `Sysinternals`. You should already have Sysinternals in your VM.

```
$ pipelist.exe

PipeList v1.01
by Mark Russinovich
http://www.sysinternals.com

Pipe Name                                    Instances       Max Instances
---------                                    ---------       -------------
GameScannerPipe                                   2               -1
```

## So we have a pipe name. How can we sniff it?

I have never done this before. We can learn how to do it together.

**Game scanner logs: C:\ProgramData\Razer\Services\Logs**

## Debugging

In dnSpy put a breakpoint on `RazerServiceBase.dll > RazerServiceBase.ctor(string serviceName, RzServiceType serviceType, string pipeName)` and you can see the pipename in dnSpy.

![](images/service04.png)

``` csharp
protected RazerServiceBase(string serviceName, RzServiceType serviceType, string pipeName)
{
  this.m_pipeServer = new PipeServer(pipeName);
  this.m_pipeServer.OnConnect += new PipeConnectDelegate(this.m_pipeServer_OnConnect);
  this.m_socketManager = new SocketManager();
  this.m_socketManager.AddReceiveHandler(RzServiceType.ServiceManager, new DataReceivedDelegate(this.OnServiceReceive));
  this.m_socketManager.AddReceiveHandler(serviceType, new DataReceivedDelegate(this.OnReceive));
  base.ServiceName = serviceName;
}
```
