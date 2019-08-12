import shutil

import file_handle


# TODO path as a function's arg
def copy_all(shortcut):
    paths = file_handle.get_shortcut_info(shortcut=shortcut,
                                          path=file_handle.DATAPATH)
    source = paths['source']
    destinations = paths['destination']
    for d_path in destinations:
        return f'copy {source} to {d_path}'
        # shutil.copytree(source, d_path)
