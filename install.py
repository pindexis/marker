#!/usr/bin/env python

from __future__ import print_function
import os
import platform
import shutil
import sys
import marker

SUPPORTED_SHELLS = ('bash', 'zsh')


def get_shell():
    return os.path.basename(os.getenv('SHELL', ''))


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def generate_marker_sh(user_dir, install_dir):
    ''' generate the sh that needs to be sourced '''
    return ("export MARKER_DATA_HOME=\"%s\"" % user_dir +
            "\nexport MARKER_HOME=\"%s\"" % install_dir +
            "\nsource ${MARKER_HOME}/bin/marker.sh"
            )


def generate_readline_rc(user_dir, install_dir):
    return ("$include %s/bin/marker.rc" % install_dir +
            "\n$include %s/tmp_readline.rc" % user_dir
            )


def show_post_installation_message(user_dir):
    print("Marker installed successfully")
    print("\n")
    sourced_file = '%s/marker.sh' % user_dir
    source_msg = "[[ -s %s ]] && source %s" % (sourced_file, sourced_file)

    if platform.system() == 'Darwin' and get_shell() == 'bash':
        rcfile = '.bash_profile'
    else:
        rcfile = '.%src' % get_shell()

    print("\nPlease add he following line has to to your ~/%s:" % rcfile)
    print('\n' + source_msg)

    if get_shell() == 'bash':
        readline_source_msg = '$include %s/marker.rc' % user_dir
        print("\nAdditionnaly, add the following line to your ~/.inputrc (create the file if it does not exist)")
        print('\n' + readline_source_msg)
    print('\n')
    # do_it_for_me = None
    # while(True):
    #     do_it_for_me = raw_input("Do it for me(y/n):")
    #     if do_it_for_me=='y' or do_it_for_me=='n':
    #         break
    # if do_it_for_me == 'y':
    #     with open(os.path.join(os.path.expanduser("~"), rcfile), 'a+') as f:
    #         f.write('\n' + source_msg)
    #     if get_shell() == 'bash':
    #         with open(os.path.join(os.path.expanduser("~"), '.inputrc'), 'a+') as f:
    #             f.write('\n' + readline_source_msg)
    #     print("Marker installed successfully")
    print("\nPlease restart the terminal after doing that.")


def verify_requirements():
    if not get_shell() in SUPPORTED_SHELLS:
        print("Your SHELL %s is not supported" % get_shell(), file=sys.stderr)
        sys.exit(1)
    
    if sys.version_info[0] == 2 and sys.version_info[1] < 6:
        print("Python v2.6+ or v3.0+ required.", file=sys.stderr)
        sys.exit(1)


def main():
    verify_requirements()
    print("---------------------------------------")
    user_dir = os.path.join(os.path.expanduser("~"), '.local', 'share','marker')
    install_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    mkdir(user_dir)
    
    write_to_file(
        os.path.join(user_dir, 'marker.sh'),
        generate_marker_sh(user_dir, install_dir))
    write_to_file(
        os.path.join(user_dir, 'marker.rc'),
        generate_readline_rc(user_dir, install_dir))   
    # only overwrite the file if it doesn't already exist(can useful when updating the tool)
    if not os.path.isfile(os.path.join(user_dir, 'marks.txt')):
        write_to_file(os.path.join(
            user_dir, 'marks.txt'),
            "") 
    
    show_post_installation_message(user_dir)
    print("---------------------------------------")

if __name__ == "__main__":
    main()
