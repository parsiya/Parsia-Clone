import winappdbg
import argparse
import winapputil
from winappdbg.win32 import PVOID, DWORD, HANDLE


class DebugEvents(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """

    """
        BOOL HttpSendRequest(
            _In_ HINTERNET hRequest,
            _In_ LPCTSTR   lpszHeaders,
            _In_ DWORD     dwHeadersLength,
            _In_ LPVOID    lpOptional,
            _In_ DWORD     dwOptionalLength
        );

        HINTERNET HttpOpenRequest(
          _In_ HINTERNET hConnect,
          _In_ LPCTSTR   lpszVerb,
          _In_ LPCTSTR   lpszObjectName,
          _In_ LPCTSTR   lpszVersion,
          _In_ LPCTSTR   lpszReferer,
          _In_ LPCTSTR   *lplpszAcceptTypes,
          _In_ DWORD     dwFlags,
          _In_ DWORD_PTR dwContext
        );
    """

    apiHooks = {

        # Hooks for the wininet.dll library - note this is case-sensitive
        "wininet.dll": [

            # Function            Signature
            ("HttpSendRequestW", (HANDLE, PVOID, DWORD, PVOID, DWORD)),
            ("HttpOpenRequestW", (HANDLE, PVOID, PVOID, PVOID, PVOID, PVOID,
                                  DWORD, PVOID)),
        ],
    }

    def pre_HttpSendRequestW(self, event, ra, hRequest, lpszHeaders,
                             dwHeadersLength, lpOptional, dwOptionalLength):

        process = event.get_process()

        if dwHeadersLength != 0:
            mylogger.log_text(winapputil.utils.get_line())
            mylogger.log_text("HttpSendRequestW")

            headers = process.peek_string(lpszHeaders, fUnicode=True)
            mylogger.log_text("Headers %s" % (headers))

        if dwOptionalLength != 0:
            # This is not unicode - see the pointer name dummy (lp vs. lpsz)
            # False by default but a good idea to include it for clarity
            optional = process.peek_string(lpOptional, fUnicode=False)

            mylogger.log_text("Optional %s" % (optional))
            mylogger.log_text(winapputil.utils.get_line())

    def pre_HttpOpenRequestW(self, event, ra, hConnect, lpszVerb,
                             lpszObjectName, lpszVersion, lpszReferer,
                             lplpszAcceptTypes, dwFlags, dwContext):

        process = event.get_process()

        verb = process.peek_string(lpszVerb, fUnicode=True)
        if verb is None:
            verb = "GET"

        obj = process.peek_string(lpszObjectName, fUnicode=True)

        mylogger.log_text(winapputil.utils.get_line())
        mylogger.log_text("HttpOpenRequestW")
        mylogger.log_text("verb: %s" % verb)
        mylogger.log_text("obj : %s" % obj)
        mylogger.log_text(winapputil.utils.get_line())


# ---------------

"""
Debug an app with parameters passed by -run
e.g. python 02-debug2.py c:\windows\system32\notepad.exe c:\textfile.txt
print system info with -i or --sysinfo
print current processes if nothing is passed
attach to a process with --attach-process or -pid
attach to a process using name with -pname or --attach-process-name
log to file with -o or --output
"""


def main():
    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    # Make -r and -pid mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--run", nargs="+",
                       help="path to application followed by parameters")
    group.add_argument("-pid", "--attach-pid", type=int, dest="pid",
                       help="pid of process to attach and instrument")
    group.add_argument("-pname", "--attach-process-name", dest="pname",
                       help="pid of process to attach and instrument")

    parser.add_argument("-i", "--sysinfo", action="store_true",
                        help="print system information")

    # Add optional log file
    parser.add_argument("-o", "--output", dest="output", help="log filename")

    args = parser.parse_args()

    # Setup logging
    # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1766

    global mylogger
    if args.output:
        # verbose=False disables printing to stdout
        mylogger = winappdbg.Logger(args.output, verbose=False)
    else:
        mylogger = winappdbg.Logger()

    # Create an instance of our eventhandler class
    myeventhandler = DebugEvents()

    if (args.run):
        try:
            myutil = winapputil.WinAppUtil(cmd=args.run,
                                           eventhandler=myeventhandler,
                                           logger=mylogger)

            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" %
                              (error.pid_pname, error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.pid:
        try:
            myutil = winapputil.WinAppUtil(pid_pname=args.pid, logger=mylogger,
                                           eventhandler=myeventhandler,
                                           attach=True)
            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" % (error.pid_pname,
                                                       error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.pname:
        try:
            myutil = winapputil.WinAppUtil(pid_pname=args.pname,
                                           logger=mylogger,
                                           eventhandler=myeventhandler,
                                           attach=True)
            debug = myutil.debug()
            debug.loop()

        except winapputil.DebugError as error:
            mylogger.log_text("Exception in %s: %s" % (error.pid_pname,
                                                       error.msg))

        except KeyboardInterrupt:

            debug.stop()
            mylogger.log_text("Killed process")

    elif args.sysinfo:
        myutil = winapputil.WinAppUtil()
        print (myutil.sysinfo())

    else:
        myutil = winapputil.WinAppUtil()
        print (myutil.get_processes())

    pass


if __name__ == "__main__":
    main()
