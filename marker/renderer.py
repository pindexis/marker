import os
import ansi
import re
import math

'''Command line user interface'''

MAX_ROWS=20
def _get_terminal_columns():
    ''' get the number of terminal columns, used to determine spanned lines of a mark(required for cursor placement) '''
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)

def erase():
    ''' the commandline cursor is always at the first line (Marker prompt)
    Therefore, erasing the current and following lines clear all marker output
    '''
    ansi.move_cursor_line_beggining()
    ansi.erase_from_cursor_to_end()

def refresh(state):
    ''' Redraw the output, this function will be triggered on every user interaction(key pressed)'''
    erase()
    lines, num_rows = _construct_output(state)
    for line in lines:
        print(line)
    # go up
    ansi.move_cursor_previous_lines(num_rows)
    # palce the cursor at the end of first line
    ansi.move_cursor_horizental(len(lines[0])+1)
    ansi.flush()

def _construct_output(state):
    columns = _get_terminal_columns()
    ansi_escape = re.compile(r'\x1b[^m]*m')
    def number_of_rows(line):
        line = ansi_escape.sub('', line)
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
                    fm = fm.replace(w, ansi.bold_text(w))
            # highlighting selected command
            if m == state.get_selected_match():
                fm = ansi.select_text(fm)
            displayed_lines.append(fm)
    else:
        not_found_line = 'Nothing found'
        displayed_lines.append(not_found_line)
        num_rows += number_of_rows(not_found_line)
    return displayed_lines, num_rows

