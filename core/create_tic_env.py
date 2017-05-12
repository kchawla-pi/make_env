#!/python3
import os
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


def identify_shell(abs_path):

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
    shell_setup_info = {'shell':shell_name,
                        'hook':shell_hooks[shell_name][0],
                        'file': shell_config_file}

    return shell_setup_info


def new_subshell(shell_setup_info, abs_paths):

    with open(shell_setup_info['file'] , 'a') as file_obj:
        file_obj.writelines(shell_setup_info['hook'])

    os.chmod(abs_paths['direnv'], 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.


def identify_subshell_installation():


def main():
    abs_paths = setup_paths()
    identify_shell(abs_paths)

if __name__ == '__main__':
    main()