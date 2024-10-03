#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import subprocess
import sys
from collections import OrderedDict

if sys.version_info.major >= 3:
    import tkinter as tk
    from tkinter import messagebox
else:
    import Tkinter as tk
    import tkMessageBox as messagebox


if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(MODULE_DIR)
    sys.path.insert(0, REPO_DIR)

from moreservers import (
    get_jars,
    which,
)

from moreservers.plugininfo import PluginInfo

from moreservers.serverinfo import ServerInfo


class PluginManagerApp(tk.Frame):
    def __init__(self, parent):
        if sys.version_info.major >= 3:
            super().__init__(parent)
        else:
            tk.Frame.__init__(self, parent)
        self.default_plugin_name = "CustomRecipes"
        self.launcher_path = os.path.join(REPO_DIR, "launch-server.sh")

        # Define terminal arguments in order of preference
        self.gui_term_args = OrderedDict([
            ("xfce-terminal", ["--hold", "--command"]),
            ("mate-terminal", ["-x"]),
            ("konsole", ["-e"]),
            ("gnome-terminal", ["--"]),
            ("xterm", [])
        ])

        self.gui_term_path = None
        for term, args in self.gui_term_args.items():
            term_path = which(term)
            if term_path:
                self.gui_term_path = term_path
                self.gui_term_name = term
                break

        if not self.gui_term_path:
            messagebox.showerror("Error", "Could not find any terminal programs")
            self.enable_launch = False
        else:
            self.enable_launch = True

        # Get matching plugin paths
        matching_plugins_paths = get_jars(os.getcwd(), opener=self.default_plugin_name)
        self.plugin_src = matching_plugins_paths[-1] if matching_plugins_paths else None
        plugin_name = os.path.split(self.plugin_src)[1]

        # Load server info
        self.servers = OrderedDict()
        for sub in os.listdir(os.getcwd()):
            sub_path = os.path.join(os.getcwd(), sub)
            if not os.path.isdir(sub_path):
                continue
            server_info = ServerInfo()
            server_info.load(sub_path)
            if not server_info.ready:
                continue
            server_info.refresh_plugins(opener=self.default_plugin_name)
            self.servers[sub] = server_info

        # Add buttons for servers
        self.this_row = 0
        for server_name, server in self.servers.items():
            server.launch_button = tk.Button(self, text="Launch %s" % server_name,
                                             command=lambda s=server: self.run_server(s))
            server.plugin_button = tk.Button(self, text="Install Plugin %s" % plugin_name,
                                             command=lambda s=server: self.install_plugin(s))
            server.launch_button.grid(row=self.this_row, column=0)
            server.plugin_button.grid(row=self.this_row, column=1)
            self.this_row += 1

    def run_server(self, server):
        """
        Launch the server using the detected terminal.

        Args:
            server (ServerInfo): The server to launch.
        """
        if not self.gui_term_path:
            messagebox.showerror("Error", "Could not find any terminal programs")
            return False
        command = [self.gui_term_path] + self.gui_term_args[self.gui_term_name] + [self.launcher_path]
        os.chdir(server.path)
        subprocess.run(command)
        return True

    def install_plugin(self, server):
        """
        Install a plugin to the server.

        Args:
            server (ServerInfo): The server to install the plugin to.
        """
        server.refresh_plugins(opener=self.default_plugin_name)
        result = server.install_plugin(self.plugin_src)
        if result:
            messagebox.showinfo("Plugin Installation", result)

def main():
    root = tk.Tk()
    root.title("Plugin Manager")
    app = PluginManagerApp(root)
    app.pack()
    root.mainloop()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
