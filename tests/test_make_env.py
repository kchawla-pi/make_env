import unittest
import os
import collections as coll

import archived_code.moved_frm_make_env


core_path = os.path.realpath(os.path.join(__file__, os.pardir, os.pardir, 'src'))
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
        return_actual = archived_code.moved_frm_make_env.setup_paths()
        self.assertEqual(len(return_actual), len(return_expected))
        for i in range(0, len(return_actual)):
            key = keys_list[i]
            expected_val = return_expected[key]
            actual_val = return_actual[key]
            try:
                self.assertEqual(expected_val, actual_val)
            except:
                print("ERROR: Assertion failure: Values not equal.")
                print("expect -- {}: {}".format(key, expected_val))
                print("actual -- {}: {}".format(key, actual_val))


    def test_identify_shell(self):
        ShellHook =   coll.namedtuple('ShellHook', 'name command file')
        shell_hooks = (ShellHook(name='bash', command='eval "$(direnv hook bash)"\n', file="~/.bashrc"),
                       ShellHook(name='zsh', command='eval "$(direnv hook zsh)"\n', file="~/.zshrc"), 
                       ShellHook(name='fish', command='eval (direnv hook fish)\n', file="~/.config/fish/config.fish"), 
                       ShellHook(name='tcsh', command='eval `direnv hook tcsh`\n', file="~/.cshrc")
                       )
        for shell_ in shell_hooks:
            actual = me.identify_shell(shell_.name, 'force')
            
            self.assertEqual(actual['name'], shell_.name)
            self.assertEqual(actual['command'], shell_.command)
            shell_config_file = os.path.realpath(os.path.expanduser(shell_.file)) + '1'
            self.assertEqual(actual['file'], shell_config_file)


if __name__ == '__main__':
    unittest.main()
