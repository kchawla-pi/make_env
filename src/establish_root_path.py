import os



def establish_root_path(root_dir_path='', root_dir_name = 'make_env'):
    if root_dir_path == '':
        root_dir_path = os.path.split(os.path.split(__file__)[0])[0]
    try:
        assert(os.path.split(root_dir_path)[1] == root_dir_name)
    except AssertionError:
        
        print('\a',
              "Error. Possibly invalid path. Please review the following information:",
              " {} -- Expected root directory name.".format(os.path.split(root_dir_path)[1]),
              " {} -- Supplied root directory name.".format(root_dir_name),
              "\nAutomatically determined path is:\n\t --- {}".format(root_dir_path), sep='\n'
              )
        query = input("Is this correct? (Type y/n/q and press Enter key for yes/no/quit program: ")
        if query.lower() in {'y', 'yes', 'yup', 'yeah', 'yah'}:
            pass
        elif query.lower in {'n', 'no', 'nah', 'nope', 'nada'}:
            print("Type the root directory path: ")
            root_dir_path = establish_root_path(root_dir_path=query, root_dir_name=root_dir_name)
        else:
            quit()
        
            
    finally:
        return root_dir_path
        
root_path = establish_root_path(root_dir_path='', root_dir_name='make_envy')