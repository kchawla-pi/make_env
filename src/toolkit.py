import os
import stat
import collections
from shutil import rmtree

FunctionOutcome = collections.namedtuple('FunctionOutcome', 'fn worked')
FunctionCalled = collections.namedtuple('FunctionCalled', 'fn')
no_print = '\b'


def fn_worked(fn, worked, notify=False):
    return FunctionOutcome(fn=fn, worked=worked) if notify else None


def fn_called(fn, notify=False):
    return FunctionCalled(fn=fn) if notify else None


def debug_print(*arg):
    # return
    if arg[-1] != '00' or True or 'db' or 'debug':
        print(*arg)
        return
    print()
    if isinstance(arg[0], str) and arg[0].find('--',0, 2):
        print(arg[0])
        start_idx = 1
    else:
        start_idx = 0
    on = 1
    if on and True:
        for arg_elem in arg[start_idx:]:
            if arg_elem == 'xxx':
                return
            try:
                len(arg_elem)
            except TypeError:
                print(arg[1:], sep='\n')
            else:
                for elem in arg_elem:
                    print(elem)
    print()


def cleanup_tree(tree_root, handle_exceptions=True, notify_init=False, notify_outcome=False):
    
    fn_called('cleanup_tree', notify_init)
    
    def remove_readonly(fn, problem_path, excinfo):
        def core_logic():
            if os.name ==' posix':
                os.chmod(problem_path, 0o600)
            else:
                os.chmod(problem_path, stat.S_IWRITE)
            fn(problem_path)
        
        if handle_exceptions:
            try:
                core_logic()
            except Exception as exc:
                print("Skipped:", problem_path, "because:\n", exc)
                raise Exception
        else:
            core_logic()
    
    rmtree(tree_root, onerror=remove_readonly)
    if handle_exceptions:
        try:
            rmtree(tree_root)
        except FileNotFoundError as excep:
            print(excep)
        except PermissionError as excep:
            print(excep)
        except Exception as excep:
            print(excep)
        
    else:
        rmtree(tree_root)

    print(fn_worked(fn='cleanup_tree', worked=not os.path.exists(tree_root), notify=notify_outcome))
    
    

def change_permissions(path,tree=False, nix_perm=0o600, topdown=True, initial_exception='', handle_exceptions=True, notify_init=False):
    print(fn_called('change_permissions', notify_init))
    perm = stat.S_IWRITE if os.name == 'nt' else nix_perm
    if initial_exception:
        excep_list = [initial_exception]
    else:
        excep_list = []
    try:
        os.chmod(path, perm)
    except Exception as exc:
        print("Skipped:", path, "because:\n", exc)
    if tree is False:
        return
    
    for root, dirs, files in os.walk(path, topdown=topdown):
        # print('path', path)
        paths = [os.path.join(root, dir_) for dir_ in dirs]
        # print('paths', paths)
        paths.extend([os.path.join(root, file_) for file_ in files])
        while paths:
            popped_path = paths.pop()
            # print('popped_path', popped_path)
            try:
                os.chmod(popped_path, perm)
            except Exception as exc:
                print("Skipped:", popped_path, "because:\n", exc)
    


if __name__ == '__main__':
    # location = os.path.split(os.path.split(__file__)[0])[0]
    # tree_root = os.path.normpath(os.path.join(location, 'tests', 'data', 'test_trees'))
    # tree_root = 'C:\\Users\\kshit\\Dropbox\\workspace\\make_env\\kchawla-pi\\make_env\\tests\\data\\test_trees'
    
    print("Enter the full path of the root that you wish to delete. WARNING! This may NOT be reversible.")
    tree_root = os.sys.argv
    cleanup_tree(tree_root)
    