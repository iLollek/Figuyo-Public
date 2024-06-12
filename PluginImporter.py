import importlib.util
from pathlib import Path
from typing import Type
from Plugins.BasePlugin import FiguyoBasePlugin

def load_plugin(plugin_path: str) -> Type[FiguyoBasePlugin]:
    spec = importlib.util.spec_from_file_location("plugin", plugin_path)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)

    for name in dir(plugin_module):
        obj = getattr(plugin_module, name)
        if isinstance(obj, type) and issubclass(obj, FiguyoBasePlugin) and obj is not FiguyoBasePlugin:
            return obj

    raise ValueError("No FiguyoBasePlugin subclass found in plugin file")

def GetAllPlugins() -> list[Type[FiguyoBasePlugin]]:
    plugin_folder = Path("Plugins")
    plugin_files = plugin_folder.glob("*.py")
    Plugins = []

    for plugin_file in plugin_files:
        plugin_class = None
        try:
            plugin_class = load_plugin(str(plugin_file))
            Plugins.append(plugin_class)
        except ValueError:
            pass

    return Plugins

def GetAllPluginNames() -> list[str]:
    """Returns all available Plugins names in a list of strings.
    
    Returns:
        - plugin names list[str]: A list of available Plugin names"""

    plugin_classes = GetAllPlugins()
    plugin_names = [plugin_class.__name__ for plugin_class in plugin_classes]
    return plugin_names

def GetPluginByName(name: str) -> FiguyoBasePlugin:
    """Returns a Plugin Instance by it's Name.
    
    Args:
        - name (str): The Name of the Plugin
        
    Returns:
        - FiguyoBasePlugin: The Instance of the Plugin"""
    
    for plugin_class in GetAllPlugins():
        plugin_instance = plugin_class(None)
        print(f'Target: {name} - Cursor: {plugin_instance.GetPluginFilename()}')
        if plugin_instance.GetPluginFilename() == name:
            return plugin_class

if __name__ == "__main__":
    plugin_classes = GetAllPlugins()
    for plugin_class in plugin_classes:
        plugin_instance = plugin_class(None) # None should be instancedata
        # Now you can work with each plugin instance as needed
        print(plugin_instance.GetPluginDescription())
