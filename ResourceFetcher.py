import os
import sys

class ResourceFetcher:
    def __init__(self):
            self.env = self.determine_prod_or_dev_env()
            if self.env == "DEV":
                self.basepath = self.development_resource_path() + "\\"
            elif self.env == "PROD":
                self.basepath = self.productive_resource_path() + "\\"

    def productive_resource_path(self):
        """ Gets the AppData Resource Path """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
            return base_path
        except Exception:
            base_path = os.path.abspath(".")
            return base_path

    def development_resource_path(self) -> str:
        """ Gets the Docs Resource Path """

        return os.getcwd() + f"\\Content\\Icons"

    def determine_prod_or_dev_env(self) -> str:
        """Internal Function used to determine if the Script is running in a DEV or PROD Environment.
        
        Returns:
            - Environment (str): The Environment (PROD or DEV)"""
        if getattr(sys, 'frozen', False):
            return "PROD"
        else:
            return "DEV"

    def GetResource(self, filename: str) -> str:
        """Returns the path to the Resource based on the Environment.

        Args:
            - filename (str): The name of the File.
        
        Returns:
            - filepath (str): The Path to the Resource."""

        return self.basepath + filename