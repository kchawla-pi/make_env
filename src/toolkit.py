import os
import stat
from shutil import rmtree


def debug_print(*arg):
    on = 1
    if on and True:
        print(arg[0])
    if on and True:
        print(arg[1:], sep='\n')


def cleanup_tree(tree_root):
    
    def remove_readonly(fn, problem_path, excinfo):
        try:
            if os.name ==' posix':
                os.chmod(problem_path, 0o600)
            else:
                os.chmod(problem_path, stat.S_IWRITE)
            fn(problem_path)
        except Exception as exc:
            print("Skipped:", problem_path, "because:\n", exc)
    
    rmtree(tree_root, onerror=remove_readonly)


if __name__ == '__main__':
    # location = os.path.split(os.path.split(__file__)[0])[0]
    # tree_root = os.path.normpath(os.path.join(location, 'tests', 'data', 'test_trees'))
    # tree_root = 'C:\\Users\\kshit\\Dropbox\\workspace\\make_env\\kchawla-pi\\make_env\\tests\\data\\test_trees'
    
    print("Enter the full path of the root that you wish to delete. WARNING! This may NOT be reversible.")
    tree_root = os.sys.argv
    cleanup_tree(tree_root)
    