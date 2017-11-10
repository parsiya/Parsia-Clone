import winappdbg
import argparse
from winappdbg import win32

# Debug an app with arguments passed by -r
# e.g. python 02-RunWithArgs.py -r c:\windows\system32\notepad.exe c:\textfile.txt


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    parser.add_argument("-r", "--run", nargs="+",
                        help="path to application followed by parameters")

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
                # Debug the app
                # Debug.execv([args.app])
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

if __name__ == "__main__":
    main()
