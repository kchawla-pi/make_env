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
        
    def copy_binary(self, max_attempts:(1|2|3)=3):
        """

        :type max_attempts: int (1|2|3)
        """
        if max_attempts == 0:
            print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        if max_attempts not in (1, 2, 3):
            print("max_attempt can be 1, 2 or 3.")
            print("Using default.")
            max_attempts = 1
        exceptions_list = []
        max_attempts -= 1
        try:
            shutil.copy2(self.paths.setupfile, self.paths.installationpath)
        except FileNotFoundError as excep:
            exceptions_list.append(excep)
            print("Not found: ", self.paths.setupfile)
            self.paths.setupfile = input("Enter the complete path including name of direnv setup binary:")
            reattempt = True
        except PermissionError as excep:
            exceptions_list.append(excep)
            toolkit.change_permissions(self.paths.installationpath)
            reattempt = True
        except Exception as excep:
            exceptions_list.append(excep)
            reattempt = True
        else:
            reattempt = False
        finally:
            if reattempt:
                self.copy_binary(self, max_attempts)
            return exceptions_list

    def make_exec(self, max_attempts = 3):
        current_perm = toolkit.get_file_permission_via_shell(self.paths.installedfile, in_form='code')
        add_perm = toolkit.recalculate_final_permission(current_perm=current_perm, new_perm='0o111', action='add')
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
            
    
if __name__ == '__main__':
    print(__file__)
    sub_shell = SubShell(purpose='test')
    print(sub_shell.copy_binary())
