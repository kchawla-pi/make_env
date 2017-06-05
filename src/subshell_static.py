#! /usr/bin/env python3
import os
import shutil
import collections as coll


class SubShell(object):
    def __init__(self, root_dir_name='make_env'):
        self.root_dir_name = root_dir_name

    @staticmethod
    def setup_paths(self, is_test=False):
        self.root_dir_path = os.path.split(os.path.split(__file__)[0])[0]
        if is_test:
            suffix = '_test'
        else:
            suffix = ''
        try:
            assert(os.path.split(self.root_dir_path)[1] == self.root_dir_name)
        except AssertionError:
            print('\a',
                  "Error. Possibly invalid path. Please review the following information:",
                  " {} -- Expected root directory name.".format(os.path.split(self.root_dir_path)[1]),
                  " {} -- Supplied root directory name.".format(self.root_dir_name),
                  "\nAutomatically determined path is:\n\t --- {}".format(self.root_dir_path), sep='\n'
                  )
            
        installationpath = os.path.expanduser(os.path.join('~', 'bin'+suffix, 'direnv'))
        Paths = coll.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        self.paths = Paths(
            setupfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath = installationpath,
            installedfile = os.path.join(installationpath, 'direnv_executable'),
            backupspath = os.path.join(installationpath, 'pre_direnv_backups')
            )
        return self.paths

    @staticmethod
    def make_dirs(self):
        # os.makedirs(self.paths.installationpath, exist_ok=True)
        os.makedirs(self.paths.backupspath, exist_ok=True)
        if os.path.exists(self.paths.backupspath):
            return 0
        else:
            return 1

    @staticmethod
    def copy_binary(self, shell, max_attempts=3):
        max_attempts -= 1
        if max_attempts == 0:
            print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
            quit()
        try:
            shutil.copy2(self.paths.setupfile, self.paths.installationpath)
        except FileNotFoundError:
            print("Not found: ", self.paths.setupfile)
            self.paths.setupfile = input("Enter the complete path including name of direnv setup binary:")
            self.copy_binary(shell, self.paths, max_attempts)

    @staticmethod
    def make_exec(self, shell, direnv_paths, max_attempts = 3):
        max_attempts -= 1
        if max_attempts == 0:
            print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
            quit()
        try:
            os.chmod(self.paths.installedfile, 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.
        except FileNotFoundError:
            print("Not found:", self.paths.installedfile)
            print("Copy the direnv binary file to a location of your choice and enter the path here:")
            self.paths.installedfile = input("Enter the complete path including name of direnv installed binary:")
            self.make_exec(shell, self.paths, max_attempts)

    @staticmethod
    def install(self, shell, direnv_paths, max_attempts=3):
        os.makedirs(self.paths.backupspath)
        self.copy_binary(shell, self.paths, max_attempts)
        self.make_exec(shell, self.paths)
        with open(shell.file, 'a') as write_obj:
            write_obj.writelines(shell.command)
        # os.environ["PATH"] += os.pathsep + self.paths['installpath']

    @staticmethod
    def uninstall(self, shell):
        with open(shell.file, 'r') as read_obj:
            contents = read_obj.readlines()
        remove_line_idx = {idx for idx, line_ in enumerate(contents) if shell.command in line_}
        new_contents = [line_ for idx, line_ in enumerate(contents) if idx not in remove_line_idx]
        with open(shell.file, 'w') as write_obj:
            write_obj.write('\n'.join(new_contents))

    @staticmethod
    def check(self, shell):
        try:
            with open(shell.file, 'r') as read_obj:
                contents = read_obj.readlines()
        except FileNotFoundError:
            return False
        direnv_installed = [True for line_ in contents if shell.command in line_]
        if True in direnv_installed:
            return True
        else:
            return False

SubShell().setup_paths()
# direnv.copy_binary()
