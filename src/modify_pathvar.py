#
# # 45 wayne st, jc
# # nari
# # liberty realty


import os
from pprint import pprint
from subshell import SubShell
import toolkit
import collections


def _open_shell_config_file(configfile):
    with open(configfile, 'r') as read_obj:
        shell_str = read_obj.read()
    return shell_str


def _find_path_region(shellstring):
    PathRegionInfo = collections.namedtuple('PathRegionInfo', 'begin_tag end_tag begin_idx end_idx')
    begin_tag = 'PATH="'
    end_tag = ':$PATH'
    
    path_region = PathRegionInfo(begin_tag=begin_tag, end_tag=end_tag,
                                 begin_idx=shellstring.find(begin_tag) + len(begin_tag),
                                 end_idx=shellstring.find(end_tag) + len(end_tag)
                                 )
    return path_region


def _split_shell(shellstring, path_region):
    ShellConfigSplit = collections.namedtuple('ShellConfigSplit', 'before_paths paths after_paths')
    shell_split = ShellConfigSplit(before_paths=shellstring[: path_region.begin_idx],
                                   paths=shellstring[path_region.begin_idx: path_region.end_idx],
                                   after_paths=shellstring[path_region.end_idx:]
                                   )
    return shell_split


def _add_path(shell_split, addin):
    shell_whole = ''.join([shell_split.before_paths, addin, ':',
                           shell_split.paths, shell_split.after_paths])
    return shell_whole


def _write_to_sh_file(configfile, shell_whole):
    with open(configfile, 'w') as write_obj:
        write_obj.write(shell_whole)


def add_to_path(configfile, addin):
    shell_str = _open_shell_config_file(configfile)
    path_region = _find_path_region(shell_str)
    shell_split = _split_shell(shell_str, path_region)
    shell_whole = _add_path(shell_split, addin=addin)
    _write_to_sh_file(filename=sh_conf_file, shell_whole=shell_whole)

if __name__ == '__main__':
    shell_args = os.sys.argv
    try:
        sh_conf_file = shell_args[1]
    except IndexError:
        sh_conf_file = os.path.join(
            os.path.split(os.path.split(shell_args[0])[0])[0],
            'tests', 'data', '.profile_test'
            )
    add_to_path(configfile=sh_conf_file, addin="$HOME/bin/direnv")
