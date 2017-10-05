# Marker

![marker](https://cloud.githubusercontent.com/assets/2557967/14209204/d99db934-f81a-11e5-910c-9d34ac155d18.gif)

Marker is a command palette for the terminal. It lets you bookmark commands (or commands templates) and easily retreive them with the help of a real-time fuzzy matcher.

It's also shipped with many commands common usage(Thanks to [tldr](https://github.com/tldr-pages/tldr)).

After installation, all commands have to be stored within the folder `~/.local/share/marker/`.
All new commands, bookmarked with `Ctrl-k` will be stored in the file `/.local/share/marker/added_commands.txt`.

## Features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (through commands and their descriptions).
- Command template: You can bookmark commands with place-holders and place the cursor at those place-holders using a keyboard shortcut.
- Portability across supported shells: you can use bookmarked commands in both Bash and Zshell.

## Usage
- `Ctrl-space`: search for commands that match the current written string in the command-line.
- `Ctrl-k` (or `marker add`): Bookmark a command.
- `Ctrl-t`: place the cursor at the next placeholder, identified by '{{anything}}'
- `Ctrl-g`: copy to clipboard you just selected - it uses xsel
- `marker remove`: remove a bookmark

You can customize key binding using environment variables, respectively with ```MARKER_KEY_GET```, ```MARKER_KEY_MARK```, ```MARKER_KEY_NEXT_PLACEHOLDER``` and ```MARKER_KEY_COPY```.

## Requirements
- python (2.7+ or 3.0+)
- Bash-4.3+ or Zshell.
- Linux Or OSX
- xsel by Conrad Parker <conrad@vergenet.net>

#####Note:

In OSX, it seems like Bash 3.x is the default shell which is not supported. you have to [update your Bash to 4.3+](http://apple.stackexchange.com/a/24635) or [change your shell to zshell](http://stackoverflow.com/a/1822126/1117720) in order to use Marker.

## Installation
- `mkdir ~/.marker && cd ~/.marker` or go wherever you want to install Marker
- `git clone` the repistory to the current working directory
- `./install.py`
- `apt-get install xsel` to install xsel, in order to use the `Ctrl-g` feature
- `mv ./tldr ~/.local/share/marker/` to copy the commands within the tldr folder into the marker home folder where all the commands need to be added

## License
[MIT](LICENSE)
