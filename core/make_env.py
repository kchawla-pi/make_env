#! /usr/bin/env python3
import os
import shutil


def setup_paths():
    P = os.path
    setup_file_path = P.realpath(P.join(__file__, P.pardir, P.pardir, 'requirements', 'bin', 'direnv.linux-amd64'))
    installation_path = os.path.expanduser(os.path.join('~','bin','direnv'))
    installed_file_path = os.path.join(installation_path, 'direnv.linux-amd64')
    backups_path = os.path.join(installation_path, 'pre_direnv_backups')
    keys_list = ['setupfile', 'installedfile', 'installpath', 'backupspath']
    values_list = [setup_file_path, installed_file_path, installation_path, backups_path]
    direnv_paths = dict(zip(keys_list, values_list))
    return direnv_paths


def identify_shell():
    # userconfig file locations for various shells & the instructions to be inserted into them:
    shell_hooks = {'bash': ('eval "$(direnv hook bash)"\n', "~/.bashrc"),
                   'zsh': ('eval "$(direnv hook zsh)"\n', "~/.zshrc"),
                   'fish': ('eval (direnv hook fish)\n', "~/.config/fish/config.fish"),
                   'tcsh': ('eval `direnv hook tcsh`\n', "~/.cshrc")
                   }
    shell_name = 'bash'  # default shell is 'bash'.
    try:
        shell_name = os.environ.get('SHELL').split(os.sep)[-1]
    except:
        print("$SHELL variable not found. Defaulting to bash.")
    if shell_name not in shell_hooks.keys():
        print("Unknown shell name:", shell_name)
        print("Defaulting to bash.")
        shell_name = 'bash'
    shell_config_file = os.path.realpath(os.path.expanduser(shell_hooks[shell_name][1])) + '1'  # +1 prevents overwriting shell config file during dev
    shell = {'name': shell_name,
             'insert': shell_hooks[shell_name][0],
             'file': shell_config_file}
    return shell


def backup_shell_config(shell, direnv_paths, msg=True):
    errorcodes = [0, 0]
    try:
        backup_dst = os.path.join(direnv_paths['backupspath'], os.path.split(shell['file'])[1], '_pre_direnv_bkup')
        shutil.copy2(shell['file'], backup_dst)
    except:
        if msg: print("{} backup unsuccessful. Consieder making a manual backup.".format(shell['file']))
        errorcodes[0] = 1
    try:
        curr_path_info = os.environ.get('PATH')
        backup_dst = os.path.join(direnv_paths['backupspath'], 'PATH_var', '_pre_direnv_bkup')
        with open(backup_dst, 'w') as write_obj:
            write_obj.write(curr_path_info)
    except:
        if msg: print("Current $PATH backup unsuccessful. Consider making a manual backup.")
        errorcodes[1] = 1
    return errorcodes


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
        write_obj.writelines(shell['insert'])


def uninstall_direnv(shell):
    with open(shell['file'], 'r') as read_obj:
        contents = read_obj.readlines()
    remove_line_idx = {idx for idx, line_ in enumerate(contents) if shell['insert'] in line_}
    new_contents = [line_ for idx, line_ in enumerate(contents) if idx not in remove_line_idx]
    with open(shell['file'], 'w') as write_obj:
        write_obj.write('\n'.join(new_contents))


def check_direnv(shell):
    with open(shell['file'], 'r') as read_obj:
        contents = read_obj.readlines()
    direnv_installed = [True for line_ in contents if shell['insert'] in line_]
    if True in direnv_installed:
        return True
    else:
        return False


def new_subshell(target_dir, subshell_name):
    direnv_config_init = "export subshellname=".join(subshell_name)
    target_path = os.sep.join(target_dir, ".envrc")
    with open(target_path, 'w') as write_obj:
        write_obj.writelines(direnv_config_init)


def direnv_handler(task='check'):
    direnv_setup_bin = setup_paths()
    shell = identify_shell()
    installed = check_direnv(shell)

    if task == 'install':
        if installed:  # uninstall existing installation first
            uninstall_direnv(shell, direnv_setup_bin)
        backup_shell_config(shell)
        install_direnv(shell, direnv_setup_bin)
        installed = check_direnv(shell)
    elif task == 'uninstall' and installed:
        uninstall_direnv(shell, direnv_setup_bin)
        installed = check_direnv(shell)

    print("'direnv' is installed.") if installed else print("'direnv' is not installed.")
    print("Executable binary location:", direnv_setup_bin)


if __name__ == '__main__':
    direnv_handler('uninstall')
    # new_subshell(target_dir, subshell_name)
