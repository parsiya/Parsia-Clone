# from winappdbg import Debug, System, version, Table

import winappdbg
from winappdbg import win32

"""
WinAppUtils is a set of helper functions for WinAppDbg.
WinAppDbg is created by Mario Vilas @mario_vilas.
URL: https://github.com/MarioVilas/winappdbg
"""


# Exceptions class(es)
class MyError(Exception):
    """Base class for exceptions in this module."""
    pass


class DebugError(MyError):
    """
    Exception raised when attempting to debug an application.

    Attributes:
        pid_pname -- process id or process name
        msg       -- error message
    TODO: replace with group stuff
    """

    def __init__(self, pid_pname, msg):
        self.pid_pname = pid_pname
        self.msg = msg

# -------------------


class WinAppUtil(object):
    """
    Main class for WinAppUtil.
    Contains most of the helper functions and utilities.

    TODO: group stuff
    """

    def __init__(self, cmd=None, logger=None, pid_pname=None,
                 eventhandler=None, attach=False, kill_on_exit=True):
        """
        Create a WinAppUtil object.

        @type  pid_pname: str or int
        @param pid_pname: (Optional) Process id or process name to debug.
            Only used if attach is True.
            If int, debugger will try to attach to pid.
            If str, debugger will search for running processes with that name
            and try to attach to them.

        @type  cmd: list of str
        @param cmd: (Optional) Contains command line to execute or attach.
            If attach is False, first item contains the application name
            and path if any. The rest contain command line parameters to pass
            to the newly started application.
            If attach is True, first item of the list must contain the pid or
            process name of the application to attach to.

        @type  logger: winappdbg.logger
        @param logger: (Optional) An instance of WinAppDbg logger.
            The winappdbg.logger can be used as follows:
                logger = winappdbg.Logger(filename, verbose)
                filename if provided will be the location of the log file.
                If verbose is True, logs will also be printed to stdout.
                If no arguments are provided, logs will be printed to stdout.

            for example:
                logger = winappdbg.Logger("mylog.txt") or
                logger = winappdbg.Logger("mylog.txt", verbose=True)
                Logs will be stored in "mylog.txt" AND printed to stdout.

                logger = winappdbg.Logger("mylog.txt", verbose=False)
                Logs will only be stored in the file.

                logger = winappdbg.Logger()
                Logs will be printed to stdout.
        More info:
        https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L1766

        @type  eventhandler: winappdbg.eventhandler
        param  eventhandler: (Optional) An instance of a EventHandler class.
            This way we can customize our own eventhandler without having to
            write a lot of code to do it in the class.

        @type  attach: bool
        @type  attach: (Optional) Attach or start a new process.
            If True,  try to attach to the pid or pname.
            If False, start a new process.

        @type  kill_on_exit: bool
        @param kill_on_exit: (Optional) Kill the process when debugger exits.
            We generally just pass this to bkillOnExit in WinAppDbg.

        @rtype:  winapputil.WinAppUtil
        @return: Returns an instance of WinAppUtil.
        """

        self.cmdline      = cmd
        self.logger       = logger
        self.eventhandler = eventhandler
        self.attach       = attach
        self.kill_on_exit = kill_on_exit
        self.pid_pname    = pid_pname

        if attach is False and cmd is not None:
            self.pid_pname = cmd[0]

    def sysinfo(self):
        """
        Returns information about the system.
        @rtype:  str
        @return: A table populated with system information.
        """

        # Create a System object
        # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/system.py#L66
        system = winappdbg.System()

        # Use the built-in Table
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

        return table.getOutput()

    def get_processes(self):
        """
        Returns a table of all running processes with their pid and
        filename.

        @rtype:  str
        @return: A table listing all running processes.
        """

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

        return table.getOutput()

    def get_process_handle(pid):
        """
        Returns a handle to the process with pid.

        @type  pid: int
        @param pid: ID of the target process.

        @rtype:  winappdbg.process
        @return: A handle to the process associated with pid.
        """

        system = winappdbg.System()

        if system.has_process(pid):
            return system.get_process(pid)
        else:
            raise DebugError(pid, "Process not found")

    def debug(self):
        """
        Starts a new process or attaches to a running process.

        @rtype:  winappdbg.Debug
        @return: WinAppDbg Debug object that can be used to interact with the
                 application.
        """

        if self.attach is True:
            if self.logger is not None:
                self.logger.log_text(
                        "Attaching to %s" % (str(self.pid_pname)))

            return self.__attach()

        else:
            if self.logger is not None:
                self.logger.log_text("Starting %s" % (" ".join(self.cmdline)))

            return self.__start()

    def __attach(self):
        """
        Attaches to a process based on pid or process name.

        @rtype:  winappdbg.Debug
        @return: WinAppDbg Debug object that can be used to interact with the
                 application.
        """

        debugger = winappdbg.Debug(self.eventhandler,
                                   bKillOnExit=self.kill_on_exit)

        if type(self.pid_pname) is int:

            # Get all running pids
            pids = debugger.system.get_process_ids()

            if self.pid_pname in pids:

                # pid exists then attach to the pid
                # attach:
                # https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/debug.py#L219
                debugger.attach(self.pid_pname)

                return debugger

            else:
                raise DebugError(self.pid_pname, "pid not found")

        elif type(self.pid_pname) is str:

            # Example 3:
            # https://winappdbg.readthedocs.io/en/latest/_downloads/03_find_and_attach.py
            debugger.system.scan()

            # Search for all processes with that name
            rslt = debugger.system.find_processes_by_filename(self.pid_pname)

            if len(rslt) is not 0:

                # Process found
                # Attach to all processes
                for (process, name) in rslt:
                    debugger.attach(process.get_pid())

                return debugger

            else:

                # Process not found
                raise DebugError(self.pid_pname, "Process not found")

        else:
            # pid_pname is neither int nor str
            raise DebugError(self.pid_pname, "Invalid parameter passed")

    def __start(self):
        """
        Start and debug a program with (or without) parameters

        @rtype:  winappdbg.Debug
        @return: WinAppDbg Debug object that can be used to interact with the
                 application.

        @raise DebugError: Raises an exception on error.
            File was not found.
        """

        # First check if file exists (in case we have passed a full path)
        # If we cannot find the full path, search in %PATH%
        if win32.PathFileExists(self.pid_pname) is False:

            try:
                # Search for file using win32.SearchPath
                # If file does not exist, then an exception is raised
                # Works: win32.SearchPath(None, "notepad.exe", ".exe")
                # Works: win32.SearchPath(None, "notepad.exe", None)
                # Doesn't work: win32.SearchPath(None, "notepad", None)
                _, _ = win32.SearchPath(None, self.pid_pname, ".exe")

            # An exception will be raised if file was not found
            except WindowsError, e:
                raise DebugError(self.pid_pname, e)

        # Either fullpath is passed or file exists in %PATH%
        # In both cases we can just pass it to execv
        debugger = winappdbg.Debug(self.eventhandler,
                                   bKillOnExit=self.kill_on_exit)

        debugger.execv(self.cmdline, bFollow=True)

        return debugger
