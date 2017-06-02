import os
import collections
import shutil
from subshell import SubShell
import make_env


sub_shell = SubShell('test')
shell = make_env.identify_shell()
# print(shell)  # debug


def backup_shell_config(shell, sub_shell, handle_excep=True):
    # if handle_excep:
    #     msg = "{} backup unsuccessful. Consider making a manual backup.".format(shell['file'])
    # else:
    #     msg = ''
    BackupError = collections.namedtuple('BackupError', 'shell_config')
    # print(sub_shell.paths.backupspath)  # debug
    # print(os.path.split(shell['file'])[1])  # debug
    # print(shell['file'])  # debug
    shutil.copy2(shell['file'], sub_shell.paths.backupspath)
    return BackupError(shell_config=0)
    
    ## possible exceptions: See /logs/Errors - backup.txt
    
    ## will add handling later, incl toolkit.errorhandlefunction
    # try:
    # except FileNotFoundError as excep:
    #     print(excep)
    #     reattempt_src = "The file {} was not found. Enter the complete filepath here. :".format(shell['file'])
    #     try:
    #         shutil.copy2(reattempt_src, sub_shell.paths.backupspath)
    #     except Exception as excep:
    #         print(excep, '/n', )
    #
    
            #     shutil.copy2(shell['file'], backup_dst)
    #     return BackupError(shell_config=0)
    # except:
    #     if msg: print("{} backup unsuccessful. Consider making a manual backup.".format(shell['file']))
    #     return BackupError(shell_config=1)


def backup_path_var(sub_shell, msg=True):
    BackupError = collections.namedtuple('BackupError', 'path_var')
    curr_path_info = os.environ.get('PATH')
    backup_dst = os.path.join(sub_shell.paths.backupspath, 'PATH_var')
    with open(backup_dst, 'w') as write_obj:
        write_obj.write(curr_path_info)
        return BackupError(path_var=0)
    # try:
    #     with open(backup_dst, 'w') as write_obj:
    #         write_obj.write(curr_path_info)
    #         return BackupError(path_var=0)
    # except:
    #     if msg: print("Current $PATH backup unsuccessful. Consider making a manual backup.")
    #     return BackupError(path_var=1)


def backup(shell, sub_shell):
    backup_shell_config(shell, sub_shell, handle_excep=True)
    backup_path_var(sub_shell, msg=True)

    
    
    
    
