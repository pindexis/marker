import sys

BOLD = "\x1b[1m"
CLEAR_FORMATTING = "\x1b[0m"
ERASE_SCREEN = "\x1b[J"
ERASE_LINE = "\x1b[2K"
FOREGROUND_BLACK = "\x1b[30m"
BACKGROUND_WHITE = "\x1b[47m"

def _CURSOR_COLUMN(pos):
    return "\x1b["+str(pos)+"G"


def _CURSOR_PREVIOUS_LINES(number):
    return "\x1b["+str(number)+"F"


def select_text(text):
    return  (FOREGROUND_BLACK +
            BACKGROUND_WHITE + 
            text.replace(
                CLEAR_FORMATTING,
                CLEAR_FORMATTING + FOREGROUND_BLACK + BACKGROUND_WHITE)+
            CLEAR_FORMATTING)


def bold_text(text):
    return  (BOLD + 
            text.replace(
                CLEAR_FORMATTING,
                CLEAR_FORMATTING + BOLD)+
            CLEAR_FORMATTING)


def move_cursor_line_beggining():
    sys.stdout.write(_CURSOR_COLUMN(0))


def move_cursor_horizental(n):
    sys.stdout.write(_CURSOR_COLUMN(n))


def move_cursor_previous_lines(number_of_lines):
    sys.stdout.write(_CURSOR_PREVIOUS_LINES(number_of_lines))


def erase_from_cursor_to_end():
    sys.stdout.write(ERASE_SCREEN)


def erase_line():
    sys.stdout.write(ERASE_LINE)


def flush():
    sys.stdout.flush()