import os
import shutil
import subprocess

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)

from moreservers import (
    get_jars,
    subprocess_run,
)

from moreservers.plugininfo import PluginInfo


class ServerInfo:
    def __init__(self):
        self.name = None
        self.path = None
        self.launch_jars = None
        self.plugins_path = None
        self.plugins = None
        self.opener = None
        self.pid = None

        self.ready = False
        self.launch_button = None
        self.plugin_button = None

    def load(self, server_dir):
        """
        Load server information from the given directory.

        Args:
            server_dir (str): Path to the server directory.
        """
        self.name = os.path.split(server_dir)[1]
        self.path = server_dir
        self.launch_jars = get_jars(server_dir)
        self.plugins_path = os.path.join(server_dir, "plugins")
        if len(self.launch_jars) != 1:
            error = ("Expected one jar in %s, got %s"
                     % (server_dir, self.launch_jars))
            self.ready = False
        else:
            self.ready = True
        return self.ready

    def run_jar_with(self, gui_term_path, gui_term_args):
        """Start the server and store its process ID."""
        self.command_parts = [gui_term_path] + gui_term_args + [self.launch_jars[0]]
        self.run_custom(self, self.command_parts)
    
    def run_custom(self, command_parts, callback=None):
        self.command_parts = command_parts
        # process = subprocess_run(  # CompletedProcess has no PID
        process = subprocess.Popen(
            command_parts,
            cwd=self.path
        )
        self.pid = process.pid  # Store the process ID when the server starts
        # if callback:
        #     process.wait()  # works with Popen
        #     callback()
        # ^ not working (callback is too soon)

    def is_running(self):
        """Check if the server process is still running."""
        if self.pid is None:
            return False
        try:
            # Signal 0 is a no-op; it checks if the process is running
            os.kill(self.pid, 0)
        except OSError:
            self.pid = None
            return False
        return True

    def refresh_plugins(self, opener=None):
        """
        Refresh the plugins list.

        Args:
            opener (str, optional): Only include plugins that start with this prefix.
        """
        if os.path.isdir(self.plugins_path):
            self.plugin_jars = get_jars(self.plugins_path, opener)
        else:
            self.plugin_jars = None
        self.plugins = []
        if self.plugin_jars is not None:
            for plugin_jar in self.plugin_jars:
                plugin = PluginInfo()
                plugin.load(plugin_jar)
                self.plugins.append(plugin)
        self.opener = opener


    def plugin_path(self, path):
        new_plugin = PluginInfo()
        new_plugin.load(path)
        if not new_plugin.name:
            raise ValueError("Expected path got %s" % repr(new_plugin.name))
        for plugin in self.plugins:
            if new_plugin.name.lower() == plugin.name.lower():
                print('Found "%s"' % new_plugin.name)
                return plugin.path
        return None

    def has_plugin(self, path):
        if not path:
            raise ValueError("Expected path got %s" % repr(path))
        return self.plugin_path(path) is not None

    def install_plugin(self, path):
        """
        Install a plugin from the given path.

        Args:
            path (str): Path to the plugin file.

        Returns:
            str: A message indicating the result of the installation.
        """
        new_plugin = PluginInfo()
        new_plugin.load(path)
        for plugin in self.plugins:
            if new_plugin.name.lower() == plugin.name.lower():
                return "%s is already installed" % plugin.path

        if not os.path.isdir(self.plugins_path):
            os.makedirs(self.plugins_path)
        dst_path = os.path.join(self.plugins_path, new_plugin.filename)
        if os.path.isfile(dst_path):
            return "%s is already installed" % dst_path
        shutil.copy(new_plugin.path, dst_path)
        return 'Installed "%s"' % dst_path
