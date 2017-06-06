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
        self.Paths = collections.namedtuple('Paths', 'setupfile copiedfile installedfile installationpath backupspath')

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
        self.paths = self.Paths(
            setupfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv.linux-amd64'),
            copiedfile = os.path.join(self.root_dir_path, 'requirements', 'bin', 'direnv'),
            installationpath = installationpath,
            installedfile = os.path.join(installationpath, 'direnv'),
            backupspath = os.path.join(installationpath, 'pre_direnv_backups')
            )
        return self.paths
    
    def change_paths(self, setupfile=None, copiedfile=None, installationpath=None,
                    installedfile=None, backupspath=None
                    ):
        
        setupfile = self.paths.setupfile if setupfile is None else setupfile
        copiedfile = self.paths.copiedfile if copiedfile is None else copiedfile
        installationpath = self.paths.installationpath if installationpath is None else installationpath
        installedfile = self.paths.installedfile if installedfile is None else installedfile
        backupspath = self.paths.backupspath if backupspath is None else backupspath
        
        self.paths = self.Paths(setupfile=setupfile, copiedfile=copiedfile,
                                installationpath=installationpath, installedfile=installedfile,
                                backupspath=backupspath
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
        except FileExistsError:
            print("Existing directory {} used.".format(self.paths.backupspath))
        except Exception as excep:
            print('UnforeseenError: {}\t{}'.format(excep, self.paths.backupspath))
        
        if os.path.exists(self.paths.backupspath):
            return 0
        else:
            return 1
        
    def copy_move_binary(self, task:('both', 'copy', ' move')= 'both', force:(True, 'ask', False)=False):
        """

        :param force:
        :type force:
        :param task_:
        :type task_:
        """
        
        copy2_move_fn = {'copy': {'fn': shutil.copy2, 'args': (self.paths.setupfile, self.paths.copiedfile)},
                         'move': {'fn':  shutil.move, 'args': (self.paths.copiedfile,self.paths.installationpath)}
                     }
        exceptions_list = []
        tasks = ['copy', ' move']
        tasks = tasks if task not in tasks else task
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
                    choice = input("Enter choice:")
                else:
                    print(self.paths.copiedfile, "already exists.")
                    return
                toolkit.check_remove(self.paths.copiedfile)
                copy2_move_fn[task_]['fn'](*copy2_move_fn[task_]['args'])
            except Exception as excep:
                exceptions_list.append(excep)
                # reattempt = False
                raise excep
            finally:
                copy2_move_fn[task_]['fn'](*copy2_move_fn[task_]['args'])
                return exceptions_list
            #TODO: Maybr create a function to modify paths? Or revert to dict? No not the latter.
        
    def make_exec(self, max_attempts:(1|2|3)=3):
        current_perm = toolkit.get_file_permission_via_shell(self.paths.installedfile, in_form='code')
        # add_perm = toolkit.recalculate_final_permission(current_perm=current_perm, new_perm='0o777', action='add')
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
            
    def add_to_path(self):
        if os.name == 'posix':
            print(os.environ["PATH"])
            os.environ["PATH"] += os.pathsep + self.paths.installedfile
            print(os.environ["PATH"])
            

    
if __name__ == '__main__':
    print(__file__)
    sub_shell = SubShell(purpose='test')
    print(sub_shell.copy_move_binary())
