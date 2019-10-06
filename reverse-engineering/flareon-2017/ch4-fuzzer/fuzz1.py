from winappdbg import Debug, EventHandler, CrashDump, HexDump

import logging, itertools

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    )

LOWER  = 0x20
UPPER  = 0x25
LENGTH = 7
TAIL   = ".exe"


global memory_snapshot, context_snapshot, first_time, filename, all_filenames, index

# converts int payload to hex string - roughly hexlify
def toHex(payload):
    # start of hex has "0x", we do not want that
    return hex(payload)[2:]

# returns a list of all bytes in range of lower-upper with length
# adds ".exe" in the end
def generate_bytes(lower_range, upper_range, length, tail):

    initial_bytes = list(itertools.product(range(lower_range, upper_range), repeat=length))

    all_bytes  = []
    tail_bytes = '00'.join(c.encode("hex") for c in tail)

    for my_byte in initial_bytes:
        all_bytes.append(("00".join(str(x) for x in my_byte)) + tail_bytes)

    return all_bytes


# takes a memory snapshot of the process and returns it
def get_memory(event):
    myProcess = event.get_process()

    myProcess.suspend()

    # take_memory_snapshot: https://github.com/MarioVilas/winappdbg/blob/6704b334a46e3f53003bcdb9efd6bfd551a2f527/winappdbg/process.py#L3261
    memory = myProcess.take_memory_snapshot()
    myProcess.resume()
    return memory


# restores the memory snapshot of the process
def set_memory(event, memory):
    myProcess = event.get_process()

    myProcess.suspend()

    # restore_memory_snapshot: https://github.com/MarioVilas/winappdbg/blob/6704b334a46e3f53003bcdb9efd6bfd551a2f527/winappdbg/process.py#L3301
    # bSkipMappedFiles: https://github.com/MarioVilas/winappdbg/blob/6704b334a46e3f53003bcdb9efd6bfd551a2f527/winappdbg/process.py#L3317
    myProcess.restore_memory_snapshot(memory, bSkipMappedFiles=True)

    myProcess.resume()

# set a breakpoint at an address and set the callback function
# this means we need to create a function with the same name
def set_breakpoint(debug, address, callback_function):
    # since we are only debugging one process, we do not care
    # alternatively we can pass the pid to this function as a parameter and use it
    pid = debug.get_debugee_pids()[0]

    # try making a label

    # break_at: https://github.com/MarioVilas/winappdbg/blob/6704b334a46e3f53003bcdb9efd6bfd551a2f527/winappdbg/breakpoint.py#L3905
    # see also: http://winappdbg.readthedocs.io/en/latest/Debugging.html?highlight=break_at#example-11-setting-a-breakpoint
    debug.break_at(pid, address, action=callback_function)


def breakpoint_010153F6(event):

    """
    .rsrc:010153F0 mov     ecx, [ebp+var_C]
    .rsrc:010153F3 mov     edx, [ecx+28h]
    .rsrc:010153F6 push    edx   <------ we are here
    .rsrc:010153F7 call    sub_1015270
    .rsrc:010153FC cmp     eax, [ebp+arg_0]
    .rsrc:010153FF jnz     short loc_101540B
    """

    global memory_snapshot, context_snapshot, first_time, filename, all_filenames, index

    thread = event.get_thread()
    
    # get_context: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/thread.py#L469
    context = thread.get_context()
    
    if first_time:
        logging.debug("First time - taking context and memory snapshots")
        context_snapshot = context
        memory_snapshot  = get_memory(event)
        first_time       = False

    # HexDump: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/textio.py#L451

    # logging.debug(HexDump.address(context["Edx"]))

    edx = context["Edx"]

    filename = all_filenames[index]

    # logging.debug("-" * 79)
    # logging.debug("filename: " + filename.decode("hex"))
    # logging.debug("index: " + str(index))

    # write the filename to [edx]
    # make sure we are not overwriting other parts of memory
    # as a result we need to run the app with a large filename to have a good sized buffer here

    event.get_process().write(edx, filename)

    # or we could have made a breakpoint at the function
    # read the top DWORD (32-bits) and write at the location it points to
  

    # set the application to the new context (e.g. change edx and jump to the next instruction)

    # logging.debug(event.get_process().read(0x40107C, 0x79))

    # logging.debug(HexDump.address(newContext["Eip"]))
    # logging.debug(HexDump.address(newContext["Edx"]))

def breakpoint_010153FF(event):

    """
    .rsrc:010153F0 mov     ecx, [ebp+var_C]
    .rsrc:010153F3 mov     edx, [ecx+28h]
    .rsrc:010153F6 push    edx
    .rsrc:010153F7 call    sub_1015270
    .rsrc:010153FC cmp     eax, [ebp+arg_0]
    .rsrc:010153FF jnz     short loc_101540B   <------ we are here
    """

    global memory_snapshot, context_snapshot, first_time, filename, all_filenames, index

    thread = event.get_thread()
    context = thread.get_context()

    # logging.debug("-" * 79)
    logging.debug("filename: " + filename.decode("hex"))
    logging.debug("eax: " + HexDump.address(context["Eax"]))

    if context["Eax"] == 0x8FECD63F:

        logging.debug("-" * 79)
        logging.debug("filename: " + filename.decode("hex"))
        logging.debug("eax: " + HexDump.address(context["Eax"]))


    index += 1

    if (index == len(all_filenames)):
        logging.debug("-" * 79)
        logging.debug("Reached the end of the address space")
        event.debug.stop()
        return

    # restore everything - need to wait and see if this is 
    set_memory(event, memory_snapshot)
    thread.set_context(context_snapshot)

    # we need to write the memory_blob with the original because restore memory does not cover that
    # most likely due to skipping the memory mapped files

    # no idea why the restore context thing does not work
    # but this will send us back to top and hopefully that breakpoint will be triggered again
    thread.set_pc(0x010153F6)


def simple_debugger(argv):

    # Instance a Debug object using the "with" statement.
    # Note how we don't need to call "debug.stop()" anymore.
    with Debug(None, bKillOnExit = True) as debug:

        try:
            # Start a new process for debugging.
            debug.execv(argv)

            set_breakpoint(debug, 0x010153F6, breakpoint_010153F6)

            # set_breakpoint(debug, 0x40103B, breakpoint_40103B)

            set_breakpoint(debug, 0x010153FF, breakpoint_010153FF)

            # Wait for the debugee to finish.
            debug.loop()

        except KeyboardInterrupt:
            logging.debug("Ctrl+C -ed.")

            # Stop debugging. This kills all debugged processes.
            debug.stop()

        # Stop the debugger.
        finally:
            debug.stop()

         
def main():

    global memory_snapshot, context_snapshot, first_time, filename, all_filenames, index
    first_time = True
    index = 0

    all_filenames = generate_bytes(LOWER, UPPER, LENGTH, TAIL)

    logging.debug("Starting simple_debugger")

    simple_debugger(["notepad.exe"])


if __name__ == "__main__":
    main()