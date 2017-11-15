import winappdbg
import argparse
import winapputil
from winappdbg.win32 import PVOID, DWORD, HANDLE


class DebugEvents(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """

    # Better hooking
    # https://winappdbg.readthedocs.io/en/latest/Debugging.html#example-9-intercepting-api-calls

    """
    HINTERNET InternetConnect(
      _In_ HINTERNET     hInternet,
      _In_ LPCTSTR       lpszServerName,
      _In_ INTERNET_PORT nServerPort,
      _In_ LPCTSTR       lpszUsername,
      _In_ LPCTSTR       lpszPassword,
      _In_ DWORD         dwService,
      _In_ DWORD         dwFlags,
      _In_ DWORD_PTR     dwContext
    );
    """

    apiHooks = {

        # Hooks for the wininet.dll library
        "wininet.dll": [

            # InternetConnectW
            # https://msdn.microsoft.com/en-us/library/windows/desktop/aa384363(v=vs.85).aspx
            # ("InternetConnectW", (HANDLE, PVOID, WORD, PVOID, PVOID, DWORD, DWORD, PVOID)),
            ("InternetConnectW", 8),

        ],
    }

    # Now we can simply define a method for each hooked API.
    # Methods beginning with "pre_" are called when entering the API,
    # and methods beginning with "post_" when returning from the API.

    def pre_InternetConnectW(self, event, ra, hInternet, lpszServerName,
                             nServerPort, lpszUsername, lpszPassword,
                             dwService, dwFlags, dwContext):

        process = event.get_process()
        process.suspend()
        thread = event.get_thread()

        server_name = process.peek_string(lpszServerName, fUnicode=True)

        if server_name == "example.com":

            # mylogger.log_text(server_name)

            # Encoding as UTF16
            new_server_name = "synopsys.com".encode("utf-16le")

            # Get length of new payload
            payload_length = len(new_server_name)

            # Allocate memory in target process and get a pointer
            new_payload_addr = event.get_process().malloc(payload_length)

            # Write the new payload to that pointer
            process.write(new_payload_addr, new_server_name)

            top_of_stack = thread.get_sp()

            bits = thread.get_bits()
            emulation = thread.is_wow64()

            if bits == 32 or emulation is True:

                # Write the pointer to the new payload with the old one
                process.write_dword(top_of_stack + 8, new_payload_addr)

            elif bits == 64:
                thread.set_register("Rdx", new_payload_addr)

        process.resume()


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
