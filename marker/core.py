from __future__ import print_function
import os
import math
import difflib
import re
from . import keys
from . import ui
from . import readchar

from sys import version_info
if version_info[0] == 2:
    keyboard_input = raw_input
else:
    keyboard_input = input


def mark_command(command, alias):
    ''' Adding a new Mark '''
    command = command.strip()
    if not command:
        command = keyboard_input("Command:")
    else:
        print("command: %s" % command)
    if not command:
        print ("command field is required")
        return
    if not alias:
        alias = keyboard_input("Alias?:")
    else:
        print("alias: %s" % alias)
    if '##' in command or '##' in alias:
        # ## isn't allowed since it's used as seperator
        print ("command can't contain ##(it's used as command alias seperator)")
        return        
    with FileBookmarks() as bookmarks:
        bookmarks.add_mark(Mark(command, alias))


def get_matched_commands(search_string):
    ''' get commands that match a given search string '''
    with FileBookmarks() as bookmarks:
        state = State(bookmarks, search_string)
        return [m.cmd for m in state.get_matches()]


def get_selected_command_or_input(search):
    ''' Display an interactive UI interface where the user can type and select commands
        this function returns the selected command if there is matches or the written characters in the prompt line if no matches are present
    '''
    with FileBookmarks() as bookmarks:
        state = State(bookmarks, search)
        display = Display()
        # draw the screen (prompt + matchd marks)
        display.refresh(state)
        # wait for user input(returns selected mark)
        output = read_line(state, display)
        # clear the screen
        display.erase()
        if not output:
            return state.input
        return output.cmd


def remove_command(search):
    ''' Remove a command interactively '''
    with FileBookmarks() as bookmarks:
        state = State(bookmarks, search)
        display = Display()
        display.refresh(state)
        selected_mark = read_line(state, display)
        if selected_mark:
            bookmarks.remove_mark(selected_mark)
        # clear the screen
        display.erase()
        return selected_mark


def read_line(state, display):
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
        elif c <= 256 and c >=0:
            state.set_input(state.input + chr(c))
        display.refresh(state)
    return output


class State(object):
    ''' The Current User state, including user written characters, matched commands, and selected one '''

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
        self.matches = self.bookmarks.get_matches(self.input)
        self._selected_command_index = 0

    def get_selected_match(self):
        if len(self.matches):
            return self.matches[self._selected_command_index]
        else:
            raise 'No matches found'


class Display():
    '''Command line user interface'''

    def __init__(self):
        pass

    def _get_terminal_columns(self):
        ''' get the number of terminal columns, used to determine spanned lines of a mark(required for cursor placement) '''
        _, columns = os.popen('stty size', 'r').read().split()
        return int(columns)

    def erase(self):
        ''' the commandline cursor is always at the first line (Marker prompt)
        Therefore, erasing the current and following lines clear all marker output
        '''
        ui.move_cursor_line_beggining()
        ui.erase_from_cursor_to_end()

    def refresh(self, state):
        ''' Redraw the output, this function will be triggered on every user interaction(key pressed)'''
        self.erase()
        lines, num_rows = self._construct_output(state)
        for line in lines:
            print(line)
        # go up
        ui.move_cursor_previous_lines(num_rows)
        # palce the cursor at the end of first line
        ui.move_cursor_horizental(len(lines[0])+1)
        ui.flush()

    def _construct_output(self, state):
        columns = self._get_terminal_columns()
        def number_of_rows(line):
            return int(math.ceil(float(len(line))/columns))
        displayed_lines = []
        # Number of terminal rows spanned by the output, used to determine how many lines we need to go up(to place the cursor after the prompt) after displaying the output
        num_rows = 0
        prompt_line = 'search for: ' + state.input
        displayed_lines.append(prompt_line)
        num_rows += number_of_rows(prompt_line)
        matches = state.get_matches()
        if matches:
            # display commands from Max(0,selected_command_index - 10 +1 ) to Max(10,SelectedCommandIndex + 1)
            selected_command_index = matches.index(state.get_selected_match())
            matches_to_display = matches[max(0, selected_command_index - 10 + 1):max(10, selected_command_index + 1)]
            for index, m in enumerate(matches_to_display):
                fm = ' '+str(m)
                num_rows += number_of_rows(fm)
                # Formatting text(make searched word bold)
                for w in state.input.split(' '):
                    if w:
                        fm = fm.replace(w, ui.bold_text(w))
                # highlighting selected command
                if m == state.get_selected_match():
                    fm = ui.select_text(fm)
                displayed_lines.append(fm)
        else:
            not_found_line = 'Nothing found'
            displayed_lines.append(not_found_line)
            num_rows += number_of_rows(not_found_line)
        return displayed_lines, num_rows


class Bookmarks(object):
    ''' holder of user bookrmarks '''

    def __init__(self, marks_list):
        self.marks = marks_list
        # boolean representing whether a change to the bookmarks has been made, used to identify whether writing to the bookmarks file is needed
        self.dirty = False

    def get_matches(self, search_string):
        ''' return the list of marks that match a given search string
         A mark is considered a match if:
           - all words in the search string except the last one must have exact match, meaning they are present in either the command or the alias
           - for the last word, it can be contained in any word in the command or alias
         For example: 'cd tonowhere' will match 'c','cd n' but not 'c ', 'c t'
         the marks are sorted according to python difflibe.SequenceMatcher (~longest contiguous matching subsequence)
        '''
        def sort_marks(marks, search_string):
            return sorted(
                marks,
                key=lambda m:difflib.SequenceMatcher(None, str(m), search_string).ratio(),
                reverse=True
            )
        def contained(candidate, container):
            tmp = container[:]
            try:
                for i, word in enumerate(candidate):
                    if i == len(candidate) - 1:
                        if any(word in c for c in tmp):
                            return True
                        else:
                            return False
                    else:
                        tmp.remove(word)
            except ValueError:
                return False
        # Remove extra spaces
        # keep a space if it is at the end of string, since it means that a whole word must be matched
        search_string = search_string.lstrip()
        if not search_string:
            return sort_marks(self.marks, "")

        filtered_bookmarks = []
        words_re = re.compile('\w+')
        search_words = words_re.findall(search_string.lower())
        for mark in self.marks:
            mark_splitted = words_re.findall(mark.cmd.lower()) + words_re.findall(mark.alias.lower())
            if contained(search_words, mark_splitted):
                filtered_bookmarks.append(mark)

        return sort_marks(filtered_bookmarks, search_string)

    def remove_mark(self, mark):
        self.marks.remove(next(m for m in self.marks if mark.equals(m)))
        self.dirty = True

    def add_mark(self, mark):
        if not mark:
            return
        exist = [m for m in self.marks if m.cmd == mark.cmd]
        if exist and not mark.equals(exist[0]):
            self.remove_mark(exist[0])
            self.marks.append(mark)
            self.dirty = True
        elif not exist:
            self.marks.append(mark)
            self.dirty = True


class FileBookmarks(Bookmarks):
    '''Seperate Bookmarks creation from App logic for testability'''

    def __init__(self):
        self.file = open(os.path.join(os.getenv('MARKER_DATA_HOME'), 'marks.txt'), 'r+')
        super(FileBookmarks, self).__init__([Mark.deserialize(l.strip('\n').strip('\r')) for l in self.file.readlines() if l])

    def __enter__(self):
        return self

    def __exit__(self , type, value, traceback):
        if self.dirty:
            # clear file contents
            self.file.seek(0)
            self.file.truncate(0)
            self.file.write('\n'.join([m.serialize() for m in self.marks]))
        self.file.close()


class Mark(object):
    '''A Mark is basically a command and an optionnal alias'''
    def __init__(self, cmd, alias):
        if not cmd:
            raise "empty command argument"
        self.cmd = cmd
        self.alias = alias
        if not self.alias:
            self.alias = ""
        pass

    def __repr__(self):
        if self.alias and self.alias != self.cmd:
            return self.cmd+"("+self.alias+")"
        else:
            return self.cmd

    @staticmethod
    def deserialize(str):
        if "##" in str:
            cmd, alias = str.split("##")
        else:
            cmd = str
            alias = ""
        return Mark(cmd, alias)

    def serialize(self):
        if self.alias:
            return self.cmd + "##" + self.alias
        else:
            return self.cmd

    def equals(self, mark):
        return self.cmd == mark.cmd and self.alias == mark.alias

