import unittest
import os
import shutil
from toolkit import debug_print
import toolkit
import subshell_class as src
import make_env as me
import collections as coll
# from scratch_pad import SubShell


class MyTestCase(unittest.TestCase):
    """
    Tests for Class SubShell
    """

    def setUp(self):
        self.subshell = src.SubShell()
        self.subshell.setup_paths(is_test=True)
        self.project_root = os.path.commonpath([__file__, src.__file__])
        debug_print('setup')
        self.shell_names= ('bash', 'zsh', 'fish', 'tcsh')

    def test_setup_paths(self):
        installationpath = os.path.expanduser(os.path.join('~', 'bin', 'direnv'))
        Paths = coll.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        expected = Paths(
            setupfile=os.path.join(self.project_root, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath=installationpath,
            installedfile=os.path.join(installationpath, 'direnv_executable'),
            backupspath=os.path.join(installationpath, 'pre_direnv_backups')
            )
        observed = self.subshell.setup_paths()
        debug_print('\ntest_setup_path:', self.subshell.paths)
        self.assertEqual(expected, observed)
        

    def test_make_dirs(self):
        debug_print('\ntest_make_dirs:', self.subshell.paths)
        
        self.assertFalse(os.path.exists(self.subshell.paths.backupspath))
        self.assertFalse(os.path.exists(self.subshell.paths.installationpath))
        self.subshell.make_dirs()
        self.assertTrue(os.path.exists(self.subshell.paths.installationpath))
        self.assertTrue(os.path.exists(self.subshell.paths.backupspath))
        
    def tearDown(self):
        debug_print('\nteardown:', self.subshell.paths)
        toolkit.cleanup_tree(os.path.split(self.subshell.paths.installationpath)[0])
        self.assertFalse(os.path.exists(self.subshell.paths.backupspath))
        self.assertFalse(os.path.exists(self.subshell.paths.installationpath))
    
    def test_copy_binary(self):
        pass
        debug_print('test_copy_binary')
        # print(1, os.path.isfile(self.subshell.paths.setupfile))
        # print(5, os.path.exists(self.subshell.paths.installationpath))
        # shutil.copy2(self.subshell.paths.setupfile, self.subshell.paths.installationpath)
        # print(3, os.path.exists(self.subshell.paths.installedfile))
        # expected =


if __name__=='__main__':
    unittest.main()
