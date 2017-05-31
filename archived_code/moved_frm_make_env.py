import os
import shutil


def setup_paths():
    P = os.path  # for ease of viewong & typing. Used a lot in this function.
    setup_file_path = P.realpath(P.join(__file__, P.pardir, P.pardir, 'requirements', 'bin', 'direnv.linux-amd64'))
    installation_path = os.path.expanduser(os.path.join('~','bin','direnv'))
    installed_file_path = os.path.join(installation_path, 'direnv')
    backups_path = os.path.join(installation_path, 'pre_direnv_backups')
    keys_list = ['setupfile', 'installedfile', 'installpath', 'backupspath']
    values_list = [setup_file_path, installed_file_path, installation_path, backups_path]
    direnv_paths = dict(zip(keys_list, values_list))
    return direnv_paths


def copy_direnv(shell, direnv_paths, max_attempts=3):
    max_attempts -= 1
    if max_attempts == 0:
        print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        quit()
    try:
        shutil.copy2(direnv_paths['setupfile'], direnv_paths['installpath'])
    except FileNotFoundError:
        print("Not found: ", direnv_paths['setupfile'])
        direnv_paths['setupfile'] = input("Enter the complete path including name of direnv setup binary:")
        copy_direnv(shell, direnv_paths, max_attempts)


def make_exec(shell,direnv_paths, max_attempts = 3):
    max_attempts -= 1
    if max_attempts == 0:
        print("Too many attempts with incorrect paths. Please ascertain the file paths and run install again.")
        quit()
    try:
        os.chmod(direnv_paths['installedfile'], 0o111)  # sets the direnv binary's permission to executable, as instructed in direnv README.
    except FileNotFoundError:
        print("Not found:", direnv_paths['installedfile'])
        print("Copy the direnv binary file to a location of your choice and enter the path here:")
        direnv_paths['installedfile'] = input("Enter the complete path including name of direnv installed binary:")
        make_exec(shell, direnv_paths, max_attempts)


def check_direnv(shell):
    try:
        with open(shell['file'], 'r') as read_obj:
            contents = read_obj.readlines()
    except FileNotFoundError:
        return False
    direnv_installed = [True for line_ in contents if shell['command'] in line_]
    if True in direnv_installed:
        return True
    else:
        return False