# App logic
from __future__ import print_function
import os
from . import keys
from . import readchar
from . import command
from . import renderer
from .filter import filter_commands

from sys import version_info, platform

if version_info[0] == 2:
    keyboard_input = raw_input
else:
    keyboard_input = input

def get_os():
    if platform.lower() == 'darwin':
        return 'osx'
    elif platform.lower().startswith('linux'):
        return 'linux'
    else:
        # throw is better
        return 'unknown'

def get_user_marks_path():
    return os.path.join(os.getenv('MARKER_DATA_HOME'), 'user_commands.txt')
def get_tldr_os_marks_path():
    return os.path.join(os.getenv('MARKER_HOME'), 'tldr', get_os()+'.txt')
def get_tldr_common_marks_path():
    return os.path.join(os.getenv('MARKER_HOME'), 'tldr', 'common.txt')


def mark_command(cmd_string, alias):
    ''' Adding a new Mark '''
    if cmd_string:
        cmd_string = cmd_string.strip()
    if not cmd_string:
        cmd_string = keyboard_input("Command:")
    else:
        print("command: %s" % cmd_string)
    if not cmd_string:
        print ("command field is required")
        return
    if not alias:
        alias = keyboard_input("Alias?:")
    else:
        print("alias: %s" % alias)
    if '##' in cmd_string or '##' in alias:
        # ## isn't allowed since it's used as seperator
        print ("command can't contain ##(it's used as command alias seperator)")
        return        
    commands = command.load(get_user_marks_path())
    command.add(commands, command.Command(cmd_string, alias))
    command.save(commands, get_user_marks_path())

def get_selected_command_or_input(search):
    ''' Display an interactive UI interface where the user can type and select commands
        this function returns the selected command if there is matches or the written characters in the prompt line if no matches are present
    '''
    commands = command.load(get_user_marks_path()) + command.load(get_tldr_os_marks_path()) + command.load(get_tldr_common_marks_path())
    state = State(commands, search)
    # draw the screen (prompt + matchd marks)
    renderer.refresh(state)
    # wait for user input(returns selected mark)
    output = read_line(state)
    # clear the screen
    renderer.erase()
    if not output:
        return state.input
    return output.cmd


def remove_command(search):
    ''' Remove a command interactively '''
    commands = command.load(get_user_marks_path())
    state = State(commands, search)
    renderer.refresh(state)
    selected_mark = read_line(state)
    if selected_mark:
        command.remove(commands, selected_mark)
        command.save(commands, get_user_marks_path())
    # clear the screen
    renderer.erase()
    return selected_mark

def read_line(state):
    ''' parse user input '''
    output = None
    while True:
        c = readchar.get_symbol()
        if c == keys.ENTER:
            if state.get_matches():
                output = state.get_selected_match()
            break
        elif c == keys.CTRL_C or c == keys.ESC:
            state.reset_input()
            break
        elif c == keys.CTRL_U:
            state.clear_input()
        elif c == keys.BACKSPACE:
            state.set_input(state.input[0:-1])
        elif c == keys.UP:
            state.select_previous()
        elif c == keys.DOWN or c == keys.TAB:
            state.select_next()
        elif c <= 126 and c >= 32:
            state.set_input(state.input + chr(c))
        renderer.refresh(state)
    return output

class State(object):
    ''' The app State, including user written characters, matched commands, and selected one '''

    def __init__(self, bookmarks, default_input):
        self.bookmarks = bookmarks
        self._selected_command_index = 0
        self.matches = []
        self.default_input = default_input
        self.set_input(default_input)

    def get_matches(self):
        return self.matches

    def reset_input(self):
        self.input = self.default_input

    def set_input(self, input):
        self.input = input if input else ""
        self._update()

    def clear_input(self):
        self.set_input("")

    def clear_selection(self):
        self._selected_command_index = 0

    def select_next(self):
        self._selected_command_index = (self._selected_command_index + 1) % len(self.matches) if len(self.matches) else 0

    def select_previous(self):
        self._selected_command_index = (self._selected_command_index - 1) % len(self.matches) if len(self.matches) else 0

    def _update(self):
        self.matches = filter_commands(self.bookmarks, self.input)
        self._selected_command_index = 0

    def get_selected_match(self):
        if len(self.matches):
            return self.matches[self._selected_command_index]
        else:
            raise 'No matches found'
