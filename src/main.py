import os

def add_path():
    root = __file__.split(os.sep)[0:-2]
    path = os.path.realpath(os.path.join(*[*root, 'src']))
    os.sys.path.append(path) if path not in os.sys.path \
        else print("{} already in sys.path".format(path))

import make_env
import subshell
import backup
import toolkit

shell = make_env.identify_shell(param_shell='bash', force=False)
sub_shell = subshell.SubShell('test')
sub_shell.make_dirs()
backup.backup(shell, sub_shell)
sub_shell.copy_binary()
sub_shell.make_exec()
