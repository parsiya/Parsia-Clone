using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Runtime.Remoting.Channels.Tcp;

namespace RemotingSample
{
    class Server
    {
        static void Main(string[] args)
        {
            // create a TCP channel and bind it to port 8888
            TcpChannel remotingChannel = new TcpChannel(8888);

            // register the channel, the second parameter is ensureSecurity
            // I have set it to false to disable encryption and signing
            // for more information see section Remarks in https://msdn.microsoft.com/en-us/library/ms223155(v=vs.90).aspx
            ChannelServices.RegisterChannel(remotingChannel, false);

            // create a new servicetype of type RemoteMath named "rMath" and of type SingleCall
            // SingleCall: a new object will be created for each call
            // as opposed to WellKnownObjectMode.Singleton where there is one object for all calls (and clients)
            WellKnownServiceTypeEntry remoteObject = new WellKnownServiceTypeEntry(typeof(RemoteMath), "rMath", WellKnownObjectMode.SingleCall);

            // register the remoteObject servicetype
            RemotingConfiguration.RegisterWellKnownServiceType(remoteObject);

            Console.WriteLine("Registered service");
            Console.WriteLine("Press any key to exit");
            Console.ReadLine();

        }
    }
}
