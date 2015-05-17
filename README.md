# marker
Do you heavily use Ctrl+R(search through history) to search for commands that you frequently use?  
Marker let you easily bookmark these commands and quickly retrieve them without going through Shell Aliasing/Many Ctrl-R.
It offers the following features:
- A UI selector that let you easily select desired command if more than one command is matched
- Fuzzy matching (rather than Ctrl-R exact match)
- Aliases: `listen port` can magically be transformed into `sudo netstat -nlp | grep`

## Usage
Simplicity is key, Two keyboard shortcuts let you take most of Marker:
- `Ctrl+k`: Mark the current written string in the command line prompt.
- `Ctrl+Space`: search for commands that match the current written string.
- `marker remove`: remove a bookmark

## Requirements
- python (2.7+ or 3.0+)
- Bash or Zshell.
- if you're using Bash, Readline should be in Emacs mode(It is by default)
- Linux Or OSX (Windows not supported)

## Installation
- `cd /usr/local` or wherever you want to install Marker
- `curl -L https://github.com/pindexis/marker/archive/master.tar.gz | tar -zx && mv marker-master marker`
- `./install.py`

## License
[MIT](LICENSE)
