#!/python3
import os


def resolve_path(some_path = '', *dirs):
    if len(dirs) == 0:
        return os.path.realpath(os.path.expanduser(some_path))
    # if os.sep in some_path:
    some_path_parts = some_path.split(os.sep)
    some_path_parts.extend(dirs)
    joined_dirs = os.sep.join(some_path_parts)
    return os.path.realpath(os.path.expanduser(joined_dirs))

def paths_setup(root_name = 'tic_env'):
    script_path = resolve_path(__file__)
    path_dirs = script_path.split(os.sep)
    root_idx = max({idx for idx, elem in enumerate(path_dirs) if elem == root_name and path_dirs[idx+1] == 'core'}) + 1
    root_dirs = path_dirs[0:root_idx]
    root_path = os.sep.join(root_dirs)
    rel_dirs = {'direnv': ['requirements', 'bin', 'direnv.linux-amd64']}
    temp_list = root_dirs
    temp_list.extend(rel_dirs['direnv'])
    abs_paths = {'direnv': os.sep.join(temp_list)}
    return abs_paths


