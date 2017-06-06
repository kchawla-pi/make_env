def add_path():
    root = __file__.split(os.sep)[0:-2]
    path = os.path.realpath(os.path.join(*[*root, 'src']))
    os.sys.path.append(path) if path not in os.sys.path \
        else print("{} already in sys.path".format(path))


# import unittest
import os
import collections
import shutil
from pprint import pprint
import subprocess


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


# Establishing necessary paths to run the tests.
def setup_tests():
    tester_file_path = os.path.realpath(__file__)
    testee_module_path = os.path.realpath(subshell.__file__)
    project_root = os.path.commonpath([tester_file_path, testee_module_path])
    
    # setting up path for benchmarks .
    suffix = '_test'
    installationpath = os.path.expanduser(os.path.join('~', 'bin' + suffix, 'direnv'))
    Paths = collections.namedtuple('Paths', 'setupfile copiedfile installedfile installationpath backupspath')
    benchmark_paths = Paths(
                setupfile=os.path.join(project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
                copiedfile=os.path.join(project_root, 'requirements', 'bin', 'direnv'),
                installationpath=installationpath,
                installedfile=os.path.join(installationpath, 'direnv'),
                backupspath=os.path.join(installationpath, 'pre_direnv_backups')
                )
    assert([False, False, True, True, True] == ['test' in path for path in benchmark_paths])
    return benchmark_paths

    
def test_setup_paths(testee, benchmark_paths):
    assert(benchmark_paths == testee.setup_paths())
    return 'Passed.'
    
    
def test_make_dirs(testee):
    toolkit.check_remove(testee.paths.installationpath)
    testee.make_dirs()
    assert(os.path.exists(testee.paths.backupspath) is True)
    return 'Passed.'

    
def test_copy_binary(testee):
    toolkit.check_remove(testee.paths.installedfile)
    toolkit.check_make(testee.paths.installationpath)
    testee.copy_move_binary(task='both')
    assert(os.path.isfile(testee.paths.copiedfile) is True)
    return 'Passed.'


def test_move_binary(testee):
    toolkit.check_remove(testee.paths.installedfile)
    testee.move_binary(max_attempts=3)
    assert(os.path.isfile(testee.paths.installedfile) is True)
    return 'Passed.'
    
    
def test_make_exec(testee):
    if os.name == 'nt':
        return 'NotImplemented in nt'
    testee.copy_move_binary()
    os.chmod(testee.paths.installedfile, 0o666)
    pre_fn_permit = toolkit.get_file_permission_via_shell(testee.paths.installedfile, in_form='code')
    assert(pre_fn_permit == '0o666')
    testee.make_exec()
    post_fn_permit = toolkit.get_file_permission_via_shell(testee.paths.installedfile, in_form='code')
    assert(post_fn_permit == '0o111')
    return 'Passed.'
    
   
if __name__ == '__main__':
    incr = toolkit.increment(start=1, step=1)
    testee = subshell.SubShell(purpose='test')  # Instance of SubShell, which will be tested
    benchmark_paths = setup_tests()
    print(next(incr), test_setup_paths(testee, benchmark_paths))
    print(next(incr), test_make_dirs(testee))
    print(next(incr), test_copy_binary(testee))
    print(next(incr), test_make_exec(testee))
    print(next(incr), test_move_binary(testee))

    