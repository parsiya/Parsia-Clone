using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.Remoting;
using System.Runtime.Remoting.Channels;
using System.Runtime.Remoting.Channels.Tcp;

namespace RemotingLibraryExpanded
{
    class Server
    {
        static void Main(string[] args)
        {
            TcpChannel remotingChannel = new TcpChannel(8888);

            ChannelServices.RegisterChannel(remotingChannel, false);

            WellKnownServiceTypeEntry remoteObject = new WellKnownServiceTypeEntry(typeof(RemoteMathExpanded), "rMath", WellKnownObjectMode.SingleCall);

            RemotingConfiguration.RegisterWellKnownServiceType(remoteObject);

            Console.WriteLine("Registered service");
            Console.WriteLine("Press any key to exit");
            Console.ReadLine();
        }
    }
}
