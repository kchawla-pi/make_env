import os
import collections
import shutil

import make_env
import toolkit

from pprint import pprint
from subshell import SubShell

sub_shell = SubShell('test')
shell = make_env.identify_shell()
switch = False


def backup_shell_config(shell, sub_shell, handle_excep=True):
    BackupError = collections.namedtuple('BackupError', 'shell_config exception file')
    err_log = []
    not_found_files = []
    for file_ in shell['files']:
        
        try:
            shutil.copy2(file_, sub_shell.paths.backupspath)
        except PermissionError as excep:
            toolkit.change_permissions(sub_shell.paths.installationpath, '0o666')
            shutil.copy2(file_, sub_shell.paths.backupspath)
            err_log.append(BackupError(shell_config=1, exception=excep, file=file_))
        except FileNotFoundError as excep:
            err_log.append(BackupError(shell_config=1, exception=excep, file=file_))
            not_found_files.append(file_)
            toolkit.print_exceptions(error=excep, switch=switch)
        else:
            err_log.append(BackupError(shell_config=0, exception=None, file=file_))
            
    if not_found_files:
        print("These files were not found at the specified location and were not backed up:")
        pprint(not_found_files)
    return err_log


def backup_path_var(sub_shell, msg=True):
    BackupError = collections.namedtuple('BackupError', 'path_var')
    curr_path_info = os.environ.get('PATH')
    backup_dst = os.path.join(sub_shell.paths.backupspath, 'PATH_var.txt')
    try:
        with open(backup_dst, 'w') as write_obj:
            write_obj.write(curr_path_info)
    except PermissionError as excep:
        exceptions_list = [excep]
        toolkit.check_make(sub_shell.paths.backupspath)
        toolkit.change_permissions(sub_shell.paths.backupspath, nix_perm='0o666')
        shutil.copy2(shell['file'], sub_shell.paths.backupspath)
    else:
        return BackupError(path_var=0)
        

def backup(shell, sub_shell):
    shell_log = backup_shell_config(shell, sub_shell, handle_excep=True)
    path_log = backup_path_var(sub_shell, msg=True)

    
def restore_shell_config(shell, sub_shell):
    pass


def restore_path_var(shell, sub_shell):
    pass


def restore(shell, sub_shell):
    restore_path_var(shell, sub_shell)
    restore_shell_config(shell, sub_shell)
    
if __name__ == '__main__':
    backup(shell=shell, sub_shell=sub_shell)
    
#TODO: create verify_copy() uing is os.issamefile()