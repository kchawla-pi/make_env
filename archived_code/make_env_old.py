#! /usr/bin/env python3
import collections as coll
import os
import shutil

# from archived_code.moved_frm_make_env import setup_paths, copy_direnv, make_exec, check_direnv


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