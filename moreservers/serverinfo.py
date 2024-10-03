import os
import shutil

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)

from moreservers import (
    get_jars,
)

from moreservers.plugininfo import PluginInfo


class ServerInfo:
    def __init__(self):
        self.name = None
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
