#! /usr/bin/env python3
import os
import stat
import shutil
import make_env
import collections
try:
    import toolkit
except ImportError:
    os.sys.path.append(os.path.split(__file__)[0])
    import toolkit

# shell = make_env.identify_shell()

class SubShell(object):
    def __init__(self, purpose='check', rootname='make_env'):
        self.shell = make_env.identify_shell()
        self.purpose = purpose
        self.rootname = rootname
        if purpose == 'test':
            self.suffix = '_test'
        else:
            self.suffix = ''
        self.paths = self.setup_paths()
        # self.purposes = {
        #     'install': self.install,
        #     'uninstall': self.uninstall,
        #     'check': self.check,
        #     'test': self.shellfile_for_tests
        #     }
        # quit()
        
    def shellfile_for_tests(self):
        self.suffix = '_test'
        self.shell['file'] = self.shell['file'] + self.suffix
        
    def setup_paths(self):
        self.root_dir_path = os.path.realpath(os.path.split(os.path.split(__file__)[0])[0])
        root_name_from_path = os.path.split(self.root_dir_path)[1]
        try:
            assert( root_name_from_path == self.rootname)
        except AssertionError:
            print("Error. Possibly invalid path. Please review the following information:",
                  " {} -- Expected root directory name.".format(root_name_from_path),
                  " {} -- Supplied root directory name.".format(self.rootname),
                  "\nAutomatically determined path is:\n\t --- {}".format(self.root_dir_path), sep='\n'
                  )
            
        installationpath = os.path.expanduser(os.path.join('~', 'bin'+self.suffix, 'direnv'))
        Paths = collections.namedtuple('Paths', 'setupfile installedfile installationpath backupspath')
        self.paths = Paths(
            setupfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv.linux-amd64'),
            installationpath = installationpath,
            installedfile = os.path.join(installationpath, 'direnv.linux-amd64'),
            backupspath = os.path.join(installationpath, 'pre_direnv_backups')
            )
        return self.paths
    
    def make_dirs(self):
        # MakeDirStatus = collections.namedtuple('MakeDirStatus', '
        try:
            os.makedirs(self.paths.backupspath)
        except FileNotFoundError as excep:
            print('FileNotFoundError: {}\t{}'.format(excep, self.paths.backupspath))
        except PermissionError as excep:
            print('PermissionError: {}\t{}'.format(excep, self.paths.backupspath))
            toolkit.change_permissions(self.paths.backupspath, topdown=False, initial_exception=excep)
        except Exception as excep:
            print('UnforeseenError: {}\t{}'.format(excep, self.paths.backupspath))
        
        if os.path.exists(self.paths.backupspath):
            return 0
        else:
            return 1
        
    def copy_binary(self, max_attempts=3):
        exceptions_list = []
        if max_attempts == 0:
            print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        max_attempts -= 1
        try:
            shutil.copy2(self.paths.setupfile, self.paths.installationpath)
        except FileNotFoundError as excep:
            exceptions_list.append(excep)
            print("Not found: ", self.paths.setupfile)
            # self.paths.setupfile = input("Enter the complete path including name of direnv setup binary:")
            # self.copy_binary(self, max_attempts)
        except PermissionError as excep:
            exceptions_list.append(excep)
            toolkit.change_permissions(self.paths.installationpath)
        except Exception as excep:
            exceptions_list.append(excep)
        finally:
            return exceptions_list

    def make_exec(self, max_attempts = 3):
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
            self.make_exec(max_attempts)

    def install(self, max_attempts=3):
        # self.setup_paths()
        self.make_dirs()
        self.copy_binary(max_attempts)
        self.make_exec()
        with open(self.shell.file, 'a') as write_obj:
            write_obj.writelines(self.shell.command)
        # os.environ["PATH"] += os.pathsep + self.paths['installpath']

    def uninstall(self):
        with open(self.shell.file, 'r') as read_obj:
            contents = read_obj.readlines()
        remove_line_idx = {idx for idx, line_ in enumerate(contents) if self.shell.command in line_}
        new_contents = [line_ for idx, line_ in enumerate(contents) if idx not in remove_line_idx]
        with open(self.shell.file, 'w') as write_obj:
            write_obj.write('\n'.join(new_contents))

    def check(self):
        try:
            with open(self.shell.file, 'r') as read_obj:
                contents = read_obj.readlines()
        except FileNotFoundError:
            return False
        direnv_installed = [True for line_ in contents if self.shell.command in line_]
        if True in direnv_installed:
            return True
        else:
            return False


if __name__ == '__main__':
    print(__file__)
    sub_shell = SubShell(purpose='test')
    print(sub_shell.copy_binary())
    # paths = sub_shell.setup_paths()
    # print('paths', paths)
    # mk_dirs = sub_shell.make_dirs()
    # print('mk_dirs', mk_dirs)
    # copybin_exceptions = sub_shell.copy_binary()
    # print('copybin_exceptions', copybin_exceptions)
    
    
    # sub_shell.setup_paths()
    # print(sub_shell.paths)
    # print(sub_shell.__dict__)
    # print(sub_shell.__dir__())
    # direnv.copy_binary()
