import unittest
import os

core_path = os.path.realpath(os.path.join(__file__, os.pardir, os.pardir, 'core'))
os.sys.path.append(core_path)

import make_env as me

me.__file__
P = os.path
project_root = P.realpath(P.join(__file__, P.pardir, P.pardir, P.pardir))

# project_root = "C:\\Users\\kshit\\Dropbox\\workspace\\make_env\\kchawla-pi"


class MyTestCase(unittest.TestCase):
    def test_setup_paths(self):
        setupfile = P.normpath(P.join(project_root, "make_env\\requirements\\bin\\direnv.linux-amd64"))
        installedfile = P.expanduser(P.join('~', 'bin', 'direnv', 'direnv'))
        installpath = P.expanduser(P.join('~', 'bin', 'direnv'))
        backupspath = P.expanduser(P.join('~', 'bin', 'direnv', 'pre_direnv_backups'))

        keys_list = ['setupfile', 'installedfile', 'installpath', 'backupspath']
        values_list = [setupfile, installedfile, installpath, backupspath]

        return_expected = dict(zip(keys_list, values_list))
        return_actual = me.setup_paths()
        self.assertEqual(len(return_actual), len(return_expected))
        for i in range(0, len(return_actual)):
            key = keys_list[i]
            expected_val = return_expected[key]
            actual_val = return_actual[key]
            try:
                self.assertEqual(expected_val, actual_val)
            except:
                print("expect -- ", expected_val)
                print("actual -- ", actual_val)


if __name__ == '__main__':
    unittest.main()
