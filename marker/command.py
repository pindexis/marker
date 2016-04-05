from . import ansi

def load(filePath):
    lines = []
    try:
        with open(filePath, 'r') as f:
            lines = [Command.deserialize(l.strip('\n').strip('\r')) for l in f.readlines() if l]
    except:
        pass
    return lines

def save(commands, filePath):
    with open(filePath, 'w') as f:
        f.write('\n'.join([m.serialize() for m in commands]))

def add(commands, command):
    remove(commands, command)
    commands.append(command)

def remove(commands, command):
    try:
        match = next(m for m in commands if command.equals(m))
        commands.remove(match)
    except StopIteration:
        pass

class Command(object):
    '''A Command is composed of the shell command string and an optionnal alias'''
    def __init__(self, cmd, alias):
        if not cmd:
            raise "empty command argument"
        self.cmd = cmd
        self.alias = alias
        if not self.alias:
            self.alias = ""
        pass

    def __repr__(self):
        if self.alias and self.alias != self.cmd:
            return self.cmd+" "+ansi.grey_text(self.alias)
        else:
            return self.cmd

    @staticmethod
    def deserialize(str):
        if "##" in str:
            cmd, alias = str.split("##")
        else:
            cmd = str
            alias = ""
        return Command(cmd, alias)

    def serialize(self):
        if self.alias:
            return self.cmd + "##" + self.alias
        else:
            return self.cmd

    def equals(self, mark):
        return self.cmd == mark.cmd and self.alias == mark.alias

