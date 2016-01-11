# marker

Do you heavily use Ctrl+R(search through history) to search for commands that you frequently use?  
Marker lets you easily bookmark these commands and quickly retrieve them without going through Shell Aliases/Functions/Multiple Ctrl-R...  
It offers the following features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (rather than Ctrl-R exact match).
- Aliases: `listen port` can be expanded into `sudo netstat -nlp | grep`.
- Command templates: Marker lets you bookmark commands with place-holders and easily place the cursor at those place-holders.
- Portability across supported shells: you can use bookmarked commands in both Bash and Zshell.

![command-template](https://cloud.githubusercontent.com/assets/2557967/7770230/184f4d8a-0084-11e5-8e03-2402cbe634aa.gif)

## Usage
Simplicity is key, Three keyboard shortcuts let you take most of Marker:
- `Ctrl-k`: Mark the current written string in the command line.
- `Ctrl-space`: search for commands that match the current written string.
- `Ctrl-t`: place the cursor at the next placeholder, identified by '{{anything}}'
- `marker remove`: remove a bookmark

[![ScreenShot](https://cloud.githubusercontent.com/assets/2557967/7701147/3078969c-fe1c-11e4-9837-a2e586fbe07e.png)](http://youtu.be/JuBY9sbzjdU)

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
