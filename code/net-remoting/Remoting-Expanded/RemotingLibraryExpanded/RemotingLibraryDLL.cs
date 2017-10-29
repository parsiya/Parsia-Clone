using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace RemotingLibraryExpanded
{
    public class RemoteMathExpanded : MarshalByRefObject
    {
        public int Add(int a, int b)    // add
        {
            Console.WriteLine("Add({0},{1}) called", a, b);
            return a + b;
        }

        public int Sub(int a, int b)    // subtract
        {
            Console.WriteLine("Sub({0},{1}) called", a, b);
            return a - b;
        }

        // super secret process start method
        public void StartProcess(string processPath)
        {

            Console.WriteLine("Starting process {0}", processPath);
            Process.Start(processPath);
            
        }
    }
}
