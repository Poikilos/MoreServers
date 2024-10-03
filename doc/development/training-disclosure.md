# Training Disclosure for MoreServers
This Training Disclosure, which may be more specifically titled above here (and in this disclosure possibly referred to as "this disclosure"), is based on Training Disclosure version 1.0.0 at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission implies unless stated elsewhere is of direct human origin to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This document is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this document lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this document contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- GPT-4-Turbo (Version 4o, chatgpt.com)

Scope of use: code described in subsections--typically modified by hand to improve logic, variable naming, integration, etc.


## moreservers
Make a new class called PluginInfo. For the selected jar file, use plugin_info.load(sub_path). set self.path to the value. then set _, self.filename = os.path.split(self.path). then parts = filename.split("("). If there is only 1 part, set self.name = parts[0].split(".")[0], otherwise set it to parts[0]. Make a global function get_jars(parent, opener=None) method to return a list of paths. In it, check each sub in the parent directory, storing full path in sub_path. If not file, continue (short-circuit logic). If not lower().endswith(".jar") continue (short-circuit logic). If opener and not sub.lower().startswith(opener.lower()) continue (short-circuit logic). After all those are stored in a matching_plugins_paths list, sort alphabetically and return the resulting sorted list. Make a new class called ServerInfo. Let it have a load function that accepts a directory path named server_dir. In load, set self.name = os.path.split(server_dir)[1] and set self.path = server_dir. set self.launch_jars = get_jars(server_dir). If the list len is != 1, show ValueError "expected one jar got %s" % self.launch_jars. set self.plugins_path = os.path.join(server_dir, "plugins"). Call a separate method, refresh_plugins(self, opener=None) that sets self.plugin_jars = get_jars(self.plugins_path, opener) if isdir self.plugins_path else None. If not None, reset self.plugins = [], then iterate through plugin_jars for each set plugin = PluginInfo() then call plugin.load(plugin_jar) and append plugin to self.plugins. Also set self.opener = opener. Make an install_plugin method that accepts a path. First, it should set new_plugin = PluginInfo() then call new_plugin.load(path). for each plugin in self.plugins, if new_plugin.name.lower() == plugin.name.lower() return "%s is already installed" % plugin.path. After that loop, set dst_path = os.path.join(self.plugins_path, new_plugin.filename) and do shutil.copy(new_plugin.path, dst_path) and return 'Installed "%s"' % dst_path. Make an object-oriented Tkinter Python Frame. Set self.default_plugin_name = "CustomRecipes". Set self.repo_dir = os.path.dirname(os.path.realpath(__file__)). Set self.launcher_path to os.path.join(self.repo_dir, "launch-server.sh"). use shutil.which to determine which to use, in order of most preferred first, iterating through keys of an OrderedDict called self.gui_term_args where keys are xfce-terminal, mate-terminal, konsole, gnome-terminal, xterm, and each value is a list of arguments that must precede a bash script path and its arguments if special arguments are necessary for any of those terminal GUIs to launch a script with an argument, otherwise set the list to blank for that specific key if not necessary for that specific terminal's command syntax (if a bash script can be the first argument and no others are required). If none of those keys are found with shutil.which (if self.gui_term_path was not set), show an error in a messagebox and set self.enable_launch=False otherwise set it to True and set self.gui_term_path to the first one found with shutil.which in the OrderedDict. Set matching_plugins_paths = get_jars(os.getcwd(), opener=self.default_plugin_name), and set self.plugin_src = matching_plugins_paths[-1] if matching_plugins_paths else None. For each sub_path set this_server = ServerInfo() then call this_server.load(sub_path), then call this_server.refresh_plugins(opener=self.default_plugin_name). Set an OrderedDict self.servers[sub] = server_info. After all that, loop for server in self.servers. Each should generate a two buttons side by side using the grid method and iterate self.this_row. store the left button in server.launch_button and the right one in server.plugin_button. When any launch_button is clicked, if not self.gui_term_path, show a messagebox saying "Could not find any of: %s" % self.gui_term_names. Otherwise, the text of the button is used as an arg to run a "run" method. That method runs [self.gui_term_path] + self.gui_term_args[self.gui_term_name] + [self.launcher_path] using server.path as the working directory. When any plugin_button is clicked, it should run server.install_plugin(self.plugin_src). If the return is not None, show a messagebox with the returned string.

if sys.version_info.major >= 3 import subprocess.run as subprocess_run otherwise define a subprocess_run function that takes the same arguments we use in the program and is compatible with python 2.

### moreserverstk
put the main code in a main function returning 0 at the end, so the __main__ case only includes sys.exit(main()). start with a python shebang then for compatibility, from __future__ import print_function.

Assume the other classes don't have to change, and lets work on PluginManagerApp. Add a File, Open Servers Folder item that
launches a tk folder chooser dialog where you can set self.servers_dir unless cancelled.

Get the screen width and height then set the size of the tk window to screen_w*.15, screen_h*.3

## setup.py
Assume that main function is in moreservers.moreserverstk.py and make a corresponding setup.py file that defines a gui launch script. Be descriptive and use classifiers.


## readme.md
Create a readme.md file

Reword it to explain that all servers in your servers directory are detected and plugins in that same directory can be easily installed into a server with one click.
