import os
import stat
import collections
from shutil import rmtree

FunctionOutcome = collections.namedtuple('FunctionOutcome', 'fn worked')
FunctionCalled = collections.namedtuple('FunctionCalled', 'fn')
no_print = '\b'


def fn_worked(fn, worked, notify=False):
    """
    Accepts function name and success status of the nesting function and
    returns namedtuple FunctionOutcome indicating this info.
    Usage, inserted to a condition statement such as if-then, try-catch.
    Inserted at teh end of function.
    :param fn: (str) nesting function's name
    :param worked: (bool) Whether the function's operation worked.
    :param notify: (bool) Allows switching on and off individual calls of this function.
        Default = False
    """
    print(FunctionOutcome(fn=fn, worked=worked)) if notify else None


def fn_called(fn, notify=False):
    """
        Accepts function name of the nesting function and
        returns namedtuple FunctionCalled indicating the begining of a function's execution.
        Usage, Inserted at the begining of a function.
        :param fn: (str) nesting function's name
        :param notify: (bool) Allows switching on and off individual calls of this function.
            Default = False
        """
    print(FunctionCalled(fn=fn)) if notify else None


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
            if os.name == ' posix':
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
    
    
    if handle_exceptions:
        try:
            rmtree(tree_root, onerror=remove_readonly)
        except FileNotFoundError as excep:
            print(excep)
        except PermissionError as excep:
            print(excep)
        except Exception as excep:
            print(excep)
        
    else:
        rmtree(tree_root)

    fn_worked(fn='cleanup_tree', worked=not os.path.exists(tree_root), notify=notify_outcome)
    
    
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
    

def check_remove(path, notify=False):
    try:
        assert(os.path.exists(path) is False)
    except:
        cleanup_tree(path)
        assert (os.path.exists(path) is False)


def check_make(path, notify=False):
    try:
        assert(os.path.exists(path) is True)
    except:
        if os.path.isdir(path):
            os.mkdir(path)
        elif os.path.isfile(path):
            with open(path, 'w') as temp_obj:
                pass
        assert(os.path.exists(path) is True)
        
        
def increment(start=0, step=1):
        while True:
            yield start
            start += step


def path_nt2nix(abspath):
    drive_letter, rest_of_path = os.path.splitdrive(abspath)
    path_with_posix_drive = os.sep.join(['mnt', drive_letter[0].lower(), rest_of_path])
    almost_posix = ''.join([os.sep, os.path.normpath(path_with_posix_drive)])
    return almost_posix.replace('\\', '/')


def get_file_permission_via_shell(filepath, in_form='namedtuple'):
    from subprocess import check_output
    if os.path.isfile(filepath):
        path, file = os.path.split(filepath)
    else:
        path = filepath
    ls_call = str(check_output(['ls', '-l', path]))
    ls_call = ls_call.lstrip('b')
    ls_call = ls_call.split('\\n')
    file_entry = [entry for entry in ls_call if file in entry][0]
    permissions_string = file_entry[0:file_entry.find(' ')]
    ## derived_filename = file_entry[file_entry.rfind(' '):]
    permissions_key_alpha2num = {'r': 4, 'w': 2, 'x': 1, '-': 0, 'd':0}
    ## permissions_string = '-rw--w--wx'
    permission_nums = ([permissions_key_alpha2num[p] for p in permissions_string])
    user_categs = ('user', 'group', 'other')
    permits_dict = {gp: (str(sum(permission_nums[start:stop])), *(permissions_string[start:stop].replace('-', '')))
               for (gp, start, stop) in zip(user_categs, range(1, 10, 3), range(4, 13, 3))}
    perm_code = ''.join(['0o', permits_dict['user'][0], permits_dict['group'][0], permits_dict['other'][0]])
    
    return_options = {'dict': permits_dict, 'groups': permits_dict, 'code': perm_code, 'str': permissions_string}
    is_dict = True if permissions_string[0] == 'd' else False
    try:
        return return_options[in_form]
    except KeyError:
        Permissions = collections.namedtuple('Permissions', 'code user group other string is_dict')
        return Permissions(code=perm_code, user=permits_dict['user'], group=permits_dict['group'],
                           other=permits_dict['other'], string=permissions_string, is_dict=is_dict)


def recalculate_final_permission(current_perm, new_perm, action='add'):
    perm_num_sets = {'x': {1, 3, 5, 7}, 'w': {2, 3, 6, 7}, 'r': {4, 5, 6, 7}}
    
    final_perm = {'add': int(str(current_perm)[-3:]) + int(str(new_perm)[-3:])}
        # ,'remove': int(str(current_perm)[-3:]) - int(str(new_perm)[-3:])}
    

if __name__ == '__main__':
    path_arg = "/mnt/c/Users/kshit/bin_test/direnv/direnv.linux-amd64"