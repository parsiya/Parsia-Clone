import winappdbg
import threading
import time
import winapputil

global key, memory_snapshot, context_snapshot, first_time, memory_blob

mylogger = winappdbg.Logger()


# Takes a memory snapshot of the process and returns it
def get_memory(event):
    myProcess = event.get_process()
    myProcess.suspend()

    # take_memory_snapshot: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3261
    memory = myProcess.take_memory_snapshot()
    myProcess.resume()
    return memory


# Restores the memory snapshot of the process
def set_memory(event, memory):
    myProcess = event.get_process()
    myProcess.suspend()

    # restore_memory_snapshot: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3301
    # bSkipMappedFiles: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/process.py#L3317
    myProcess.restore_memory_snapshot(memory, bSkipMappedFiles=True)

    myProcess.resume()


# Set a breakpoint at an address and set the callback function
def set_breakpoint(debug, address, callback_function):
    # Since we are only debugging one process, we do not care
    # Alternatively we can pass the pid to this function as a parameter and use it
    pid = debug.get_debugee_pids()[0]

    # break_at: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/breakpoint.py#L3905
    # see also: https://winappdbg.readthedocs.io/en/latest/Debugging.html?highlight=break_at#example-11-setting-a-breakpoint
    debug.break_at(pid, address, action=callback_function)


# Breakpoint at 0x401036
def breakpoint_401036(event):

    global key, memory_blob, context_snapshot, memory_snapshot, first_time

    if (key >= 0x100):
        mylogger.log_text(str("Reached " + hex(key)))
        event.debug.stop()
        return

    thread = event.get_thread()

    # get_context: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/thread.py#L469
    context = thread.get_context()

    # If we have not started bruteforcing yet
    if first_time:
        # Read the memory blob that is being bruteforced
        memory_blob = event.get_process().read(0x40107C, 0x79)

        # Store the current context
        context_snapshot = context

        # Store a snapshot of memory
        memory_snapshot = get_memory(event)

        # Done
        first_time = False

    context["Edx"] = key

    key += 1

    # Set the application to the new context (e.g. change edx and jump to the next instruction)

    # set_context: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/thread.py#L570
    thread.set_context(context)
    thread.set_pc(0x401039)


def breakpoint_40105B(event):

    global key, memory_blob, context_snapshot, memory_snapshot, first_time

    thread = event.get_thread()
    context = thread.get_context()

    if context["Eax"] == 0xFB5E:

        logstring = ("\n%s\nKey: %s\nEax: %s" %
                     (("-" * 79), hex(key-1),
                      winappdbg.HexDump.address(context["Eax"])))

        mylogger.log_text(logstring)

    # Restore everything
    set_memory(event, memory_snapshot)
    thread.set_context(context_snapshot)

    # We need to write the memory_blob with the original because
    # restore memory skipps memory mapped locations
    event.get_process().write(0x40107C, memory_blob)

    # Go to top so the first breakpoint will be triggered again
    thread.set_pc(0x401036)


def simple_debugger(argv):

    myutil = winapputil.WinAppUtil(cmd=argv)

    debug = myutil.debug()

    set_breakpoint(debug, 0x401036, breakpoint_401036)

    set_breakpoint(debug, 0x40105B, breakpoint_40105B)

    # Wait for the debugee to finish.
    debug.loop()


def send_me(payload):
    """
    Connect to port 2222 and send something.
    This will start the process
    """
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 2222))

    mylogger.log_text("Socket connected")

    s.send(hex(payload))
    logmsg = "Sent %s" % (payload)
    mylogger.log_text(logmsg)

    data = s.recv(2048)
    s.close()


def main():

    global key
    key = 0x00

    global memory_snapshot, context_snapshot, first_time
    first_time = True

    mylogger.log_text("Starting simple_debugger")

    debugger = threading.Thread(name="Debugger", target=simple_debugger,
                                args=(["greek_to_me.exe"], ))
    debugger.start()

    mylogger.log_text("Started simple_debugger. Sleeping for 2 seconds.")

    time.sleep(2)

    mylogger.log_text("Starting send_me.")

    sendMe = threading.Thread(name="Send Me", target=send_me, args=(key, ))
    sendMe.start()

    sendMe.join()
    debugger.join()


if __name__ == "__main__":
    main()
