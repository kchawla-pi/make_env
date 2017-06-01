def install(self, max_attempts=3):
    # self.setup_paths()
    self.make_dirs()
    self.copy_binary(max_attempts)
    self.make_exec()
    with open(self.shell.file, 'a') as write_obj:
        write_obj.writelines(self.shell.command)
        # os.environ["PATH"] += os.pathsep + self.paths['installpath']


def uninstall(self):
    with open(self.shell.file, 'r') as read_obj:
        contents = read_obj.readlines()
    remove_line_idx = {idx for idx, line_ in enumerate(contents) if self.shell.command in line_}
    new_contents = [line_ for idx, line_ in enumerate(contents) if idx not in remove_line_idx]
    with open(self.shell.file, 'w') as write_obj:
        write_obj.write('\n'.join(new_contents))


def check(self):
    try:
        with open(self.shell.file, 'r') as read_obj:
            contents = read_obj.readlines()
    except FileNotFoundError:
        return False
    direnv_installed = [True for line_ in contents if self.shell.command in line_]
    if True in direnv_installed:
        return True
    else:
        return False

