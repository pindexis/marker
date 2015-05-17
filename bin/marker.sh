# I rather aliasing Marker than add it to the global variable $PATH or pollute /usr/local directory
# this will make uninstalling easier
alias marker="${MARKER_HOME}/bin/marker"

function markergn(){
    marker get --search="$1" --non-interactive --stdout="$MARKER_DATA_HOME/pipe.txt"
}

function markerg(){
    marker get --search="$1" --stdout="$MARKER_DATA_HOME/pipe.txt"
}

# This Portion of code is responsible for invoking the marker command when keyboard shortcuts are pressed
# This works as follow:
# 1- Invoke  marker in non-interactive mode, this îs to make sure that if only one result matches the user input
# - If only one result is matched, Replace the user input in the current shell prompt with it, without displaying marker interface or creating a new shell prompt
# - if more than one results are returned, then re-invoke the command with interactive mode
# 2- The result of Marker will be stored in a temporary file that will be read by the shell, and the user input will be replaced with the content of that file
if [ -n "$ZSH_VERSION" ]; then
    # zshell
    function _marker-get {
        search="$BUFFER"
        zle kill-whole-line
        $(markergn "$search")
        num_lines=$(cat $MARKER_DATA_HOME/pipe.txt | wc -l)
        if [[ num_lines -ne 1 ]]; then
            # there are more than one result that matches the typed string
            # Marker will then be executed in interactive mode             
            BUFFER="markerg \"$search\""
            zle accept-line
        fi
    }
    zle -N _marker-get
    bindkey '\e1' _marker-get 

    function _marker-set {
        BUFFER="$(<$MARKER_DATA_HOME/pipe.txt)"
        zle end-of-line
    }
    zle -N _marker-set
    bindkey '\e2' _marker-set 
    # C-space is set to execute two keyboard shortcuts, to run statements in two commandline prompts(execute->Enter->execute)
    bindkey -s '\C-@' '\e1\e2'

    function _mkm {
        export TMP_MARKER="$BUFFER"
        # Escape single quotes (keeping the string written by the user intact)
        # Unfortunaetly, this is not possible in Bash(single quotes will be stripped) 
        TMP_MARKER=$(echo $TMP_MARKER | sed "s/'/'\"'\"'/g")
        BUFFER="marker mark --command='$TMP_MARKER'"
        zle accept-line
    }
    zle -N _mkm
    bindkey '\e3' _mkm

    function _mks {
        BUFFER="$TMP_MARKER"
        zle end-of-line
    }
    zle -N _mks 
    bindkey '\e4' _mks

    bindkey -s '\C-k' '\e3\e4'
else
    # Assume the shell use readline

    # A readline command is a literal sequence of characters and Meta-characters
    # It's not possible to evaluate a shell statement in a readline command, and write different input based on it
    # Fortunately, there is an indirect way to do so by evaluating a shell statement via the expand-line keyboard shortcut(\e\C-e),
    # this shell statement will bind a different command to a keyboard key which will be typed by the original readline command
    # Here's simplified example to demonstrate the idea:
    # bind "\C-a" "`greeting`\e\C-e\C-b:" -> this will execute the greeting function below followed by \C-b
    # greeting = if(user == Admin){
    #    bind '\C-b' 'Hi Sir'
    # }else{
    #    bind '\C-b' 'You don\'t have access ):' 
    # }
    # 
    # The binding is done by writing to an .rc file than re-interpreting .inputrc by using \C-x\C-r shortcut
    # Take a look at marker.rc
    function rl_marker(){
        args="$@"
        markergn "$args"
        num_lines=$(cat $MARKER_DATA_HOME/pipe.txt | wc -l)
        if [[ num_lines -ne 1 ]]; then 
            # none or more than one result matched the typed string
            # Marker will then be executed in interactive mode            
            echo '"\el":" markerg \"'$args'\"\C-j$(<$MARKER_DATA_HOME/pipe.txt)\e\C-e\"'>$MARKER_DATA_HOME/tmp_readline.rc
        else
            # One result match the user input, Substitute the current written string with the returned one
            echo '"\el":"$(<$MARKER_DATA_HOME/pipe.txt)\e\C-e"'>$MARKER_DATA_HOME/tmp_readline.rc;
        fi
    }
fi
