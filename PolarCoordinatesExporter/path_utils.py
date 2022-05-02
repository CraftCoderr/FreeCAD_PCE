from os import path

workbecnh_path = path.dirname(path.realpath(__file__))

def get_workbench_file_path(filename):
    return path.join(workbecnh_path, filename)

