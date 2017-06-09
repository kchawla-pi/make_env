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

print("\nMaking directories...")
sub_shell.make_dirs()

print("\nBacking up PATH and configuration files...")
backup.backup(shell, sub_shell)

print("\nPreparing binary file for installation...")
sub_shell.copy_move_binary(task='both')

print("\nInstalling Binary file...")
sub_shell.move_binary(force=True)

print("\nGranting execution permissions...")
sub_shell.make_exec()

# sub_shell.read_path_file()
# sub_shell.add_to_path()