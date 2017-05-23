import unittest
import os
import collections
import toolkit


def create_empty_test_tree(location=os.path.join(os.path.split(__file__)[0], 'data')):
    """
    Creates a three level deep tree with regular and read-only files and directories for testing
    the clean_tree function in toolkit.py
    Tree structure:
    <location>/data/test_trees/tree_0/
            /readonly.dir/
                        readonly.file, regular.file
            /regular.dir/
                        readonly.file, regular.file
                        
    :param location: Fullpath where the tree will be created default is project_root/tests/data
    :type location: (str)
    :return: namedtuple- TestPaths(files, emptytree, filledtree) with paths for each.
    :rtype: (namedtuple: dict, dict, dict)
    """
    
    pathcases_keys = ('regular', 'readonly', 'nonexistent')  # keys correspond to different cases.
    # 'non-existent' path is not created, tests PathNotExistsError condition.

    # Creates directory paths, for an empty tree and sets readonly permission to some of them.
    path_prefix = "test_trees/tree_empty"
    dir_paths_empty = {key: os.path.normpath(os.path.join(location, path_prefix, '.'.join([key, 'dir']))) for key in pathcases_keys}
    [os.makedirs(path, exist_ok=True) for key, path in dir_paths_empty.items() if key != 'nonexistent']
    [os.chmod(path, 0o444) for key, path in dir_paths_empty.items() if key == 'readonly']

    # Creates directory paths, the tree is populated with files.
    path_prefix = "test_trees/tree_filled"
    dir_paths_filled = {key: os.path.normpath(os.path.join(location, path_prefix, '.'.join([key, 'dir']))) for key in pathcases_keys}
    
    [os.makedirs(path, exist_ok=True) for key, path in dir_paths_filled.items() if key != 'nonexistent']
        # Creates directories intended for creation. Skips creation if they already exist.
    
    
    for dir_key, dir_path_ in dir_paths_filled.items():  # iterates through each dir path.
        if os.path.exists(dir_path_):
            # Creates file paths using the paths of existing directories,
            # including path for files marked for non-creation
            file_paths = {file_key: os.path.join(dir_path_, '.'.join([file_key, 'file'])) for file_key in pathcases_keys}
        for file_key_, file_path_ in file_paths.items():  # iterates throught just created file paths
            if file_key_ != 'nonexistent':  # If file is meant to be created
                try:
                    with open (file_path_, 'x') as temp_obj:  # Pass if it already exists, Create if it doesn't
                        pass
                except FileExistsError as excep:
                    # print(excep)
                    pass
                except FileNotFoundError as excep:
                    # print(excep)
                    pass
                except PermissionError as excep:
                    # print(excep)
                    pass
                finally:
                    if file_key_ == 'readonly':  # If file is supposed to be read-only, make it so.
                        os.chmod(file_path_, 0o444)
        if dir_key == 'readonly':  # If directory is supposed to be read only, make it so.
            os.chmod(dir_path_, 0o444)
    
    root_path = os.path.commonpath([
                    os.path.commonpath(dir_paths_empty.values()),
                    os.path.commonpath(dir_paths_filled.values())
                ])
    TestPaths = collections.namedtuple('TestPaths', 'root emptytree filledtree files')
    test_paths = TestPaths(root=root_path, emptytree=dir_paths_empty, filledtree=dir_paths_filled, files=file_paths)
    return test_paths
    

class CleanupTreeFunctionTest(unittest.TestCase):
    def setUp(self):
        self.test_paths = create_empty_test_tree()
        
    def test_empty_tree(self):
        toolkit.cleanup_tree(self.test_paths.root)
        pass
        # self.assertEqual(True, False)
    


if __name__ == '__main__':
    # unittest.main()
    pass
    test_paths = create_empty_test_tree()

