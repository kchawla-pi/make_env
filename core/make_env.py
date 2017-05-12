#! /usr/bin/env python3
import os
import shutil
import os.path as P


def resolve_path(some_path='', *dirs):
    """
    Creates absolute paths using given arguments.
    
    Single Arg:  some_path (default=''): return os.path.realpath(os.expanduser(some_path))
    Multiple Args: *args : return [some_path].extend(args), then same as single arg.
    
    :param some_path: (str)-- accepts a str (dir or relpath) and converts it into a real path
    :param dirs: (tuple)-- accepts variable number of string args
    :return: (str) or (dict)
or     """
    some_path = ''.join(list(str(some_path)))
    some_path.replace('\\', os.sep)
    if len(dirs) == 0:
        return os.path.realpath(os.path.expanduser(some_path))
    # if os.sep in some_path:
    some_path_parts = some_path.split(os.sep)
    some_path_parts.extend(dirs)
    joined_dirs = os.sep.join(some_path_parts)
    return os.path.realpath(os.path.expanduser(joined_dirs))


def setup_paths(root_name ='make_env'):
    script_path = os.path.realpath(__file__)
    path_dirs = script_path.split(os.sep)
    root_idx = max({idx for idx, elem in enumerate(path_dirs) if elem == root_name and path_dirs[idx+1] == 'core'}) + 1
    root_dirs = path_dirs[0:root_idx]
    root_path = os.sep.join(root_dirs)
    rel_dirs = {'direnv': ['requirements', 'bin', 'direnv.linux-amd64']}
    temp_list = root_dirs
    temp_list.extend(rel_dirs['direnv'])
    abs_paths = {'direnv': os.sep.join(temp_list)}
    return abs_paths


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

    shell_config_file = resolve_path(shell_hooks[shell_name][1])+'1'  # +1 to prevent overwriting/clutterring current .bashrc in posix.
    shell_info = {'shell':shell_name,
                        'config':shell_hooks[shell_name][0],
                        'file': shell_config_file}

    return shell_info


def backup_shell_config(shell_info):
    dst = ''.join([shell_info['file'], '_pre_direnv_bkup'])
    shutil.copy2(shell_info['file'], dst)



def install_direnv(shell_info, abs_paths):
    with open(shell_info['file'] , 'a') as write_obj:
        write_obj.writelines(shell_info['config'])
    os.chmod(abs_paths['direnv'], 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.


def uninstall_direnv(shell_info, abs_paths):
    if check_direnv(shell_info) is True:
        with open(shell_info['file'], 'r') as read_obj:
            contents = read_obj.readlines()
        remove_config_idx = [idx for idx, line_ in enumerate(contents) if shell_info['config'] in line_]


def check_direnv(shell_info):
    with open(shell_info['file'], 'r') as read_obj:
        contents = read_obj.readlines()
    direnv_installed = [True for line_ in contents if shell_info['config'] in line_]
    if True in direnv_installed:
        return True
    else:
        return False


def new_subshell(target_dir, subshell_name):
    direnv_config_init = "export subshellname=".join(subshell_name)
    target_path = os.sep.join(target_dir, ".envrc")
    with open(target_path, 'w') as write_obj:
        write_obj.writelines(direnv_config_init)


def direnv_handler(task='check', msg=False):
    abs_paths = setup_paths()
    shell_info = identify_shell(abs_paths)
    installed = check_direnv(shell_info)

    if task == 'install' and installed is False:
        backup_shell_config(shell_info)
        install_direnv(shell_info, abs_paths)
    if task == 'reinstall' and installed is True:
        install_direnv(shell_info, abs_paths)
    if task == 'uninstall' and installed is True:
        uninstall_direnv(shell_info, abs_paths)



if __name__ == '__main__':
    direnv_handler()
    cwd = os.getcwd()
    new_subshell(target_dir, subshell_name)