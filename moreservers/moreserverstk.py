#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import subprocess
import sys
from collections import OrderedDict

if sys.version_info.major >= 3:
    import tkinter as tk
    from tkinter import messagebox, filedialog
else:
    import Tkinter as tk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog


if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(MODULE_DIR)
    sys.path.insert(0, REPO_DIR)

from moreservers import (
    get_jars,
    which,
    subprocess_run,
)

from moreservers.plugininfo import PluginInfo

from moreservers.serverinfo import ServerInfo


class PluginManagerApp(tk.Frame):
    def __init__(self, parent):
        self.servers_dir = os.getcwd()
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
        matching_plugins_paths = get_jars(self.servers_dir, opener=self.default_plugin_name)
        self.plugin_src = matching_plugins_paths[-1] if matching_plugins_paths else None

        # Load server info
        self.refresh_servers()

    def remove_widgets(self, clear_servers=True):
        self.this_row = 0
        if not self.servers:
            return
        for server_name, server in self.servers.items():
            if server.launch_button:
                server.launch_button.grid_forget()
            if server.plugin_button:
                server.plugin_button.grid_forget()
        if clear_servers:
            self.servers = OrderedDict()

    def create_widgets(self):
        plugin_name = None
        plugin = None
        if self.plugin_src:
            plugin = PluginInfo()
            plugin.load(self.plugin_src)
            plugin_name = os.path.split(self.plugin_src)[1]

        self.remove_widgets(clear_servers=False)
        # Add buttons for servers
        for server_name, server in self.servers.items():
            server.launch_button = tk.Button(self, text="Launch %s" % server_name,
                                             command=lambda s=server: self.run_server(s))
            server.plugin_button = tk.Button(self, text="Install Plugin %s" % plugin_name,
                                             command=lambda s=server: self.install_plugin(s))
            if not server.ready:
                server.launch_button['state'] = tk.DISABLED
            else:
                print("Found %s" % server.launch_jars)
            if not plugin_name or server.has_plugin(plugin_name):
                server.plugin_button['state'] = tk.DISABLED
            server.launch_button.grid(row=self.this_row, column=0)
            server.plugin_button.grid(row=self.this_row, column=1)
            self.this_row += 1
        self.create_menu()

    def create_menu(self):
        """Create a menu bar with 'File' and 'Open Servers Folder' options."""
        menubar = tk.Menu(self.master)

        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Servers Folder",
                             command=self.open_servers_folder)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)

        menubar.add_cascade(label="File", menu=filemenu)

        # Set the menu to the window
        self.master.config(menu=menubar)

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
        subprocess_run(command)
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

    def open_servers_folder(self):
        """Open a folder chooser dialog and update the servers directory."""
        selected_folder = filedialog.askdirectory(
            initialdir=self.servers_dir,
            title="Select Servers Folder")

        if selected_folder:
            self.servers_dir = selected_folder
            self.refresh_servers()  # Optionally refresh the servers after folder change
        else:
            messagebox.showinfo("Cancelled", "No folder selected.")

    def refresh_servers(self):
        """Refresh the server list after changing servers directory."""
        # Logic to refresh the server list, based on self.servers_dir
        self.servers = OrderedDict()
        for sub in os.listdir(self.servers_dir):
            sub_path = os.path.join(self.servers_dir, sub)
            if not os.path.isdir(sub_path):
                continue
            server_info = ServerInfo()
            server_info.load(sub_path)
            if not server_info.ready:
                continue
            server_info.refresh_plugins(opener=self.default_plugin_name)
            self.servers[sub] = server_info
        self.create_widgets()


def main():
    root = tk.Tk()
    root.title("Plugin Manager")

    # Get screen width and height
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Calculate desired window size (15% width, 30% height of the screen)
    window_w = int(screen_w * 0.15)
    window_h = int(screen_h * 0.3)

    # Set window size and position to the center
    root.geometry("%dx%d+%d+%d" % (window_w, window_h, (screen_w - window_w) / 2, (screen_h - window_h) / 2))

    app = PluginManagerApp(root)
    app.pack()
    root.mainloop()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
