# marker
Do you heavily use Ctrl+R(search through history) to search for commands that you frequently use?  
Marker let you easily bookmark these commands and quickly retrieve them without going through Shell Aliases/Functions/Multiple Ctrl-R...  
It offers the following features:
- A UI selector that let you easily select desired command if more than one command is matched.
- Fuzzy matching (rather than Ctrl-R exact match).
- Aliases: `listen port` can magically be transformed into `sudo netstat -nlp | grep`.
- Command templates: Marker let you bookmark commands with place-holders and easily place the cursor at those place-holders.

[![ScreenShot](https://cloud.githubusercontent.com/assets/2557967/7701147/3078969c-fe1c-11e4-9837-a2e586fbe07e.png)](http://youtu.be/JuBY9sbzjdU)

## Usage
Simplicity is key, Three keyboard shortcuts let you take most of Marker:
- `Ctrl+k`: Mark the current written string in the command line prompt.
- `Ctrl+Space`: search for commands that match the current written string.
- `Ctrl+t`: place the cursor at the next placeholder, identified by the '%' character
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
