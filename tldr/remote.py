import tempfile
import shutil
import requests
import StringIO
import zipfile
import sys
import io
import itertools
from os import listdir
from os.path import join, isdir

def download(url):
    dirpath = tempfile.mkdtemp()
    shutil.rmtree(dirpath)
    r = requests.get(url)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall(dirpath)


def get_tldr_pages(dirpath):
    return [join(dirpath, f) for f in listdir(dirpath) if f.endswith('.md')]
 
def parse_file(f):
    def readline(f):
        line = f.readline()
        while line and not line.strip():
            line = f.readline()
        return line.strip()

    commands = []
    with io.open(f, encoding='utf-8') as f:
        main_command = {'cmd': '', 'desc': ''}
        line = readline(f)
        if not line.startswith('#'):
            raise Exception('Parsin err')
        main_command['cmd'] = line[1:].strip().lower()
        while 1:
            line = readline(f)
            if not line.startswith('>'):
                break
            main_command['desc'] += ','+line[1:].strip()
        #commands.append(main_command)
        while line:
            command = {'cmd': '', 'desc': ''}
            if not line.startswith('-'):
                raise Exception('Parsin err')
            command['desc'] = line[1:].strip()
            line = readline(f)
            if not line or not line.startswith('`') or not line.endswith('`'):
                raise Exception('Parsin err')
            command['cmd'] = line[1:-1]
            commands.append(command)
            line = readline(f)
            while line and line.startswith('`') and line.endswith('`'):
                commands.append({'cmd':line[1:-1], 'desc': command['desc']})
                line = readline(f)
    return commands

def process_pages(pages_dir, output_file):
    parsed = list(itertools.chain(*[parse_file(f) for f in get_tldr_pages(pages_dir)]))
    # remove duplicate commands
    # TODO, clean and optimize
    used = [] 
    strings = []
    for el in parsed:
        if not el['cmd'] in used:
            strings.append(el['cmd']+'##'+el['desc'])
            used.append(el['cmd'])
    with io.open(output_file, "w", encoding="utf-8") as text_file:
            text_file.write('\n'.join(sorted(strings)))

repo = '/home/aminehajyoussef/projects/tldr/'
pages_dir_path = join(repo, 'pages')
for d in listdir(pages_dir_path):
    if isdir(join(pages_dir_path, d)):
        process_pages(join(pages_dir_path, d), d+'.txt')

def _get_platform_dirs():
    dirs = ['common']
    platform = sys.platform
    if platform.startswith('linux'):
        dirs.append('linux')
    elif platform.startswith('darwin'):
        dirs.append('osx')
    elif platform.startswith('sunos'):
        dirs.append('sunos')
    return dirs

