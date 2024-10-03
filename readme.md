# MoreServers
Install your plugin and launch multiple server versions quickly.

**MoreServers** is a user-friendly plugin manager GUI designed to manage Java `.jar` plugins for multiple servers. It automatically detects all server directories within a specified location and allows you to install plugins into any server with a single click.

## Features

- **Automatic Server Detection**: Scans your servers directory and lists all detected server instances.
- **One-Click Plugin Installation**: Install `.jar` plugins into your servers effortlessly with just one click.
- **Easy Plugin Management**: Refresh, manage, and organize plugins for each server from a centralized GUI.
- **Server Launch Control**: Start and manage your servers directly from the GUI.
- **Cross-Platform**: Works on Linux, macOS, and Windows systems.

## Requirements

- Python 3.7 or higher
- `Tkinter` (bundled with most Python installations)
- Java `.jar` plugin files

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/moreservers.git
    cd moreservers
    ```

2. **Install the package** using `pip`:
    ```bash
    pip install .
    ```

3. **Run the GUI**:
    After installation, you can launch the GUI with:
    ```bash
    moreservers-gui
    ```

## Usage

1. **Server Detection**:
    - The GUI automatically scans the `servers/` directory, detecting all server folders and organizing them in the interface.

2. **Plugin Installation**:
    - Place your plugin `.jar` files into the `servers/plugins/` directory.
    - From the GUI, select a server and click to install a plugin with just one click. The plugin will be installed in the selected server’s `plugins/` folder.

3. **Server Launch**:
    - Choose a server from the list in the GUI and click the "Launch" button to start the server.

4. **Refresh Plugins**:
    - You can refresh the plugin list for each server by selecting the server and clicking the "Refresh Plugins" button.

## Example

Once installed and launched:

1. **Add servers**: Ensure your servers are placed in the `servers/` directory.
2. **Add plugins**: Place plugin `.jar` files in the `plugins/` subdirectory of each server.
3. **Manage plugins**: Use the GUI to install and refresh plugins.
4. **Launch servers**: Click "Launch" to start any server listed in the GUI.

## Contributing

We welcome contributions! If you'd like to contribute, please feel free to submit a pull request or report any issues via [GitHub](https://github.com/yourusername/moreservers/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
- See [Issues](https://github.com/Poikilos/MoreServers/issues)
