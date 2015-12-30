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
marker_key_get="${MARKER_KEY_GET:-\C-@}"
marker_key_next_placeholder="${MARKER_KEY_NEXT_PLACEHOLDER:-\C-t}"

function get_cursor_position(){
  # based on a script from http://invisible-island.net/xterm/xterm.faq.html
  exec < /dev/tty
  oldstty=$(stty -g)
  stty raw -echo min 0
  # on my system, the following line can be replaced by the line below it
  echo -en "\033[6n" > /dev/tty
  # tput u7 > /dev/tty    # when TERM=xterm (and relatives)
  IFS=';' read -r -d R  row col 
  stty $oldstty
  # change from one-based to zero based so they work with: tput cup $row $col
  row=$((${row:2} - 1))    # strip off the esc-[
  col=$((${col} - 1))
  echo "$row $col"
}
function get_col_position(){
  echo $(get_cursor_position) | cut -f 2 -d " "
}
function get_row_position(){
  echo $(get_cursor_position) | cut -f 1 -d " "
}
function place_cursor_next_line(){
  </dev/tty echo ''
}
function place_cursor(){
  tput cup $1 $2
}
if [[ -n "$ZSH_VERSION" ]]; then
    # zshell
    
    # 1- Invoke  marker in non-interactive mode:
    # - If only one result is matched, Replace the written string in the command-line with it, without displaying a UI selector
    # - if more than one results are returned, then re-invoke the command in interactive mode
    # 2- The result of Marker will be stored in a temporary file that will be read by the shell, and the user input will be replaced with the content of that file    
    #
    # Due to stdin related problems when running interactive commands(require user input) from a widget(from inside shell functions)
    # I've adopted the approach of running interactive commands like normal shell commands, by setting the commandline content to marker command, then simulating the press of Enter

    function _marker_get {
        line="$BUFFER"
        zle kill-whole-line
        $(markergn "$line")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then
            # there are more than one result that matches the typed string
            # Marker will then be executed in interactive mode  
            # get the offset from the start of comandline prompt
            col=$(get_col_position)
            place_cursor_next_line
            </dev/tty markerg $line
            # reset the absolute and relative cursor position, note that it's necessary to get row position after qfc is run, because it may be changed during qfc execution
            row=$(get_row_position)
            place_cursor $(($row - 1)) $col 
        fi
        BUFFER="$(<${MARKER_DATA_HOME}/pipe.txt)"
        zle end-of-line
        _move_cursor_to_next_placeholder
    }

    # Mark the written string in the command-line
    function _marker_mark_1 {
        export TMP_MARKER="$BUFFER"
        # Escape single quotes (keeping the string written by the user intact)
        ESCAPED_COMMAND=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        BUFFER=" marker mark --command='${ESCAPED_COMMAND}'"
        zle accept-line
    }
    # Set the user written string back in the command-line
    function _marker_mark_2 {
        BUFFER="$TMP_MARKER"
        zle end-of-line
    }
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

    zle -N _marker_get
    zle -N _move_cursor_to_next_placeholder
    bindkey "$marker_key_get" _marker_get 
    bindkey "$marker_key_next_placeholder" _move_cursor_to_next_placeholder

    zle -N _marker_mark_1
    bindkey '\emm1' _marker_mark_1
    zle -N _marker_mark_2 
    bindkey '\emm2' _marker_mark_2
    bindkey -s "$marker_key_mark" '\emm1\emm2'

elif [[ -n "$BASH" ]]; then

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

    # Look at zsh _marker_get docstring
    # In Bash the written string will be accessed via the 'READLINE_LINE' variable, and the cursor position via 'READLINE_POINT'. Those variables are read-write
    function _marker_get {
        line="$READLINE_LINE"
        $(markergn "$line")
        num_lines=$(cat ${MARKER_DATA_HOME}/pipe.txt | wc -l)
        if [[ "$num_lines" -ne 1 ]]; then
            col=$(get_col_position)
            </dev/tty markerg $line
            # reset the absolute and relative cursor position, note that it's necessary to get row position after qfc is run, because it may be changed during qfc execution
            row=$(get_row_position)
            place_cursor $row $col 
        fi
        # set the content of the temporary file in the command-line
        READLINE_LINE="$(<${MARKER_DATA_HOME}/pipe.txt)"
        READLINE_POINT="${#READLINE_LINE}"
        _marker_next_placeholder
    }

     # mark the written string in the command-line
    function _marker_mark_1 {
        export TMP_MARKER="$READLINE_LINE"
        # Escape single quotes (keeping the string written by the user intact)
        TMP_MARKER=$(echo "$TMP_MARKER" | sed "s/'/'\"'\"'/g")
        READLINE_LINE=" marker mark --command='${TMP_MARKER}'"
    }

    function _marker_mark_2 {
        READLINE_LINE="$TMP_MARKER"
        READLINE_POINT="${#READLINE_LINE}"
    }   

    # bind -x somehow doesn't support ctrl+space directly
    bind -x '"\emg1":"_marker_get"'
    bind '"'"$marker_key_get"'":"\emg1"'

    bind -x '"\emm1":"_marker_mark_1"'
    bind -x '"\emm2":"_marker_mark_2"'
    bind '"'"$marker_key_mark"'":"\emm1\n\emm2"'   

    bind -x '"'"$marker_key_next_placeholder"'":"_marker_next_placeholder"'
fi
