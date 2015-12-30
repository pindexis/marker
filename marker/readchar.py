import sys
import tty
import termios
import fcntl
import os
from . import keys

def get_symbol():
    ''' Read a symbol, which can be a single byte character or a multibyte string'''
    ch = read_char()
    ch_code = ord(ch)
    # check for multibyte string
    if ch_code == keys.ESC:
        ch = read_char_no_blocking()
        if ch == '':
            # ESC key pressed
            return keys.ESC
        elif ch != 'O' and ch != '[':
            return ord(ch)
        else:
            ch = read_char_no_blocking()
            if ch == 'A':
                return keys.UP
            elif ch == 'B':
                return keys.DOWN
            elif ch == 'C':
                return keys.RIGHT
            elif ch == 'D':
                return keys.LEFT
    return ch_code


def read_char():
    ''' Read a character '''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd, termios.TCSADRAIN)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def read_char_no_blocking():
    ''' Read a character in nonblocking mode, if no characters are present in the buffer, return an empty string '''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    try:
        tty.setraw(fd, termios.TCSADRAIN)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
        return sys.stdin.read(1)
    except IOError as e:
        ErrorNumber = e[0]
        # IOError with ErrorNumber 11(35 in Mac)  is thrown when there is nothing to read(Resource temporarily unavailable)
        if (sys.platform.startswith("linux") and ErrorNumber != 11) or (sys.platform == "darwin" and ErrorNumber != 35):
            raise
        return ""
    finally:
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
