#! /usr/bin/env python3
import os
import shutil


def setup_paths():
    P = os.path
    direnv_bin = P.realpath(P.join(__file__, P.pardir, P.pardir, 'requirements', 'bin', 'direnv.linux-amd64'))
    return direnv_bin


def identify_shell():

    # names & userconfig file locations of various shells. bash is default.
    shell_hooks = {'bash': ('eval "$(direnv hook bash)"\n', "~/.bashrc"),
               'zsh': ('eval "$(direnv hook zsh)"\n', "~/.zshrc"),
               'fish': ('eval (direnv hook fish)\n', "~/.config/fish/config.fish"),
               'tcsh': ('eval `direnv hook tcsh`\n', "~/.cshrc")
               }
    shell_name = 'bash'
    try:
        shell_name = os.environ.get('SHELL').split(os.sep)[-1]
    except:
        print("$SHELL variable not found. Defaulting to bash.")
    if shell_name not in shell_hooks.keys():
        print("Unknown shell name:", shell_name)
        print("Defaulting to bash.")
        shell_name = 'bash'
    P = os.path
    shell_config_file = P.realpath(P.expanduser(shell_hooks[shell_name][1]))+'1'  # +1 to prevent overwriting/clutterring current .bashrc in posix.
    shell = {'name':shell_name,
            'insert':shell_hooks[shell_name][0],
            'file': shell_config_file}
    return shell


def backup_shell_config(shell):
    dst = ''.join([shell['file'], '_pre_direnv_bkup'])
    shutil.copy2(shell['file'], dst)


def install_direnv(shell, direnv_bin):
    with open(shell['file'] , 'a') as write_obj:
        write_obj.writelines(shell['insert'])
    try:
        os.chmod(direnv_bin, 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.
    except FileNotFoundError:
        print("The path to executable file for 'direnv' was computed to be {}.\n However the file can not be found at this location.".format(direnv_bin))
        direnv_bin = input("Enter the full path to 'direnv.linux-amd64', or press ENTER to abort.\nEnter path>>")
        try:
            os.chmod(direnv_bin, 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.
        except FileNotFoundError:
            print("ERROR: The binary executable for 'direnv.linux-amd64' not found.\n Installation Aborted.")


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
    direnv_bin = setup_paths()
    shell = identify_shell()
    installed = check_direnv(shell)

    if task == 'install' and installed is False:
        backup_shell_config(shell)
        install_direnv(shell, direnv_bin)
        print("'direnv' installed.") if installed else print("'direnv' not installed.")
    elif task == 'reinstall':
        if installed is True:
            uninstall_direnv(shell, direnv_bin)
        install_direnv(shell, direnv_bin)
    elif task == 'uninstall' and installed is True:
        uninstall_direnv(shell, direnv_bin)
    else:
        print("'direnv' is installed.") if installed else print("'direnv' is not installed.")


if __name__ == '__main__':
    direnv_handler('uninstall')
    # new_subshell(target_dir, subshell_name)