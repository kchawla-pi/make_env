#! /usr/bin/env python3
import os
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
    """
    Class with data and methods to install the direnv binary which can create subshells.
    """
    def __init__(self, purpose='check', rootname='make_env', force_shell=False):
        """
        Creates namedtuple Paths and calls setup_paths()
        :param purpose: (str) 'check'(default), 'test': calls specific methods for specific actions.
        If 'test', adds suffix '_test' to created/modified dirs, files to preserve operating environment.
        :param rootname: (str) 'make_env'(default): The directory name of the project containing
        files necessary to install subshell project and make new ones.
        """
        self.shell = make_env.identify_shell(force=force_shell)
        self.purpose = purpose
        self.rootname = rootname
        self.Paths = collections.namedtuple('Paths', 'installationpath backupspath setupfile copiedfile installedfile')

        self.suffix = '_test' if purpose == 'test' else ''
        self.shell['files'] = tuple(''.join([file_, self.suffix]) for file_ in self.shell['files'])
        self.paths = self.setup_paths()
        
    def setup_paths(self):
        """
        Sets up the paths for files and directories for direnv.
        <user profile> or $HOME/bin/direnv as installation root.
        :return: instance of namedtuple Paths with fields
        - installationpath: path where direnv will be installed
        - backupspath: path where the backup of modified shell files and shell path is stored
        - setupfile: path of direnv binary file
        - copiedfile: path to the renamed copy of direnv binary file
        - installedfile: path of the renamed direnv binary executable is placed
        """
        self.root_dir_path = os.path.realpath(os.path.split(os.path.split(__file__)[0])[0])
        root_name_from_path = os.path.split(self.root_dir_path)[1]
        try:
            # Enforces dev awareness of the specified and derived root name
            assert( root_name_from_path == self.rootname)
        except AssertionError:
            print("Error. Possibly invalid path. Please review the following information:",
                  " {} -- Expected root directory name.".format(root_name_from_path),
                  " {} -- Supplied root directory name.".format(self.rootname),
                  "\nAutomatically determined path is:\n\t --- {}".format(self.root_dir_path), sep='\n'
                  )
            
        installationpath = os.path.expanduser(os.path.join('~', 'bin'+self.suffix, 'direnv'))
        self.paths = self.Paths(
            installationpath = installationpath,
            backupspath = os.path.join(installationpath, 'pre_direnv_backups'),
            setupfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv.linux-amd64'),
            copiedfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv'),
            installedfile = os.path.join(installationpath, 'direnv')
            )
        return self.paths
    
    def change_paths(self, setupfile=None, copiedfile=None, installationpath=None,
                     installedfile=None, backupspath=None
                    ):
        
        installationpath = self.paths.installationpath if installationpath is None else installationpath
        backupspath = self.paths.backupspath if backupspath is None else backupspath
        setupfile = self.paths.setupfile if setupfile is None else setupfile
        copiedfile = self.paths.copiedfile if copiedfile is None else copiedfile
        installedfile = self.paths.installedfile if installedfile is None else installedfile
        
        self.paths = self.Paths(installationpath=installationpath, installedfile=installedfile,
                                backupspath=backupspath, setupfile=setupfile, copiedfile=copiedfile
                                )
        return self.paths
    
    def make_dirs(self):
        """
        Creates directories for direnv installation and backup of existing config.
        :return: (int) returns 0 if directory exists at end of operation, else 1
        """
        try:
            os.makedirs(self.paths.backupspath)
        except FileNotFoundError as excep:
            print('FileNotFoundError: {}\t{}'.format(excep, self.paths.backupspath))
        except PermissionError as excep:
            print('PermissionError: {}\t{}'.format(excep, self.paths.backupspath))
            toolkit.change_permissions(self.paths.backupspath, topdown=False, initial_exception=excep)
        except FileExistsError:
            print("Existing directory {} used.".format(self.paths.backupspath))
        except Exception as excep:
            print('UnforeseenError: {}\t{}'.format(excep, self.paths.backupspath))
            raise excep
        
        if os.path.exists(self.paths.backupspath):
            return 0
        else:
            return 1
        
    def copy_move_binary(self, task:('both', 'copy', ' move')= 'both', force:(True, 'ask', False)=False):
        """

        :param force: (bool, str) args: False(default), 'ask', True : Reperforms the operation on error,
         or gives user the option to do so.
        :param task: (str) args: 'both'(default), 'copy', 'move' : Specifies the functions action
        """
        
        copy2_move_fn = {'copy': {'fn': shutil.copy2, 'args': (self.paths.setupfile, self.paths.copiedfile)},
                         'move': {'fn':  shutil.move, 'args': (self.paths.copiedfile,self.paths.installationpath)}
                     }
        exceptions_list = []
        tasks = ['copy', 'move']
        tasks = tasks if task not in tasks else [task]
        for task_ in tasks:
            try:
                copy2_move_fn[task_]['fn'](*copy2_move_fn[task_]['args'])
            except FileNotFoundError as excep:
                exceptions_list.append(excep)
                print("Not found: ", copy2_move_fn[task_]['args'][0])
                copy2_move_fn[task_]['args'][0] = input("Enter correct path:")
            except PermissionError as excep:
                exceptions_list.append(excep)
                toolkit.change_permissions(copy2_move_fn[task_]['args'][1])
            except FileExistsError as excep:
                exceptions_list.append(excep)
                if force == 'ask':
                    print(excep, "Type 'force' (without quotes) and press enter to replace, ",
                                 "or press enter to skip.",
                                 "The replaced and existing versions maybe different.", sep='\n'
                          )
                else:
                    print(self.paths.copiedfile, "already exists.")
                    return
                toolkit.check_remove(self.paths.copiedfile)
                copy2_move_fn[task_]['fn'](*copy2_move_fn[task_]['args'])
            except Exception as excep:
                exceptions_list.append(excep)
                raise excep
            finally:
                try:
                    copy2_move_fn[task_]['fn'](*copy2_move_fn[task_]['args'])
                except shutil.Error as excep:
                    print(excep)
                return exceptions_list
            #TODO: Maybr create a function to modify paths? Or revert to dict? No not the latter.
        
    def make_exec(self, max_attempts:(1|2|3)=3):
        max_attempts = toolkit.reattempt(max_attempts)
        if max_attempts == 0:
            print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
            quit()
        try:
            os.chmod(self.paths.installedfile, 0o777)  # sets the direnv binary's permission to executable, as instructed in direnv README.
        except FileNotFoundError:
            print("Not found:", self.paths.installedfile)
            print("Copy the direnv binary file to a location of your choice and enter the path here:")
            self.paths.installedfile = input("Enter the complete path including name of direnv installed binary:")
            self.make_exec(max_attempts)
            
    def read_path_file(self):
        if os.name == 'posix':
            print(self.shell['files'])
            with open(self.shell['files'][0]) as read_obj:
                config_contents = read_obj.readlines()
            # config_contents.f
            print(config_contents)
        
    def add_to_path(self):
        if os.name == 'posix':
            print(self.shell['files'])
            with open(self.shell['files'][0], 'a') as write_obj:
                write_obj.writelines([self.paths.installationpath])
            
            # print(os.environ["PATH"])
            # os.environ["PATH"] += os.pathsep + self.paths.installedfile
            # print(os.environ["PATH"])
            
    
    
            
if __name__ == '__main__':
    print(__file__)
    sub_shell = SubShell(purpose='test')
    sub_shell.read_path_file()
