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
    function _marker_get_1 {
        line="$BUFFER"
        zle kill-whole-line
        $(markergn "$line")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then
            # there are more than one result that matches the typed string
            # Marker will then be executed in interactive mode  
            line=$(echo "$line" | sed "s/'/'\"'\"'/g")           
            BUFFER="markerg '$line'"
            zle accept-line
        fi
    }
    zle -N _marker_get_1
    bindkey '\emg1' _marker_get_1 

    # set the content of the temporary file in the command-line
    function _marker_get_2 {
        BUFFER="$(<${MARKER_DATA_HOME}/pipe.txt)"
        zle end-of-line
    }
    zle -N _marker_get_2
    bindkey '\emg2' _marker_get_2 

    # In zsh, it's not possible(or I couldn't) execute statements in two command-line prompts within the same function,
    # That's why I'm using the pattern of defining two functions(ie _marker_get and _marker_set), bind them to two unimportant shortcuts
    # Then define a third binding using the main shortcut(ie C-g) where I trigger the created shortcuts
    # This will make it possible to control more than one single command-line prompt
    # marker_key_next_placeholder will automatically place the cursor at the first placeholder if it does exist 
    bindkey -s "$marker_key_get" "\emg1\emg2$marker_key_next_placeholder"

    # Mark the written string in the command-line
    function _marker_mark_1 {
        export TMP_MARKER="$BUFFER"
        # Escape single quotes (keeping the string written by the user intact)
        TMP_MARKER=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        BUFFER="marker mark --command='${TMP_MARKER}'"
        zle accept-line
    }
    zle -N _marker_mark_1
    bindkey '\emm1' _marker_mark_1

    function _marker_mark_2 {
        BUFFER="$TMP_MARKER"
        zle end-of-line
    }
    zle -N _marker_mark_2 
    bindkey '\emm2' _marker_mark_2

    bindkey -s "$marker_key_mark" '\emm1\emm2'

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
    function _marker_get_1 {
        line="$READLINE_LINE"
        $(markergn "$line")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then
            line=$(echo "$line" | sed "s/'/'\"'\"'/g")
            READLINE_LINE="markerg '$line'"
            # can't execute newline here like what we do for zsh, use temporary binding to do the tric
            bind '"\emgn":"\n"'
        else
            bind '"\emgn":""'
        fi
    }

    # set the content of the temporary file in the command-line
    function _marker_get_2 {
        READLINE_LINE="$(<${MARKER_DATA_HOME}/pipe.txt)"
        READLINE_POINT="${#READLINE_LINE}"
    }

    # mark the written string in the command-line
    function _marker_mark_1 {
        export TMP_MARKER="$READLINE_LINE"
        # Escape single quotes (keeping the string written by the user intact)
        TMP_MARKER=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        READLINE_LINE="marker mark --command='${TMP_MARKER}'"
    }
    function _marker_mark_2 {
        READLINE_LINE="$TMP_MARKER"
        READLINE_POINT="${#READLINE_LINE}"
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

    bind -x '"\emg1":"_marker_get_1"'
    bind -x '"\emg2":"_marker_get_2"'
    bind -x '"\emm1":"_marker_mark_1"'
    bind -x '"\emm2":"_marker_mark_2"'

    bind -x '"'"$marker_key_next_placeholder"'":"_marker_next_placeholder"'
    # combine both marker_get and marker_next_placeholder
    bind '"'"$marker_key_get"'":"\emg1\emgn\emg2'"$marker_key_next_placeholder"'"'
    bind '"'"$marker_key_mark"'":"\emm1\n\emm2"'   
fi
