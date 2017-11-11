import winappdbg
import argparse
import winapputil
from winappdbg.win32 import PVOID, DWORD, HANDLE


class DebugEvents(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """

    def load_dll(self, event):
        module = event.get_module()

        if module.match_name("kernel32.dll"):

            # Resolve function addresses
            address_CreateFileA = module.resolve("CreateFileA")
            address_CreateFileW = module.resolve("CreateFileW")

            # Types are here
            # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/win32/defines.py#L380
            sig_CreateFileA = (PVOID, DWORD, DWORD, PVOID, DWORD, DWORD, HANDLE)
            sig_CreateFileW = (PVOID, DWORD, DWORD, PVOID, DWORD, DWORD, HANDLE)

            pid = event.get_pid()

            # Hook function(pid, address, preCB, postCB, paramCount, signature)
            # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/breakpoint.py#L3969
            event.debug.hook_function(pid, address_CreateFileA,
                                      preCB=pre_CreateFileA,
                                      postCB=post_CreateFileA,
                                      signature=sig_CreateFileA)

            event.debug.hook_function(pid, address_CreateFileW,
                                      preCB=pre_CreateFileW,
                                      postCB=post_CreateFileW,
                                      signature=sig_CreateFileW)

            # Another way of setting up hooks without signature

            """
            event.debug.hook_function(pid, address_CreateFileA,
                                      preCB=pre_CreateFileA,
                                      postCB=post_CreateFileA,
                                      paramCount=7)

            event.debug.hook_function(pid, address_CreateFileW,
                                      preCB=pre_CreateFileW,
                                      postCB=post_CreateFileW,
                                      paramCount=7)
            """

# Callback functions
# -------------------

# Callback function parameters are always
# (event, ra (return address), then function parameters)
# self is first if part of the eventhandler class


def pre_CreateFileW(event, ra, lpFileName, dwDesiredAccess, dwShareMode,
                    lpSecurityAttributes, dwCreationDisposition,
                    dwFlagsAndAttributes, hTemplateFile):

    """
    This will be called as soon as we enter the function and before the
    function stack frame is created.
    """

    process = event.get_process()

    # Suspend the process because why not
    process.suspend()

    mylogger.log_text("Hit kernel32!CreateFileW")

    # 32-bit so all parameters are on stack

    # In case you want a pointer to the top of the stack
    # thread = event.get_thread()

    # All memory read stuff are at
    # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L125

    # fUnicode=True because we are in the Wide or Unicode version of the API
    myFileName = process.peek_string(lpFileName, fUnicode=True)

    mylogger.log_text("lpFilename: %s" % (myFileName))

    # Resume the process
    process.resume()


def pre_CreateFileA(event, ra, lpFileName, dwDesiredAccess, dwShareMode,
                    lpSecurityAttributes, dwCreationDisposition,
                    dwFlagsAndAttributes, hTemplateFile):

    process = event.get_process()

    # Suspend the process because why not
    process.suspend()

    mylogger.log_text("Hit kernel32!CreateFileA")

    # fUnicode=False because we are in the ANSI version
    myFileName = process.peek_string(lpFileName, fUnicode=False)

    mylogger.log_text("lpFilename: %s" % (myFileName))

    process.resume()


def post_CreateFileW(event, retval):

    mylogger.log_text("Leaving kernel32!CreateFileW")
    mylogger.log_text("Return value: %x" % (retval))


def post_CreateFileA(event, retval):

    mylogger.log_text("Leaving kernel32!CreateFileA")
    mylogger.log_text("Return value: %x" % (retval))

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
