#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import subprocess
import sys
from collections import OrderedDict

if sys.version_info.major >= 3:
    import tkinter as tk
    from tkinter import font
    # NOTE: tk.font does not work.
    from tkinter import messagebox, filedialog
else:
    import Tkinter as tk
    import tkFont as font
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


def toggle_bold(button, bold):
    """Toggle the button text between bold and normal based on the 'bold' argument."""
    try:
        # Attempt to get the named font if it exists
        current_font = font.nametofont(button.cget("font"))
    except tk.TclError:
        # If no named font exists, create a new Font object based on the current font settings
        current_font = font.Font(font=button.cget("font"))
    
    # Create a copy of the font and update the weight based on the 'bold' argument
    new_font = current_font.copy()
    new_font.config(weight="bold" if bold else "normal")
    
    # Apply the new font to the button
    button.config(font=new_font)


class PluginManagerApp(tk.Frame):
    def __init__(self, parent):
        self.last_server = None
        self.servers_dir = os.getcwd()
        self.root = parent.winfo_toplevel()

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
            server.launch_button = tk.Button(
                self, text="Launch %s" % server_name,
                command=lambda s=server: self.run_server(s))
            server.plugin_button = tk.Button(
                self, text="Install Plugin %s" % plugin_name,
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
        filemenu.add_command(label="Refresh Servers Folder",
                             command=self.refresh_servers)
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
            messagebox.showerror(
                "Error",
                "Could not find any terminal programs"
            )
            return False
        os.chdir(server.path)
        self.enable_buttons(False)
        if self.check_server(toggle_enable=True):
            return False
        self.last_server = server
        toggle_bold(server.launch_button, True)
        self.root.after(1, self.start_server)
        # ^ ms (int)
        return True

    def check_server(self, silent=False, toggle_enable=False):
        if self.last_server:
            if self.last_server.is_running():
                if not silent:
                    messagebox.showerror(
                        "Error",
                        ("Server %s (Process ID %s) is already running."
                        % (self.last_server.command_parts,
                            self.last_server.pid))
                    )
                if self.last_server.launch_button:
                    toggle_bold(self.last_server.launch_button, True)
                return True
            else:
                if self.last_server.launch_button:
                    toggle_bold(self.last_server.launch_button, False)
        if toggle_enable:
            self.enable_buttons(True)
        return False

    def show_ex(self, ex):
        messagebox.showerror(
            type(ex).__name__,
            str(ex)
        )

    def start_server(self):
        server = self.last_server
        try:
            command_parts = [self.gui_term_path] + self.gui_term_args[self.gui_term_name] + [self.launcher_path]
            # subprocess_run(server.command_parts)
            # server.run_jar_with(
            #     self.gui_term_path,
            #     self.gui_term_args[self.gui_term_name] + [self.launcher_path],
            # )
            server.run_custom(command_parts, callback=self.refresh_servers)
        except Exception as ex:
            self.show_ex(ex)
            self.enable_buttons(True)
            raise

    def enable_buttons(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        for server_name, server in self.servers.items():
            if server.launch_button:
                server.launch_button['state'] = state
            if server.plugin_button:
                if not server.ready:
                    server.launch_button['state'] = tk.DISABLED
                else:
                    server.plugin_button['state'] = state


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
        for sub in sorted(os.listdir(self.servers_dir)):
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
        self.check_server(silent=True)


def main():
    root = tk.Tk()
    root.title("More Servers")

    # Get screen width and height
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Calculate desired window size (15% width, 30% height of the screen)
    window_w = int(screen_w * 0.5)
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
