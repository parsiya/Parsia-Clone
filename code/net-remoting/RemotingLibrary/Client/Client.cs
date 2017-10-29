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
    class Client
    {
        static void Main(string[] args)
        {
            // create and register the TCP channel
            // please note that I have set the security of the channel to false
            TcpChannel clientRemotingChannel = new TcpChannel();
            ChannelServices.RegisterChannel(clientRemotingChannel, false);

            // create an object of type RemothMath
            // we have to do a cast because Activator.GetObject returns an object (doh)
            // type is RemoteMath and server address is what we created in Server.cs (port:8888 and rMath)

            // Server.cs code:
            // TcpChannel remotingChannel = new TcpChannel(8888);
            // ChannelServices.RegisterChannel(remotingChannel, false);
            // WellKnownServiceTypeEntry remoteObject = new WellKnownServiceTypeEntry(typeof(RemoteMath), "rMath", WellKnownObjectMode.SingleCall);

            RemoteMath remoteMathObject = (RemoteMath)Activator.GetObject(typeof(RemoteMath), "tcp://localhost:8888/rMath");

            // now we can call Add and Sub functions

            Console.WriteLine("Result of Add(1, 2): {0}", remoteMathObject.Add(1, 2));
            
            Console.WriteLine("Result of Sub(10, 3): {0}", remoteMathObject.Sub(10, 3));

            Console.WriteLine("Press any key to exit");
            Console.ReadLine();
        }
    }
}
