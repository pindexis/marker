# I rather aliasing Marker than add it to the global variable $PATH or pollute /usr/local directory
# this will make uninstalling easier
alias marker="${MARKER_HOME}/bin/marker"

function markergn(){
    marker get --search="$1" --non-interactive --stdout="$MARKER_DATA_HOME/pipe.txt"
}

function markerg(){
    marker get --search="$1" --stdout="$MARKER_DATA_HOME/pipe.txt"
}

# default key bindings
marker_key_mark="${MARKER_KEY_MARK:-'\C-k'}"
marker_key_get="${MARKER_KEY_GET:-'\C-g'}"
marker_key_next_placeholder="${MARKER_KEY_NEXT_PLACEHOLDER:-'\C-t'}"

# This Portion of code is responsible for invoking the marker command when keyboard shortcuts are pressed
# This works as follow:
# 1- Invoke  marker in non-interactive mode, this îs to make sure that if only one result matches the user input
# - If only one result is matched, Replace the user input in the current shell prompt with it, without displaying marker interface or creating a new shell prompt
# - if more than one results are returned, then re-invoke the command with interactive mode
# 2- The result of Marker will be stored in a temporary file that will be read by the shell, and the user input will be replaced with the content of that file
if [[ -n "$ZSH_VERSION" ]]; then
    # zshell
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
    # execute two keyboard shortcuts, to run statements in two commandline prompts(execute->Enter->execute)
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
        placeholder_offset=$(echo "$BUFFER" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            # substract 1 from the offset, to make it 0 based
            let "placeholder_offset = $placeholder_offset - 1"
            CURSOR="$placeholder_offset"
            BUFFER="${BUFFER[1,$placeholder_offset]}${BUFFER[$placeholder_offset+3,-1]}"
        fi        
    }
    zle -N _move_cursor_to_next_placeholder
    bindkey $marker_key_next_placeholder _move_cursor_to_next_placeholder
else if [[ -n "$BASH" ]]
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
    function _marker_mark {
        marker mark --command="${READLINE_LINE}"
    }    
    # Command Template, the purpose is this function is to move to the next placeholder '%%' whenever the user presses on \C-t
    function _marker_next_placeholder(){
        placeholder_offset=$(echo "$READLINE_LINE" | awk 'END{print index($0,"%%")}')
        if [[ "$placeholder_offset" -gt 0 ]]; then
            # substract 1 from the offset, to make the offset 0 based
            placeholder_offset=$(expr $placeholder_offset - 1)
            READLINE_POINT="$placeholder_offset"
            READLINE_LINE="${READLINE_LINE:0:$placeholder_offset}${READLINE_LINE:$placeholder_offset+2}"
        fi
    }

    bind -x '"'$marker_key_get'":"_marker_get"'
    bind -x '"'$marker_key_mark'":"_marker_mark"'
    bind -x '"'$marker_key_next_placeholder'":"_marker_next_placeholder"'
fi