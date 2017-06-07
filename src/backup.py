import os
import collections
import shutil
from subshell import SubShell
import make_env
import toolkit

sub_shell = SubShell('test')
shell = make_env.identify_shell()


def backup_shell_config(shell, sub_shell, handle_excep=True):
    BackupError = collections.namedtuple('BackupError', 'shell_config exception file')
    err_log = []
    for file_ in shell['files']:
        
        try:
            shutil.copy2(file_, sub_shell.paths.backupspath)
        except PermissionError as excep:
            exceptions_list = [excep]
            toolkit.change_permissions(sub_shell.paths.installationpath, '0o666')
            shutil.copy2(file_, sub_shell.paths.backupspath)
            err_log.append(BackupError(shell_config=1, exception=excep, file=file_))
        else:
            err_log.append(BackupError(shell_config=0, exception=None, file=file_))
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
        # try:
    #     with open(backup_dst, 'w') as write_obj:
    #         write_obj.write(curr_path_info)
    #         return BackupError(path_var=0)
    # except:
    #     if msg: print("Current $PATH backup unsuccessful. Consider making a manual backup.")
    #     return BackupError(path_var=1)


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