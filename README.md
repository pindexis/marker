# Marker

![marker](https://cloud.githubusercontent.com/assets/2557967/14208545/f1319046-f817-11e5-883b-343ecfb7b502.gif)

Marker is a command palette for the terminal. It let you bookmark commands (or commands templates) and easily retreive them with the help of a real-time fuzzy matcher.
It's also shipped with many commands common usage(Thanks to tldr).
  
## Features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (through commands and their descriptions).
- Command template: You can bookmark commands with place-holders and place the cursor at those place-holders using a keyboard shortcut.
- Portability across supported shells: you can use bookmarked commands in both Bash and Zshell.

## Usage
- `Ctrl-k`: Mark the current written string in the command line.
- `Ctrl-space`: search for commands that match the current written string.
- `Ctrl-t`: place the cursor at the next placeholder, identified by '{{anything}}'
- `marker remove`: remove a bookmark

## Requirements
- python (2.7+ or 3.0+)
- Bash-4.3+ or Zshell.
- Linux Or OSX

#####Note:
In OSX, it seems like Bash 3.x is the default shell which is not supported. you have to [update your Bash to 4.3+](http://apple.stackexchange.com/a/24635) or [change your shell to zshell](http://stackoverflow.com/a/1822126/1117720) in order to use Marker.

## Installation
- `mkdir ~/.marker && cd ~/.marker` or go wherever you want to install Marker
- `git clone https://github.com/pindexis/marker .`
- `./install.py`

## License
[MIT](LICENSE)