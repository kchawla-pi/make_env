#! /usr/bin/env python3
import os
import shutil
import collections as coll

def setup_paths():
    P = os.path  # for ease of viewong & typing. Used a lot in this function.
    setup_file_path = P.realpath(P.join(__file__, P.pardir, P.pardir, 'requirements', 'bin', 'direnv.linux-amd64'))
    installation_path = os.path.expanduser(os.path.join('~','bin','direnv'))
    installed_file_path = os.path.join(installation_path, 'direnv')
    backups_path = os.path.join(installation_path, 'pre_direnv_backups')
    keys_list = ['setupfile', 'installedfile', 'installpath', 'backupspath']
    values_list = [setup_file_path, installed_file_path, installation_path, backups_path]
    direnv_paths = dict(zip(keys_list, values_list))
    return direnv_paths


def identify_shell(param_shell='bash', force='no'):  # default parameter added here for unittests
    # userconfig file locations for various shells & the instructions to be inserted into them:
    ShellHook = coll.namedtuple('ShellHook', 'name command file')
    shell_hooks = {'bash': ShellHook(name='bash', command='eval "$(direnv hook bash)"\n', file="~/.bashrc"),
                   'zsh': ShellHook(name='zsh', command='eval "$(direnv hook zsh)"\n', file="~/.zshrc"),
                   'fish': ShellHook(name='fish', command='eval (direnv hook fish)\n', file="~/.config/fish/config.fish"),
                   'tcsh': ShellHook(name='tcsh', command='eval `direnv hook tcsh`\n', file="~/.cshrc")
        }

    if force == 'force':
        shell_name = param_shell
        shell_config_file = os.path.realpath(os.path.expanduser(
            shell_hooks[shell_name].file)) + '1'  # +1 prevents overwriting shell config file during dev
        shell = {'name': shell_name,
                 'command': shell_hooks[shell_name].command,
                 'file': shell_config_file}
        return shell

    try:
        shell_name = os.environ.get('SHELL').split(os.sep)[-1]
    except:
        if os.name != 'nt':
            print("$SHELL variable not found. Defaulting to bash.")
        shell_name = 'bash'
    finally:
        if shell_name not in shell_hooks.keys():
            print("Unknown shell name:", shell_name)
            print("Defaulting to bash.")
            shell_name = 'bash'

    shell_config_file = os.path.realpath(os.path.expanduser(shell_hooks[shell_name].file)) + '1'  # +1 prevents overwriting shell config file during dev
    shell = {'name': shell_name,
             'command': shell_hooks[shell_name].command,
             'file': shell_config_file}
    return shell


def backup_shell_config(shell, direnv_paths, msg=True):
    BackupError = coll.namedtuple('BackupError', 'shell_config')
    backup_dst = os.path.join(direnv_paths['backupspath'], os.path.split(shell['file'])[1], '_pre_direnv_bkup')
    try:
        shutil.copy2(shell['file'], backup_dst)
        return BackupError(shell_config=0)
    except:
        if msg: print("{} backup unsuccessful. Consieder making a manual backup.".format(shell['file']))
        return BackupError(shell_config=1)


def backup_path_var(direnv_paths, msg=True):
    BackupError = coll.namedtuple('BackupError', 'path_var')
    curr_path_info = os.environ.get('PATH')
    backup_dst = os.path.join(direnv_paths['backupspath'], 'PATH_var', '_pre_direnv_bkup')
    try:
        with open(backup_dst, 'w') as write_obj:
            write_obj.write(curr_path_info)
            return BackupError(path_var=0)
    except:
        if msg: print("Current $PATH backup unsuccessful. Consider making a manual backup.")
        return BackupError(path_var=1)


def copy_direnv(shell, direnv_paths, max_attempts=3):
    max_attempts -= 1
    if max_attempts == 0:
        print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        quit()
    try:
        shutil.copy2(direnv_paths['setupfile'], direnv_paths['installpath'])
    except FileNotFoundError:
        print("Not found: ", direnv_paths['setupfile'])
        direnv_paths['setupfile'] = input("Enter the complete path including name of direnv setup binary:")
        copy_direnv(shell, direnv_paths, max_attempts)


def make_exec(shell,direnv_paths, max_attempts = 3):
    max_attempts -= 1
    if max_attempts == 0:
        print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        quit()
    try:
        os.chmod(direnv_paths['installedfile'], 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.
    except FileNotFoundError:
        print("Not found:", direnv_paths['installedfile'])
        print("Copy the direnv binary file to a location of your choice and enter the path here:")
        direnv_paths['installedfile'] = input("Enter the complete path including name of direnv installed binary:")
        make_exec(shell, direnv_paths, max_attempts)


def install_direnv(shell, direnv_paths, max_attempts=3):
    os.makedirs(direnv_paths['backupspath'])
    copy_direnv(shell, direnv_paths, max_attempts)
    make_exec(shell, direnv_paths)
    with open(shell['file'], 'a') as write_obj:
        write_obj.writelines(shell['command'])
    # os.environ["PATH"] += os.pathsep + direnv_paths['installpath']


def uninstall_direnv(shell):
    with open(shell['file'], 'r') as read_obj:
        contents = read_obj.readlines()
    remove_line_idx = {idx for idx, line_ in enumerate(contents) if shell['command'] in line_}
    new_contents = [line_ for idx, line_ in enumerate(contents) if idx not in remove_line_idx]
    with open(shell['file'], 'w') as write_obj:
        write_obj.write('\n'.join(new_contents))


def check_direnv(shell):
    try:
        with open(shell['file'], 'r') as read_obj:
            contents = read_obj.readlines()
    except FileNotFoundError:
        return False
    direnv_installed = [True for line_ in contents if shell['command'] in line_]
    if True in direnv_installed:
        return True
    else:
        return False


def new_subshell(target_dir, subshell_name):
    direnv_config_init = "export subshellname=".join(subshell_name)
    target_path = os.sep.join(target_dir, ".envrc")
    with open(target_path, 'w') as write_obj:
        write_obj.writelines(direnv_config_init)


def backup(shell, direnv_paths):
    backup_shell_config(shell, direnv_paths, msg=True)
    backup_path_var(direnv_paths, msg=True)


def direnv_handler(task='check'):
    direnv_paths = setup_paths()
    shell = identify_shell()
    installed = check_direnv(shell)

    if task == 'install':
        if installed:  # uninstall existing installation first
            uninstall_direnv(shell, direnv_paths)
        backup(shell, direnv_paths)
        install_direnv(shell, direnv_paths)
        installed = check_direnv(shell)
    elif task == 'uninstall' and installed:
        uninstall_direnv(shell, direnv_paths)
        installed = check_direnv(shell)
    print("'direnv' is installed at", direnv_paths['installpath']) if installed else print("'direnv' is not installed.")


if __name__ == '__main__':
    direnv_handler()
    # new_subshell(target_dir, subshell_name)

#TODO: direnv is a good candidate for a Class. maybe backup+restore in one too. Shell?