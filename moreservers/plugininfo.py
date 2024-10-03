import os

class PluginInfo:
    def __init__(self):
        self.path = None
        self.name = None
        self.filename = None

    def load(self, sub_path):
        """
        Load the plugin from the given sub_path.

        Args:
            sub_path (str): Path to the plugin jar file.
        """
        self.path = sub_path
        _, self.filename = os.path.split(self.path)
        parts = self.filename.split("(")
        if len(parts) == 1:
            self.name = parts[0].split(".")[0]
        else:
            self.name = parts[0]
