import winappdbg
import argparse
from winappdbg import win32

# Debug an app with parameters passed by -run
# e.g. python 02-debug2.py c:\windows\system32\notepad.exe c:\textfile.txt
# print system info with --sysinfo
# print current processes if nothing is passed
# attach to a process with --attach-process or -pid


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    # Make -r and -pid mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--run", nargs="+",
                       help="path to application followed by parameters")
    group.add_argument("-pid", "--attach-pid", type=int, dest="pid",
                       help="pid of process to attach and instrument")

    parser.add_argument("-i", "--sysinfo", action="store_true",
                        help="print system information")

    args = parser.parse_args()

    if (args.run):
        # Concat all arguments into a string
        myargs = " ".join(args.run)

        # Use Win32 API functions provided by WinAppDbg
        if win32.PathFileExists(args.run[0]) is True:
            # File exists

            # Create a Debug object
            debug = winappdbg.Debug()

            try:
                # We will talk about this in a minute
                # Debug the app
                # debug.execv([args.app])
                # execl: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/debug.py#L358
                my_process = debug.execl(myargs)

                print "Started %d - %s" % (my_process.get_pid(),
                                           my_process.get_filename())

                # Keep debugging until the debugger stops
                debug.loop()

            finally:
                # Stop the debugger
                debug.stop()
                print "Debugger stopped."

        else:
            print "%s not found." % (args.run[0])

        exit()

    if(args.sysinfo):
        # Create a System object
        # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/system.py#L66
        system = winappdbg.System()

        # Use the built-in WinAppDbg table
        # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1094
        table = winappdbg.Table("\t")

        # New line
        table.addRow("", "")

        # Header
        title = ("System Information", "")
        table.addRow(*title)

        # Add system information
        table.addRow("------------------")
        table.addRow("Bits", system.bits)
        table.addRow("OS", system.os)
        table.addRow("Architecture", system.arch)
        table.addRow("32-bit Emulation", system.wow64)
        table.addRow("Admin", system.is_admin())
        table.addRow("WinAppDbg", winappdbg.version)
        table.addRow("Process Count", system.get_process_count())

        print table.getOutput()

        exit()

    if (args.pid):
        system = winappdbg.System()

        # Get all pids
        pids = system.get_process_ids()

        if args.pid in pids:
            # pid exists

            # Create a Debug object
            debug = winappdbg.Debug()

            try:
                # Attach to pid
                # attach: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/debug.py#L219
                my_process = debug.attach(args.pid)

                print "Attached to %d - %s" % (my_process.get_pid(),
                                               my_process.get_filename())

                # Keep debugging until the debugger stops
                debug.loop()

            finally:
                # Stop the debugger
                debug.stop()
                print "Debugger stopped."

        else:
            print "pid %d not found." % (args.pid)

        exit()

    # If no arguments, print running processes
    system = winappdbg.System()

    # We can reuse example 02 from the docs
    # https://winappdbg.readthedocs.io/en/latest/Instrumentation.html#example-2-enumerating-running-processes
    table = winappdbg.Table("\t")
    table.addRow("", "")

    header = ("pid", "process")
    table.addRow(*header)

    table.addRow("----", "----------")

    processes = {}

    # Add all processes to a dictionary then sort them by pid
    for process in system:
        processes[process.get_pid()] = process.get_filename()

    # Iterate through processes sorted by pid
    for key in sorted(processes.iterkeys()):
        table.addRow(key, processes[key])

    print table.getOutput()


if __name__ == "__main__":
    main()
