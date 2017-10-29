# BMC Track It 11.2
Download BMC Track It 11.2 from CNET. http://download.cnet.com/BMC-Track-It/3000-18482_4-10003961.html?tag=bc

Disconnect your VM from the internet because you don't want to be vulnerable.

First we install it. After installation:

Low and behold we have something listening on port 9010 (on all interfaces).

    PS C:\> netstat -an | findstr.exe "9010"
      TCP    0.0.0.0:9010           0.0.0.0:0              LISTENING
    PS C:\>

**pic01**

But now we have the problem of finding the module that is listening on port 9010.

For that we can use the `b` switch for `netstat` which needs an admin powershell window or command prompt.

    PS C:\> netstat -ab

	Active Connections
      Proto  Local Address          Foreign Address        State
	  ...

     TCP    0.0.0.0:5357           x64-PC:0               LISTENING
     Can not obtain ownership information

      TCP    0.0.0.0:6712           x64-PC:0               LISTENING
     [TIHost.exe]

      TCP    0.0.0.0:9010           x64-PC:0               LISTENING
     [TIServiceManagement.exe]

      TCP    0.0.0.0:49176          x64-PC:0               LISTENING
     [sqlservr.exe]

      TCP    127.0.0.1:49176        x64-PC:49519           ESTABLISHED
     [sqlservr.exe]

      TCP    127.0.0.1:49519        x64-PC:49176           ESTABLISHED
     [TIServiceManagement.exe]
	   ...


So we have two open ports `6712` and `9010`.

We can see that they are running as SYSTEM according to this screenshot from task manager.

**pic02**

And one is a service.

**[pic03]**

At this point we do not know what is running on port `5357` but if we telnet to it we will see some familiar response:

``` html
HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=us-ascii
Server: Microsoft-HTTPAPI/2.0
Date: Wed, 28 Oct 2015 01:35:23 GMT
Connection: close
Content-Length: 326

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN""http://www.w3.org/TR/html4/strict.dtd">
<HTML><HEAD><TITLE>Bad Request</TITLE>
<META HTTP-EQUIV="Content-Type" Content="text/html; charset=us-ascii"></HEAD>
<BODY><h2>Bad Request - Invalid Verb</h2>
<hr><p>HTTP Error 400. The request verb is invalid.</p>
</BODY></HTML>

Connection to host lost.
```

This is interesting, but not what we are looking for. Maybe we will come back to it later.

Connect to `localhost:9010` with telnet or your browser and observe the error message which indicates that we are on the right track.

    .NET..........System.Runtime.Remoting.RemotingException: Tcp channel protocol violation: expecting preamble.
       at System.Runtime.Remoting.Channels.Tcp.TcpSocketHandler.ReadAndMatchPreamble()
       at System.Runtime.Remoting.Channels.Tcp.TcpSocketHandler.ReadVersionAndOperation(UInt16& operation)
       at System.Runtime.Remoting.Channels.Tcp.TcpServerSocketHandler.ReadHeaders()
       at System.Runtime.Remoting.Channels.Tcp.TcpServerTransportSink.ServiceRequest(Object state)
       at System.Runtime.Remoting.Channels.SocketHandler.ProcessRequestNow()

    Connection to host lost.

Navigate to `C:\Program Files (x86)\BMC Software\Track-It!\Track-It! Services` which contains the `TIServiceManagement.exe` executable and look inside the config file `TIServiceManagement.exe.config`.

``` xml
<appSettings>
    <add key="ConfigurationRemotingChannel" value="tcp" />
    <add key="ConfigurationRemotingHost" value="x64-PC" />
    <add key="ConfigurationRemotingPort" value="9010" />

    <!--Remoting Services Manager-->
    <add key="RemotingServiceClass" value="TrackIt.Core.ServiceManagement.ServiceManagementImpl.ServiceManagementServer,TrackIt.Core.ServiceManagement.ServiceManagementImpl" />
    <add key="RemotingServiceName" value="TIServiceManagement" />
    <add key="RemotingServiceDisplayName" value="Track-It! Service Management" />
    <add key="RemotingServiceDescription" value="Manages services instances deployed on this host." />
    <add key="SystemHealth:SystemHealthConfiguration:TrackIt.Core.Configuration.MultisourceConfigurationImpl.DatabaseConfigurationSource" value="Database source" />
</appSettings>
```

Look at `Properties > Details` for `TIServicemanagement.exe` and we will see that the file description is `RemotingServicesManager` as well as its original filename.

**[pic04]**

Here's the thing, we can open the file in dnSpy and poke around but let's cut the chase and look at the local traffic.

To capture local traffic [link to the capturing local traffic blog post] we will use RawCap. Run RawCap, start capturing on the pseudo loopback interface. Now start the application and login. The demo user does not have a password.

**[pic05]**

And we can see the contents (well the printable parts) by using `Follow TCP Stream`.

**[pic06]**

We have seen the first request before (I have filtered out a lot of non-printable characters unless they are needed and we are going to talk about them).

	.NET 3 tcp://x64-PC:9010/TrackIt.Core.ConfigurationService.

Second request

	GetProductDeploymentValues TrackIt.Core.Configuration.IConfigurationSecureDelegator, TrackIt.Core.Configuration, Version=11.2.0.345, Culture=neutral, PublicKeyToken=null

As we have seen before [link to the first .NET remoting post] we can find the DLL and the object that is being called remotely.

	Remote function: GetProductDeploymentValues
    Function class: TrackIt.Core.Configuration.IConfigurationSecureDelegator
    DLL: TrackIt.Core.Configuration

The application that called the remote object is `C:\Program Files (x86)\BMC Software\Track-It!\Track-It! Server\Installers\TechnicianClient\en\TechnicianClient_11_2_0_345\TechnicianClient.exe`. The DLL is question is in the same address.

**[pic07]**

These look to be the list of all exposed functions. `GetFileContent` looks nice.

**[pic7.5]**

Now we want to know when it is called. If we remember from .NET Remoting primers we know that an instance of this function will be created and sent over. Rightclick the function and select `Analyze` and a panel appears. In the panel select `Used By`. This shows every where in loaded binaries (executables and DLLs) that this function is used. In case it is in the same DLL (`TrackIt.Core.Configuration.dll`) and the function is `TrackIt.Core.Configuration.ConfigurationInterceptor. GetProductDeploymentValues()`. Pretty handy neh?

**[pic08]**

Let's put a breakpoint here and run `TechnicianClient.exe` in dnSpy. Now if we want to see how we got here we can use `Debug (menu) > Show Call Stack`. Isn't this nice?

**[pic09]**

Now if we step into three times, we will reach the familiar code base in `mscorlib.dll` at `CommonLanguageRuntimeLibrary.System.Runtime.Remoting.Proxies.RealProxy.PrivateInvoke`.

**[pic10]**

`type` equals `1` so the if statement will be true, now if we step until we after line 408 or `message = expr_14;` (remember that breakpoints set here will not trigger). We can inspect the variable `message` and see the method being called and its arguments if it had any (remember that `Alt+4` will open the `Locals` panel.

**[pic11]**

Great, now we have a decent idea of what is happening here with regards to .NET Remoting. If we go to the `C:\Program Files (x86)\BMC Software\Track-It!\Track-It! Services` directory we will see the a similar set of DLLs (both caller and callee have a copy of methods). In this case the DLL is `TrackIt.Core.Configuration.dll`

**[pic12]**

We can use this DLL to create our own app that connects to the service and does stuff.

