import os
import shutil
import sys

if sys.version_info.major >= 3:
    which = shutil.which
else:
    def which(name):
        paths = os.environ['PATH'].split(os.pathsep)
        for path in paths:
            sub_path = os.path.join(path, name)
            if not os.path.isfile(sub_path):
                continue
            return sub_path
        return None


def get_jars(parent, opener=None):
    """
    Return a list of .jar file paths in the parent directory.

    Args:
        parent (str): Directory to search for jar files.
        opener (str, optional): Only include files that start with this prefix.

    Returns:
        list: Alphabetically sorted list of .jar file paths.
    """
    matching_plugins_paths = []
    for sub in os.listdir(parent):
        sub_path = os.path.join(parent, sub)
        if not os.path.isfile(sub_path):
            continue
        if not sub.lower().endswith(".jar"):
            continue
        if opener and not sub.lower().startswith(opener.lower()):
            continue
        matching_plugins_paths.append(sub_path)
    return sorted(matching_plugins_paths)
