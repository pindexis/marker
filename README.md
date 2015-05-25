# marker

Do you heavily use Ctrl+R(search through history) to search for commands that you frequently use?  
Marker lets you easily bookmark these commands and quickly retrieve them without going through Shell Aliases/Functions/Multiple Ctrl-R...  
It offers the following features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (rather than Ctrl-R exact match).
- Aliases: `listen port` can magically be transformed into `sudo netstat -nlp | grep`.
- Command templates: Marker lets you bookmark commands with place-holders and easily place the cursor at those place-holders.
- Portability across supported shells: you can use bookmarked commands in both Bash and Zshell.

![command-template](https://cloud.githubusercontent.com/assets/2557967/7770230/184f4d8a-0084-11e5-8e03-2402cbe634aa.gif)

## Usage
Simplicity is key, Three keyboard shortcuts let you take most of Marker:
- `Ctrl-k`: Mark the current written string in the command line.
- `Ctrl-space`: search for commands that match the current written string.
- `Ctrl-t`: place the cursor at the next placeholder, identified by '%%'
- `marker remove`: remove a bookmark

[![ScreenShot](https://cloud.githubusercontent.com/assets/2557967/7701147/3078969c-fe1c-11e4-9837-a2e586fbe07e.png)](http://youtu.be/JuBY9sbzjdU)

## Requirements
- python (2.7+ or 3.0+)
- Bash-4.0+ or Zshell.
- Linux Or OSX

#####Note:
In OSX, it seems like Bash 3.x is the default shell which is not supported. you have to [update your Bash to 4.x](http://apple.stackexchange.com/a/24635) or [change your shell to zshell](http://stackoverflow.com/a/1822126/1117720) in order to use Marker.
## Installation
- `mkdir ~/.marker && cd ~/.marker` or go wherever you want to install Marker
- `git clone https://github.com/pindexis/marker .`
- `./install.py`

## How It Works:
  Marker is a composed of shell script, and a python tool:  
  The shell code acts as a wrapper around that python tool, it's responsible for managing the user input in the command-line(adding/removing text, moving the cursor around etc...).  
  The python utility in the other hand(called marker) contains the app logic. It manages the bookmarked data, do the matching, and present a UI selector if it's called in interactive mode. It doesn't depend on the Shell script, so it can be called separately as a command line utility(`marker --help`)
  
  The communication between the shell script and the python commandline tool is done via a temporary file. For example, here's how things work when Ctrl+space is pressed:
  
  - A shell code executes, calling 'marker' tool in non-interactive mode(without displaying UI selector) passing as argument the written string in the commandline and a file path where the matched commands will be stored. The python tool will then determine the commands that match the given string and stores them in the file that was passed as an argument.
  - The shell script will then parse that file. if there is only one command there, It will replace the current string written on the command-line by that command. If there is more than one command returned, It calls the python tool again in Interactive mode, where a UI selector will be shown that allows the user to select the desired command. The user selected command will be stored in the file passed as an argument and displayed in the command-line. (The reason of this approach is to avoid creating a new command-line prompt when there is only one match, but rather work on current prompt).

You can take a look at `bin/marker.sh` for more details. Most magic happens there.

## License
[MIT](LICENSE)
