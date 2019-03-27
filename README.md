# Marker

![marker](https://cloud.githubusercontent.com/assets/2557967/14209204/d99db934-f81a-11e5-910c-9d34ac155d18.gif)

Marker is a command palette for the terminal. It lets you bookmark commands (or commands templates) and easily retreive them with the help of a real-time fuzzy matcher.

It's also shipped with many commands common usage(Thanks to [tldr](https://github.com/tldr-pages/tldr)).
  
## Features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (through commands and their descriptions).
- Command template: You can bookmark commands with place-holders and place the cursor at those place-holders using a keyboard shortcut.
- Portability across supported shells: you can use bookmarked commands in both Bash and Zshell.

## Usage
- `Ctrl-space`: search for commands that match the current written string in the command-line.
- `Ctrl-k` (or `marker mark`): Bookmark a command.
- `Ctrl-t`: place the cursor at the next placeholder, identified by '{{anything}}'
- `marker remove`: remove a bookmark

You can customize key binding using environment variables, respectively with ```MARKER_KEY_GET```, ```MARKER_KEY_MARK``` and ```MARKER_KEY_NEXT_PLACEHOLDER```.

## Requirements
- python (2.7+ or 3.0+)
- Bash-4.3+ or Zshell.
- Linux Or OSX

##### Note:
In OSX, it seems like Bash 3.x is the default shell which is not supported. you have to [update your Bash to 4.3+](http://apple.stackexchange.com/a/24635) or [change your shell to zshell](http://stackoverflow.com/a/1822126/1117720) in order to use Marker.

## Installation

`git clone --depth=1 https://github.com/pindexis/marker ~/.marker && ~/.marker/install.py`

## License
[MIT](LICENSE)
