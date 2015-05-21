# marker
Do you heavily use Ctrl+R(search through history) to search for commands that you frequently use?  
Marker lets you easily bookmark these commands and quickly retrieve them without going through Shell Aliases/Functions/Multiple Ctrl-R...  
It offers the following features:
- A UI selector that lets you easily select the desired command if more than one command is matched.
- Fuzzy matching (rather than Ctrl-R exact match).
- Aliases: `listen port` can magically be transformed into `sudo netstat -nlp | grep`.
- Command templates: Marker lets you bookmark commands with place-holders and easily place the cursor at those place-holders.

## Usage
Simplicity is key, Three keyboard shortcuts let you take most of Marker:
- `Ctrl-k`: Mark the current written string in the command line.
- `Ctrl-Space`: search for commands that match the current written string.
- `Ctrl-t`: place the cursor at the next placeholder, identified by the '%' character
- `marker remove`: remove a bookmark

[![ScreenShot](https://cloud.githubusercontent.com/assets/2557967/7701147/3078969c-fe1c-11e4-9837-a2e586fbe07e.png)](http://youtu.be/JuBY9sbzjdU)

## Requirements
- python (2.7+ or 3.0+)
- Bash or Zshell (didn't tested on other shells).
- if you're using Bash, Readline should be in Emacs mode(It is by default)
- Linux Or OSX

## Installation
- `cd /usr/local` or wherever you want to install Marker
- `git clone git@github.com:pindexis/marker.git`
- `cd marker`
- `./install.py`

## How It Works:
  Marker is a composed of shell script, and a python tool:  
  The shell code acts as a wrapper around that python tool, it's responsible for managing the user input in the command-line(adding/removing text, moving the cursor around etc...).  
  The python utility in the other hand(called marker) contains the app logic. It manages the bookmarked data, do the matching, and present a UI selector if it's called in interactive mode. It doesn't depend on the Shell script, so it can be called separately as a command line utility(`marker --help`)
  
  The communication between the shell script and the python commandline tool is done via a temporary file. For example, here's how things work when Ctrl+space is pressed:
  
  - A shell code executes, calling 'marker' tool in non-interactive mode(without displaying UI selector) passing as argument the written string in the commandline and a file path where the matched commands will be stored. The python tool will then determine the commands that match the given string and stores them in the file that was passed as an argument.
  - The shell script will then parse that file. if there is only one command there, It will replace the current string written on the command-line by that command. If there is more than one command returned, It calls the python tool again in Interactive mode, where a UI selector will be shown that allows the user to select the desired command. The user selected command will be stored in the file passed as an argument and displayed in the command-line. (The reason of this approach is to avoid creating a new command-line prompt when there is only one match, but rather work on current prompt).

You can take a look at `bin/marker.sh` for more details. Most magic happens there.

### Limitation with Bash (and shells that use Readline):
Bash uses an external library(Readline) to process the user input in the command-line(including keyboard bindings). This separation makes it hard to script and extend the command-line when certain keys are pressed. For example, It's not possible to invoke shell functions intuitively when a user press a keyboard shortcut and manipulate the command-line from those functions(in contrast with zshell where the input processor zle is integrated within the shell).  

A couple of hacks were made to make Marker work with Bash, notably triggering shell-expand-line to evaluate a shell function with the current written string as an argument. This shell function will then executes some logic and dynamically bind a certain sequence of characters to a temporary keyboard shortcut which will be executed finally by the original shortcut(ie `ctrl-Space`)(`bin/marker.sh` contains more details).  

Sadly, hacks come with a cost: It's not possible to use the keyboard shortcuts `Ctrl-k` and `Ctrl-t` with commands that contain single quotes (`'`) because single quotes are used to enclose the user input. So you probably should use double quotes with escaping instead(see [here](http://stackoverflow.com/questions/6697753/difference-between-single-and-double-quotes-in-bash for difference between single and double quotes) for difference between single and double quotes)

## License
[MIT](LICENSE)
