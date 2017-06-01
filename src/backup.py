import os
import collections
from subshell import SubShell


sub_shell = SubShell('test')

def backup_shell_config(shell, direnv_paths, msg=True):
    BackupError = collections.namedtuple('BackupError', 'shell_config')
    backup_dst = os.path.join(direnv_paths['backupspath'], os.path.split(shell['file'])[1], '_pre_direnv_bkup')
    try:
        shutil.copy2(shell['file'], backup_dst)
        return BackupError(shell_config=0)
    except:
        if msg: print("{} backup unsuccessful. Consieder making a manual backup.".format(shell['file']))
        return BackupError(shell_config=1)


def backup_path_var(direnv_paths, msg=True):
    BackupError = collections.namedtuple('BackupError', 'path_var')
    curr_path_info = os.environ.get('PATH')
    backup_dst = os.path.join(direnv_paths['backupspath'], 'PATH_var', '_pre_direnv_bkup')
    try:
        with open(backup_dst, 'w') as write_obj:
            write_obj.write(curr_path_info)
            return BackupError(path_var=0)
    except:
        if msg: print("Current $PATH backup unsuccessful. Consider making a manual backup.")
        return BackupError(path_var=1)

