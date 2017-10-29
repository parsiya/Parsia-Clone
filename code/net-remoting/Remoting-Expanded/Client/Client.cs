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
    class Client
    {
        static void Main(string[] args)
        {
            TcpChannel clientRemotingChannel = new TcpChannel();
            ChannelServices.RegisterChannel(clientRemotingChannel, false);

            RemoteMathExpanded remoteMathObject = (RemoteMathExpanded)Activator.GetObject(typeof(RemoteMathExpanded), "tcp://localhost:8888/rMath");

            // now we can call Add and Sub functions

            Console.WriteLine("Result of Add(1, 2): {0}", remoteMathObject.Add(1, 2));

            Console.WriteLine("Result of Sub(10, 3): {0}", remoteMathObject.Sub(10, 3));

            // example on how to use this exposed object
            // remoteMathObject.StartProcess("c:\\Windows\\System32\\cmd.exe");

            Console.WriteLine("Press any key to exit");
            Console.ReadLine();
        }
    }
}
