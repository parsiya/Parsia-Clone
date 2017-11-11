import winappdbg
import argparse
import winapputil


class DebugEvents(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """

    def create_process(self, event):
        process  = event.get_process()
        pid      = event.get_pid()
        # pid    = process.get_pid()
        filename = process.get_filename()

        mylogger.log_text("CreateProcess %d - %s" % (pid, filename))

    def exit_process(self, event):
        process  = event.get_process()
        pid      = event.get_pid()
        # pid    = process.get_pid()
        filename = process.get_filename()

        mylogger.log_text("ExitProcess %d - %s" % (pid, filename))

    def create_thread(self, event):
        process  = event.get_process()
        thread   = event.get_thread()

        tid  = thread.get_tid()
        name = thread.get_name()

        mylogger.log_text("CreateThread %d - %s" % (tid, name))

    def exit_thread(self, event):
        process  = event.get_process()
        thread   = event.get_thread()

        tid  = thread.get_tid()
        name = thread.get_name()

        mylogger.log_text("ExitThread %d - %s" % (tid, name))


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
