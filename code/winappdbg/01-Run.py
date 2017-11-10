import winappdbg
import argparse
from winappdbg import win32

# Debug an app passed by -r
# e.g. python 01-debug1.py -r c:\windows\system32\notepad.exe


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    parser.add_argument("-r", "--run", help="path to application")

    args = parser.parse_args()

    # Use Win32 API functions provided by WinAppDbg
    if win32.PathFileExists(args.run) is True:
        # File exists

        # Create a Debug object
        debug = winappdbg.Debug()

        try:
            # Debug the app
            # First item is program and the rest are arguments
            # execv: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/debug.py#L274
            my_process = debug.execv([args.run])

            print "Attached to %d - %s" % (my_process.get_pid(),
                                           my_process.get_filename())

            # Keep debugging until the debugger stops
            debug.loop()

        finally:
            # Stop the debugger
            debug.stop()
            print "Debugger stopped."

    else:
        print "%s not found." % (args.run)


if __name__ == "__main__":
    main()
