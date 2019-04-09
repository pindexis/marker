#!/usr/bin/env python

from __future__ import print_function
import os
import platform
import shutil
import sys
import marker
import subprocess
import re

SUPPORTED_SHELLS = ('bash', 'zsh')


def get_shell():
    return os.path.basename(os.getenv('SHELL', ''))


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def generate_marker_sh(config_dir, install_dir):
    ''' generate the sh that needs to be sourced '''
    return ("export MARKER_DATA_HOME=\"%s\"" % config_dir +
            "\nexport MARKER_HOME=\"%s\"" % install_dir +
            "\nsource ${MARKER_HOME}/bin/marker.sh" +
            "\n"
            )


def show_post_installation_message(config_dir_rel):
    print("Marker installed successfully")
    print("\n")
    sourced_file = '$HOME/%s/marker.sh' % config_dir_rel
    source_msg = "[[ -s \"%s\" ]] && source \"%s\"" % (sourced_file, sourced_file)

    if platform.system() == 'Darwin' and get_shell() == 'bash':
        rcfile = '.bash_profile'
    else:
        rcfile = '.%src' % get_shell()

    print("\nPlease add the following line to your ~/%s:" % rcfile)
    print('\n' + source_msg)
    print('\n')
    print("\nPlease restart the terminal after doing that(or re-source your *.rc).")


def verify_requirements():
    if not get_shell() in SUPPORTED_SHELLS:
        print("Your SHELL %s is not supported" % get_shell(), file=sys.stderr)
        sys.exit(1)
    if get_shell() == "bash":
        version_text = subprocess.Popen("bash --version | head -1", shell=True, stdout=subprocess.PIPE).stdout.read()
        m = re.search(b'(\d).(\d)', version_text)
        if m:
            major_version = int(m.group(1))
            minor_version = int(m.group(2))
            print(version_text)
            if major_version < 4 or (major_version == 4 and minor_version < 3):
                print("your Bash version is too old: %s" % version_text, file=sys.stderr)
                print("Marker requires Bash 4.3+", file=sys.stderr)
                sys.exit(1)
        else:
            print("Couldn't extract bash version, please report the issue", file=sys.stderr)
            print("Installation failed", file=sys.stderr)
            sys.exit(1)

    if sys.version_info[0] == 2 and sys.version_info[1] < 6:
        print("Python v2.6+ or v3.0+ required.", file=sys.stderr)
        sys.exit(1)


def main():
    verify_requirements()
    print("---------------------------------------")
    config_dir_relative_path = '.local/share/marker'
    config_dir_abosulte_path = os.path.join(os.path.expanduser("~"), config_dir_relative_path)
    install_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    mkdir(config_dir_abosulte_path)
    
    write_to_file(
        os.path.join(config_dir_abosulte_path, 'marker.sh'),
        generate_marker_sh(config_dir_abosulte_path, install_dir))

    show_post_installation_message(config_dir_relative_path)
    print("---------------------------------------")

if __name__ == "__main__":
    main()
