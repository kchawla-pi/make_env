def add_path():
    root = __file__.split(os.sep)[0:-2]
    path = os.path.join(*[*root, 'src'])
    os.sys.path.append(path) if path not in os.sys.path \
        else print("{} already in sys.path".format(path))
        

import unittest
import os
import collections
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


class TestSetupPaths(unittest.TestCase):
    """
    Tests for Class SubShell
    """

    def setUp(self):
        self.subshell = subshell.SubShell(purpose='test')
        self.suffix = self.subshell.suffix
        self.subshell.setup_paths()
        tester_file_path = os.path.realpath(__file__)
        testee_module_path = os.path.realpath(subshell.__file__)
        self.project_root = os.path.commonpath([tester_file_path, testee_module_path])
        self.shell_names= ('bash', 'zsh', 'fish', 'tcsh')
        Paths = collections.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        installationpath = os.path.expanduser(os.path.join('~', 'bin'+self.suffix, 'direnv'))
        self.paths = Paths(
            setupfile=os.path.join(self.project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath=installationpath,
            installedfile=os.path.join(installationpath, 'direnv.linux-amd64'),
            backupspath=os.path.join(installationpath, 'pre_direnv_backups')
            )

    def test_setup_paths(self):
        print('test_setup_paths')
        expected = self.paths
        observed = self.subshell.setup_paths()
        
        try:
            self.assertEqual(expected, observed)
        except AssertionError:
            print('=' * 10)
            for e,o in zip(expected, observed):
                print('e:\t', e, '\n', 'o:\t', o, '\n', sep='')
            print('=' * 10)
            raise AssertionError


class TestMakeDirs(unittest.TestCase):
    """
    Tests for Class SubShell
    """
    
    def setUp(self):
        self.subshell = subshell.SubShell(purpose='test')
        self.suffix = self.subshell.suffix
        self.subshell.setup_paths()
        tester_file_path = os.path.realpath(__file__)
        testee_module_path = os.path.realpath(subshell.__file__)
        self.project_root = os.path.commonpath([tester_file_path, testee_module_path])
        self.shell_names = ('bash', 'zsh', 'fish', 'tcsh')
        Paths = collections.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        installationpath = os.path.expanduser(os.path.join('~', 'bin' + self.suffix, 'direnv'))
        self.paths = Paths(
            setupfile=os.path.join(self.project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath=installationpath,
            installedfile=os.path.join(installationpath, 'direnv.linux-amd64'),
            backupspath=os.path.join(installationpath, 'pre_direnv_backups')
            )
        
    def test_make_dirs(self):
        print('test_make_dirs')
        # try:
        #     self.assertFalse(os.path.exists(self.subshell.paths.installationpath))
        # except AssertionError:
        #     toolkit.cleanup_tree(os.path.split(self.subshell.paths.installationpath)[0], handle_exceptions=False)
        # finally:
        #     self.assertFalse(os.path.exists(self.subshell.paths.installationpath))
        toolkit.change_permissions(os.path.split(self.paths.installationpath)[0], handle_exceptions=False, notify_init=True)
        toolkit.cleanup_tree(os.path.split(self.paths.installationpath)[0], handle_exceptions=False, notify_init=True, notify_outcome=True)
        self.subshell.make_dirs()
        self.assertTrue(os.path.exists(self.paths.installationpath))
        self.assertTrue(os.path.exists(self.paths.backupspath))
        
        # print(os.path.exists(os.path.exists(self.subshell.paths.backupspath)),\
        #       self.subshell.paths.backupspath)


class TestCopyBinary(unittest.TestCase):
    """
    Tests for Class SubShell
    """
    
    def setUp(self):
        self.subshell = subshell.SubShell(purpose='test')
        self.suffix = self.subshell.suffix
        self.subshell.setup_paths()
        self.subshell.make_dirs()
        tester_file_path = os.path.realpath(__file__)
        testee_module_path = os.path.realpath(subshell.__file__)
        self.project_root = os.path.commonpath([tester_file_path, testee_module_path])
        self.shell_names = ('bash', 'zsh', 'fish', 'tcsh')
        Paths = collections.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        installationpath = os.path.expanduser(os.path.join('~', 'bin' + self.suffix, 'direnv'))
        self.paths = Paths(
            setupfile=os.path.join(self.project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath=installationpath,
            installedfile=os.path.join(installationpath, 'direnv.linux-amd64'),
            backupspath=os.path.join(installationpath, 'pre_direnv_backups')
            )
    
    def test_copy_binary(self):
        print('test_copy_binary')
        try:
            self.assertFalse(os.path.exists(self.subshell.paths.installedfile))
        except Exception as excep:
            toolkit.change_permissions(self.subshell.paths.installedfile)
            os.remove(self.subshell.paths.installedfile)
            # raise excep
        exceptions_list = self.subshell.copy_move_binary(max_attempts=2)
        try:
            self.assertTrue(os.path.exists(self.subshell.paths.installedfile))
        except AssertionError:
            print(exceptions_list)
            raise AssertionError
        
        pass
        # toolkit.cleanup_tree(os.path.split(self.subshell.paths.installationpath)[0])


if __name__=='__main__':
    # unittest.main()
    test_make_dirs = TestMakeDirs
    test_make_dirs.test_make_dirs()
    pass