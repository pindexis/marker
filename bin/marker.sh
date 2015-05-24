# I rather aliasing Marker than add it to the global variable $PATH or pollute /usr/local directory
# this will make uninstalling easier
alias marker="${MARKER_HOME}/bin/marker"

 # Helper functions to execute marker command-line tool and redirect its output to a file
function markergn(){
    marker get --search="$1" --non-interactive --stdout="$MARKER_DATA_HOME/pipe.txt"
}
function markerg(){
    marker get --search="$1" --stdout="$MARKER_DATA_HOME/pipe.txt"
}

# default key bindings
marker_key_mark="${MARKER_KEY_MARK:-\C-k}"
marker_key_get="${MARKER_KEY_GET:-\C-g}"
marker_key_next_placeholder="${MARKER_KEY_NEXT_PLACEHOLDER:-\C-t}"

if [[ -n "$ZSH_VERSION" ]]; then
    # zshell
    
    # 1- Invoke  marker in non-interactive mode:
    # - If only one result is matched, Replace the written string in the command-line with it, without displaying a UI selector
    # - if more than one results are returned, then re-invoke the command in interactive mode
    # 2- The result of Marker will be stored in a temporary file that will be read by the shell, and the user input will be replaced with the content of that file    
    function _marker_get {
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
    zle -N _marker_get
    bindkey '\etmp1' _marker_get 

    # set the content of the temporary file in the command-line
    function _marker_set {
        BUFFER="$(<${MARKER_DATA_HOME}/pipe.txt)"
        zle end-of-line
    }
    zle -N _marker_set
    bindkey '\etmp2' _marker_set 

    # In zsh, it's not possible(or I couldn't) execute statements in two command-line prompts within the same function,
    # That's why I'm using the pattern of defining two functions(ie _marker_get and _marker_set), bind them to two unimportant shortcuts
    # Then define a third binding using the main shortcut(ie C-g) where I trigger the created shortcuts
    # This will make it possible to control more than one single command-line prompt
    # marker_key_next_placeholder will automatically place the cursor at the first placeholder if it does exist 
    bindkey -s "$marker_key_get" "\etmp1\etmp2$marker_key_next_placeholder"

    # Mark the written string in the command-line
    function _marker_mark {
        export TMP_MARKER="$BUFFER"
        # Escape single quotes (keeping the string written by the user intact)
        TMP_MARKER=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        BUFFER="marker mark --command='${TMP_MARKER}'"
        zle accept-line
    }
    zle -N _marker_mark
    bindkey '\etmp3' _marker_mark

    function _mks {
        BUFFER="$TMP_MARKER"
        zle end-of-line
    }
    zle -N _mks 
    bindkey '\etmp4' _mks

    bindkey -s "$marker_key_mark" '\etmp3\etmp4'

    # move the cursor the next placeholder '%%'
    function _move_cursor_to_next_placeholder {
        # awk command returns the first index of the place-holder in a string(offset 1 based)
        placeholder_offset=$(echo "$BUFFER" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            # substract 1 from the offset, to make it 0 based
            let "placeholder_offset = $placeholder_offset - 1"
            CURSOR="$placeholder_offset"
            BUFFER="${BUFFER[1,$placeholder_offset]}${BUFFER[$placeholder_offset+3,-1]}"
        fi        
    }
    zle -N _move_cursor_to_next_placeholder
    bindkey "$marker_key_next_placeholder" _move_cursor_to_next_placeholder

elif [[ -n "$BASH" ]]; then

    # Look at zsh _marker_get docstring
    function _marker_get {
        line="$READLINE_LINE"
        $(markergn "$line")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then           
            markerg "$line"
        fi
        READLINE_LINE="$(<${MARKER_DATA_HOME}/pipe.txt)"
        READLINE_POINT="${#READLINE_LINE}"
    }

    # mark the written string in the command-line
    function _marker_mark {
        marker mark --command="${READLINE_LINE}"
    }

    # move the cursor the next placeholder
    function _marker_next_placeholder(){
        placeholder_offset=$(echo "$READLINE_LINE" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            # substract 1 from the offset, to make the offset 0 based
            placeholder_offset=$(expr $placeholder_offset - 1)
            READLINE_POINT="$placeholder_offset"
            READLINE_LINE="${READLINE_LINE:0:$placeholder_offset}${READLINE_LINE:$placeholder_offset+2}"
        fi
    }

    bind -x '"\eg":"_marker_get"'
    bind -x '"'"$marker_key_mark"'":"_marker_mark"'
    bind -x '"'"$marker_key_next_placeholder"'":"_marker_next_placeholder"'
    # combine both marker_get and marker_next_placeholder
    bind '"'"$marker_key_get"'":"\eg'"$marker_key_next_placeholder"'"'    
fi
