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

import sys

if sys.version_info.major >= 3:
    # Python 3: Use subprocess.run directly
    from subprocess import run as subprocess_run
else:
    # Python 2: Define a compatible subprocess_run function
    import subprocess

    def subprocess_run(args, check=False, stdout=None, stderr=None, cwd=None):
        """
        Simulate subprocess.run() for Python 2 using subprocess.Popen.

        Args:
            args (list): The command and arguments to run.
            check (bool): If True, raise CalledProcessError if the command exits with a non-zero status.
            stdout (file-like object, optional): Capture standard output if specified.
            stderr (file-like object, optional): Capture standard error if specified.
            cwd (str, optional): Working directory to run the command.

        Returns:
            CompletedProcess: A simulated result object containing return code, stdout, and stderr.
        """
        # Use subprocess.Popen to execute the command and capture the output
        process = subprocess.Popen(
            args,
            stdout=stdout or subprocess.PIPE,
            stderr=stderr or subprocess.PIPE,
            cwd=cwd
        )
        # Wait for the process to complete and capture stdout and stderr
        out, err = process.communicate()
        retcode = process.returncode

        # Simulate the CompletedProcess object
        class CompletedProcess:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        result = CompletedProcess(retcode, out, err)

        if check and retcode != 0:
            raise subprocess.CalledProcessError(retcode, args, output=out, stderr=err)

        return result


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
