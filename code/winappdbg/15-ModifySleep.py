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
    VOID WINAPI Sleep(
        _In_ DWORD dwMilliseconds
    );
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms686298(v=vs.85).aspx
    """

    apiHooks = {

        # Hooks for the kernel32.dll library
        "kernel32.dll": [

            # Note how are passing only one parameter
            ("Sleep", (DWORD, )),

            # We can also pass the number of arguments instead of signature
            # ("Sleep", 1),
        ],
    }

    def pre_Sleep(self, event, ra, dwMilliseconds):

        process = event.get_process()
        process.suspend()

        thread = event.get_thread()

        bits = thread.get_bits()
        emulation = thread.is_wow64()

        logstring = "Original dwMilliseconds %d" % dwMilliseconds

        mylogger.log_text(logstring)

        # If running on a 32-bit machine or 32-bit process on 64-bit machine
        if bits == 32 or emulation is True:
            top_of_stack = thread.get_sp()

            # return_address, dwMilliseconds = thread.read_stack_dwords(2)
            # logstring = "Return Address %s" % \
            #     winappdbg.HexDump.address(return_address, bits)

            # mylogger.log_text(logstring)

            process.write_dword(top_of_stack+((bits/8)*1), 10000)

        # AMD64 calling convention on Windows uses fastcall
        # rcx, rdx, r8, r9 then stack

        elif bits == 64:
            thread.set_register("Rcx", 10000)

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
