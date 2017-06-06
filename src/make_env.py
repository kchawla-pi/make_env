#! /usr/bin/env python3
import collections as coll
import os
import shutil

# from archived_code.moved_frm_make_env import setup_paths, copy_direnv, make_exec, check_direnv


def identify_shell(param_shell='bash', force='no'):  # default parameter added here for unittests
    # userconfig file locations for various shells & the instructions to be inserted into them:
    ShellHook = coll.namedtuple('ShellHook', 'name command files')
    shell_hooks = {'bash': ShellHook(name='bash', command='eval "$(direnv hook bash)"\n',
                                     files=("~/.bashrc", "~/.bash_profile", "~/.profile")),
                   'zsh': ShellHook(name='zsh', command='eval "$(direnv hook zsh)"\n',
                                    files=("~/.zshrc", "~/.zprofile")),
                   'fish': ShellHook(name='fish', command='eval (direnv hook fish)\n',
                                     files=("~/.config/fish/config.fish",)),
                   'tcsh': ShellHook(name='tcsh', command='eval `direnv hook tcsh`\n',
                                     files=("~/.cshrc",))
        }

    if force == 'force':
        shell_name = param_shell
        shell_config_file = os.path.realpath(os.path.expanduser(
            shell_hooks[shell_name].files)) + '1'  # +1 prevents overwriting shell config file during dev
        shell = {'name': shell_name,
                 'command': shell_hooks[shell_name].command,
                 'file': shell_config_file}
        return shell

    shell_name = os.environ.get('SHELL', 'bash').split(os.sep)[-1]
    shell_config_files = tuple(os.path.realpath(os.path.expanduser(file_))
                               for file_ in shell_hooks[shell_name].files if os.path.exists(file_))
    # shell_config_files = os.path.realpath(os.path.expanduser(shell_hooks[shell_name].files)) + '1'  # +1 prevents overwriting shell config file during dev
    shell = {'name': shell_name,
             'command': shell_hooks[shell_name].command,
             'files': shell_config_files
             }
    return shell

identify_shell()
#TODO: direnv is a good candidate for a Class. maybe backup+restore in one too. Shell?