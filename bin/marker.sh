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
if [[ -n "$ZSH_VERSION" ]]; then
    # zshell

    # default key bindings
    marker_key_mark=${MARKER_KEY_MARK:-'\C-k'}
    marker_key_get=${MARKER_KEY_GET:-'\C-@'}
    marker_key_next_placeholder=${MARKER_KEY_NEXT_PLACEHOLDER:-'\C-t'}

    # function triggered when the user click on Ctrl+Space
    function _marker-get {
        search="$BUFFER"
        zle kill-whole-line
        $(markergn "$search")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then
            # there are more than one result that matches the typed string
            # Marker will then be executed in interactive mode             
            BUFFER="markerg \"$search\""
            zle accept-line
        fi
    }
    zle -N _marker-get
    bindkey '\etmp1' _marker-get 

    function _marker-set {
        BUFFER="$(<${MARKER_DATA_HOME}/pipe.txt)"
        zle end-of-line
    }
    zle -N _marker-set
    bindkey '\etmp2' _marker-set 
    # C-space is set to execute two keyboard shortcuts, to run statements in two commandline prompts(execute->Enter->execute)
    # automatically place the cursor at the first placeholder if it does exist 
    bindkey -s $marker_key_get '\etmp1\etmp2'$marker_key_next_placeholder

    function _mkm {
        export TMP_MARKER="$BUFFER"
        # Escape single quotes (keeping the string written by the user intact)
        TMP_MARKER=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        BUFFER="marker mark --command='${TMP_MARKER}'"
        zle accept-line
    }
    zle -N _mkm
    bindkey '\etmp3' _mkm

    function _mks {
        BUFFER="$TMP_MARKER"
        zle end-of-line
    }
    zle -N _mks 
    bindkey '\etmp4' _mks

    bindkey -s $marker_key_mark '\etmp3\etmp4'
    # Command Template, the purpose is this function is to move to the next placeholder '%%' whenever the user presses on \C-t
    function _move_cursor_to_next_placeholder {
    # index of the first '%%', starting from 1. 0 if not found
        placeholder_offset=$(echo "$BUFFER" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            zle beginning-of-line
            # substract 1 from the offset, to make the offset 0 based
            placeholder_offset=$(expr "$placeholder_offset" - 1)
            while [[ "$placeholder_offset" -gt 0 ]]
            do
                zle forward-char
                placeholder_offset=$(expr "$placeholder_offset" - 1)
            done
            # delete the placeholder
            zle delete-char
            zle delete-char
        fi
    }
    zle -N _move_cursor_to_next_placeholder
    bindkey $marker_key_next_placeholder _move_cursor_to_next_placeholder
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
    # Bash bind command was avoided to support more shells
    function rl_marker(){
        args="$@"
        markergn "$args"
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ num_lines -ne 1 ]]; then 
            # none or more than one result matched the typed string
            # Marker will then be executed in interactive mode            
            echo '"\etmp":" markerg \"'"$args"'\"\C-j$(<${MARKER_DATA_HOME}/pipe.txt)\e\C-e\"'>${MARKER_DATA_HOME}/tmp_readline.rc
        else
            # One result match the user input, Substitute the current written string with the returned one
            echo '"\etmp":"$(<${MARKER_DATA_HOME}/pipe.txt)\e\C-e"'>${MARKER_DATA_HOME}/tmp_readline.rc;
        fi
    }
    # Command Template, the purpose is this function is to move to the next placeholder '%%' whenever the user presses on \C-t
    function rl_template_next(){
        args="$@"
        # remove that space added(so C-y works correctly for empty cocmmands)
        readline_command="\C-y\C-e\C-?"
        # index of the first '%%', starting from 1. 0 if not found
        placeholder_offset=$(echo "$args" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            # move to the beggining of string
            readline_command="${readline_command}\C-a"
            # substract 1 from the offset, to make the offset 0 based
            placeholder_offset=$(expr $placeholder_offset - 1)
            while [[ "$placeholder_offset" -gt 0 ]]
            do
                readline_command="${readline_command}\C-f"
                placeholder_offset=$(expr "$placeholder_offset" - 1)
            done
            # delete the placeholder
            readline_command="${readline_command}\C-d\C-d"
        fi
        # save the readline command in a temporary file(the caller readline command will reload bindings and execute the \etmp command)
        echo '"\etmp":"'"$readline_command"'"'>${MARKER_DATA_HOME}/tmp_readline.rc
    }

fi

