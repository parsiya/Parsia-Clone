

"""
Utils file contains the helper functions for winapputil.
"""


def to_hex(payload):
    """
    Converts an int or long to hex but removes the "0x" at the start.

    @rtype:  str
    @return: A string representing the number in hex without "0x".
    """
    return hex(payload)[2:]


def get_line():
    """
    Returns a horizontal line.

    @rtype:  str
    @return: A string containing 79 dashes ("-").
        79 is supposed to look old school cool.
    """
    return "-" * 79
