import os
import collections
from toolkit import debug_print
from datetime import datetime
from shutil import rmtree


def cleanup_tree(tree_root):
    problem_files = dict()
    try:
        rmtree(tree_root)
    except:
        ExceptionInfo = collections.namedtuple('ExceptionInfo', 'path file exception')
        error_idx = []
        files_list = []
        debug_print('tree_root', tree_root)
        for root, subdirs, files in os.walk(tree_root, topdown=True):
            files_list.extend([os.path.join(root, file_) for file_ in files])
            try:
                rmtree(root)
            except:
                pass
        for file_ in files_list:
            
            try:
                os.remove(file_)
            except FileNotFoundError as excep:
                filepath, filename = os.path.split(file_)
                temp_excep = ExceptionInfo(path=filepath, file=filename, exception=excep)
                problem_files.setdefault('FileNotFoundError', []).append(temp_excep)
                error_idx.append(0)
            
            except PermissionError:
                try:
                    os.chmod(file_, 0o777)
                except Exception as excep:
                    filepath, filename = os.path.split(file_)
                    temp_excep = ExceptionInfo(path=filepath, file=filename, exception=excep)
                    problem_files.setdefault('PermissionError', []).append(temp_excep)
                    error_idx.append(1)
                else:
                    os.remove(file_)
            
            except Exception as excep:
                filepath, filename = os.path.split(file_)
                temp_excep = ExceptionInfo(path=filepath, file=filename, exception=excep)
                problem_files.setdefault('Unforeseen', []).append(temp_excep)
                error_idx.append(2)
            
            finally:
                ErrorMessages = collections.namedtuple('ErrorMessages', '''FileNotFoundError
                    PermissionError OtherErrors LogVar''')
                error_msgs = ErrorMessages(
                    FileNotFoundError="Some files couldn't be removed because they were not found.",
                    PermissionError='''Some files couldn't be removed because this user account does
                                not have permission to remove them. Contact the file owner or a system
                                 administrator, or use sudo.''',
                    OtherErrors='''Some files couldn't be removed due to unforeseen problems.
                        Try removing them manually.''',
                    LogVar="For devs: an error log variable has been returned."
                    )
                error_idx.append(3)
                [print(error_msgs[idx]) for idx in error_idx]
        try:
            rmtree(tree_root)
        except Exception as excep:
            filepath = tree_root
            temp_excep = ExceptionInfo(path=filepath, file='', exception=excep)
            problem_files.update({'TreeNotRemoved': temp_excep})
            print('''ERROR: Tree couldn't be removed. This is usually because there are files in
                the tree that couldn't be removed, and/or you do not have the necessary permissions
                to remove some or all files and diretories. \n For devs: a log variable has been
                returned.''')
        else:
            print("Tree has been successfully removed.")
    else:
        print("Tree has been successfully removed.")
    
    project_root = os.path.split(os.path.split(__file__)[0])[0]
    log_location = os.path.join(project_root, 'logs', 'clean_tree.log')
    log_contents = (['\n', datetime.ctime(datetime.now()), '=' * 10, problem_files])
    print(log_contents, sep='\n')
    try:
        with open(log_location, 'w+') as write_obj:
            os.sys.stdout.writelines(log_contents)
        return problem_files
    except:
        pass


if __name__ == '__main__':
    tree_root = input("Enter the path root to be cleaned")
    cleanup_tree(tree_root)