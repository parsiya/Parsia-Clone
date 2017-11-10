import winappdbg
import argparse
from winappdbg import win32

# Debug an app with parameters passed by -run
# e.g. python 02-debug2.py c:\windows\system32\notepad.exe c:\textfile.txt
# Print system info with --sysinfo


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    parser.add_argument("-r", "--run", nargs="+",
                        help="path to application followed by parameters")
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

                # kKep debugging until the debugger stops
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


if __name__ == "__main__":
    main()
