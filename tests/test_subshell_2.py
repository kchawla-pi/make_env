def add_path():
    root = __file__.split(os.sep)[0:-2]
    path = os.path.join(*[*root, 'src'])
    os.sys.path.append(path) if path not in os.sys.path \
        else print("{} already in sys.path".format(path))


# import unittest
import os
import collections
from pprint import pprint


try:
    import toolkit
except ImportError:
    add_path()
    import toolkit
try:
    import subshell
except ImportError:
    add_path()
    import subshell


testee = subshell.SubShell(purpose='test')

tester_file_path = os.path.realpath(__file__)
testee_module_path = os.path.realpath(subshell.__file__)
project_root = os.path.commonpath([tester_file_path, testee_module_path])

suffix = '_test'
installationpath = os.path.expanduser(os.path.join('~', 'bin' + suffix, 'direnv'))
Paths = collections.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
tester_file_path = Paths(
            setupfile=os.path.join(project_root, 'requirements', 'bin'+suffix, 'direnv.linux-amd64'),
            installationpath=installationpath,
            installedfile=os.path.join(installationpath, 'direnv.linux-amd64'),
            backupspath=os.path.join(installationpath, 'pre_direnv_backups')
            )


def test_setup_paths(testee_paths):
    testee_paths = testee.setup_paths()
    return testee_paths
    
    
    
if __name__ == '__main__':
    
    pprint(testee.__dict__)
    testee_paths = testee.setup_paths()
    


























#
#     sub_shell = subshell.sub_shell  #SubShell(purpose='test')
#     suffix = sub_shell.suffix
#     sub_shell.setup_paths()
#     tester_file_path = os.path.realpath(__file__)
#     testee_module_path = os.path.realpath(sub_shell.__file__)
#     project_root = os.path.commonpath([tester_file_path, testee_module_path])
#     shell_names = ('bash', 'zsh', 'fish', 'tcsh')
#     Paths = collections.namedtuple('Paths',
#                                    'setupfile installedfile installationpath backupspath')
#     installationpath = os.path.expanduser(os.path.join('~', 'bin' + suffix, 'direnv'))
#     paths = Paths(
#         setupfile=os.path.join(project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
#         installationpath=installationpath,
#         installedfile=os.path.join(installationpath, 'direnv.linux-amd64'),
#         backupspath=os.path.join(installationpath, 'pre_direnv_backups')
#         )
#
#
# def test_setup_paths(self):
#     print('test_setup_paths')
#     expected = paths
#     observed = subshell.setup_paths()
#
#     try:
#         assertEqual(expected, observed)
#     except AssertionError:
#         print('=' * 10)
#         for e, o in zip(expected, observed):
#             print('e:\t', e, '\n', 'o:\t', o, '\n', sep='')
#         print('=' * 10)
#         raise AssertionError