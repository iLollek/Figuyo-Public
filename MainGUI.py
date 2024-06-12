import customtkinter as ctk
from CTkMenuBar import *
import PluginImporter
import AboutGUI
import AddFigureToDBGUI
import SearchFigureGUI
import FiguyoDetailGUI
from datetime import datetime
from FiguyoDataAccess import FiguyoDataAccess, FiguyoFigure
from CTkTable import CTkTable
from functools import partial
from tkinter import filedialog
import PopupView
import shutil
import os
from ResourceFetcher import ResourceFetcher

rf = ResourceFetcher()

data_access = FiguyoDataAccess()

ctk.set_appearance_mode("system")

class App:
    def __init__(self, root):
        root.title("Figuyo")
        root.geometry("800x600")
        root.resizable(width=True, height=True)
        root.iconbitmap(rf.GetResource(f'by2icon-min.ico'))

        self.about_window = None
        self.add_figure_window = None
        self.figure_detailview = None
        self.figure_search = None
        self.instancedata = None

        menu = CTkMenuBar(root)
        menubutton_file = menu.add_cascade("File")
        menubutton_plugins = menu.add_cascade("Plugins")
        menubutton_about = menu.add_cascade("About", postcommand=self.open_about)

        dropdown_filemenu = CustomDropdownMenu(widget=menubutton_file)
        dropdown_filemenu.add_option(option="Import .fff File", command=lambda: self.import_fff_into_database(filedialog.askopenfilename(
        title="Select a .fff file",
        filetypes=(("FFF files", "*.fff"), ("All files", "*.*")),
        defaultextension=".fff"
    )))
        dropdown_filemenu.add_option(option="Export Database", command=self.export_database)

        dropdown_pluginsmenu = CustomDropdownMenu(widget=menubutton_plugins)
        submenu_pluginsmenu = dropdown_pluginsmenu.add_submenu("Run Plugin")
        dropdown_pluginsmenu.add_option(option="Import Plugin from File", command=lambda: self.import_plugin(filedialog.askopenfilename(
        title="Select a .py file",
        filetypes=(("Python File", "*.py"), ("All files", "*.*")),
        defaultextension=".py"
    )))

        for plugin_name in PluginImporter.GetAllPluginNames():
            action_with_arg = partial(self.run_plugin, plugin_name)
            submenu_pluginsmenu.add_option(option=plugin_name, command=action_with_arg)

        bottom_bar_frame = ctk.CTkFrame(root)
        bottom_bar_frame.pack(side="top", fill="x")

        button1 = ctk.CTkButton(bottom_bar_frame, text="📝 Add new Figure to Database", command=self.open_add_figure)
        button1.pack(side="left")

        button2 = ctk.CTkButton(bottom_bar_frame, text="🔍 Search for Figure in Database", command=self.open_search_figure)
        button2.pack(side="left")

        self.infolabel = ctk.CTkLabel(bottom_bar_frame, text="Figures in Database: 0 - Total: 0€")
        self.infolabel.pack(side="left", padx=(10))
        
        self.sheet_frame = ctk.CTkFrame(root, corner_radius=25)
        self.sheet_frame.pack()

        self.maintable = CTkTable(master=self.sheet_frame, column=6, row=0, values=[["Figure Name", "Character Name", "Origin", "Release Date", "Weight", "Price"]], hover_color="blue", command=self.open_figure_detailview)
        self.maintable.pack(expand=True, fill='both')
        self.maintable.edit_row(row=0, height=10)

        self.LoadAllFiguresFromDatabase()
        self.UpdateStats()

    def import_plugin(self, filepath: str):
        """Imports a Plugin (a .py File inheriting from the BasePlugin Class)"""
        try:
            plugin = PluginImporter.load_plugin(filepath)

            plugin_instance = plugin(None)

            PopupView.show_info_box(f'Plugin Information', f'Name: {plugin_instance.GetPluginName()}\nDescription: {plugin_instance.GetPluginDescription()}\nAuthor: {plugin_instance.GetPluginAuthor()}\nVersion: {plugin_instance.GetPluginVersion()}')

            src = filepath
            dst = f'Plugins\\{os.path.basename(filepath)}'
            shutil.copy(src, dst)

            PopupView.show_info_box(f'Plugin Imported Successfully!', f'The Plugin {plugin_instance.GetPluginName()} by {plugin_instance.GetPluginAuthor()} has been imported successfully. It will show up in your GUI after a restart.')

        except Exception as e:
            PopupView.show_error_box(f'Import Failed!', f'The Import of the Plugin-File at {filepath} failed: {e}')


    def export_database(self):
        """Exports (copies) the Database to the Users Desktop."""

        try:
            src = "Figuyo.db"
            dst = os.path.join(os.path.expanduser("~"), "Desktop")

            shutil.copy(src, dst)

            PopupView.show_info_box(f'Database Export Successful!', f'Your Database (Figuyo.db) has been Exported to your Desktop Successfully.')
        except Exception as e:
            PopupView.show_error_box(f'Error exporting Database!', f'Unable to Export your Database (Figuyo.db) to your Desktop: {e}')

    def import_fff_into_database(self, fff_filepath: str):
        """
        Imports a .fff (Figuyo Figure File) into the database.

        :param fff_filepath: Path to the .fff file.
        """
        try:
            with open(fff_filepath, 'r', encoding='utf-8') as fff_file:
                # Initialize an empty dictionary to hold the figure's data
                figure_data = {}

                for line in fff_file:
                    # Skip empty lines or lines that are comments
                    if line.strip() == '' or line.strip().startswith('#'):
                        continue

                    # Split the line into key and value based on the $$$ delimiter
                    key, value = line.strip().split(' $$$ ')

                    # Map the keys to the respective fields in the FiguyoFigure model
                    if key == 'name':
                        figure_data['name'] = value
                    elif key == 'canonname':
                        figure_data['canonname'] = value
                    elif key == 'origin':
                        figure_data['herkunft'] = value
                    elif key == 'release':
                        figure_data['erscheinungsdatum'] = datetime.strptime(value, '%Y-%m-%d').date()
                    elif key == 'price':
                        figure_data['preis'] = float(value)
                    elif key == 'weight':
                        figure_data['gewicht'] = int(value)
                    elif key == 'photo':
                        figure_data['photo'] = value

                # Use the data_access instance to create a new figure in the database
                data_access.create_figure(
                    name=figure_data['name'],
                    canonname=figure_data['canonname'],
                    herkunft=figure_data['herkunft'],
                    erscheinungsdatum=figure_data['erscheinungsdatum'],
                    preis=figure_data['preis'],
                    gewicht=figure_data['gewicht'],
                    photo=figure_data['photo']
                )

                PopupView.show_info_box(f'Import Successful!', f'Imported {figure_data["name"]} into your Database successfully.')
                self.ClearTable()
                self.LoadAllFiguresFromDatabase()
                self.UpdateStats()
        except Exception as e:
            PopupView.show_error_box(f'Import Failed!', f'The Import Failed. Exception: {e}')

    def run_plugin(self, name: str):
        plugin_class = PluginImporter.GetPluginByName(name)
        plugin_instance = plugin_class(self.instancedata) # This should be instancedata later
        plugin_instance.Run()

    def open_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = ctk.CTkToplevel()
            self.about_window.iconbitmap(rf.GetResource(f'by2icon-min.ico'))
            AboutGUI.FiguyoApp(self.about_window)
            self.about_window.protocol("WM_DELETE_WINDOW", self.on_about_close)

    def on_about_close(self):
        self.about_window.destroy()
        self.about_window = None

    def open_add_figure(self):
        if self.add_figure_window is None or not self.add_figure_window.winfo_exists():
            self.add_figure_window = ctk.CTkToplevel()
            self.add_figure_window.iconbitmap(rf.GetResource(f'by2icon-min.ico'))
            AddFigureToDBGUI.AddFigureGUI(self.add_figure_window, self.LoadAllFiguresFromDatabase)
            self.add_figure_window.protocol("WM_DELETE_WINDOW", self.on_add_figure_close)

    def on_add_figure_close(self):
        self.add_figure_window.destroy()
        self.add_figure_window = None
        self.LoadAllFiguresFromDatabase()

    def open_search_figure(self):
        if self.figure_search is None or not self.figure_search.winfo_exists():
            self.figure_search = ctk.CTkToplevel()
            self.figure_search.iconbitmap(rf.GetResource(f'by2icon-min.ico'))
            SearchFigureGUI.SearchFigureGUI(self.figure_search, self.AddFigureToView, self.ClearTable, self.UpdateStats)
            self.figure_search.protocol("WM_DELETE_WINDOW", self.on_search_figure_close)

    def on_search_figure_close(self):
        self.figure_search.destroy()
        self.figure_search = None

    def open_figure_detailview(self, ctktable_information):
        if ctktable_information["row"] != 0:
            FiguyoFigure = data_access.find_figure_by_name(self.maintable.get_row(ctktable_information["row"])[0])
            if self.figure_detailview is None or not self.figure_detailview.winfo_exists():
                self.instancedata = FiguyoFigure
                self.figure_detailview = ctk.CTkToplevel()
                self.figure_detailview.iconbitmap(rf.GetResource(f'by2icon-min.ico'))
                FiguyoDetailGUI.FigureViewGUI(self.figure_detailview, FiguyoFigure)
                self.figure_detailview.protocol("WM_DELETE_WINDOW", self.on_figure_detailview_close)

    def on_figure_detailview_close(self):
        self.figure_detailview.destroy()
        self.figure_detailview = None
        self.instancedata = None

    def AddFigureToView(self, name: str, canonname: str, origin: str, releasedate: datetime, weight: int, price: float):
        """Adds a Figure into the Main UI View Table
        
        Args:
            - name (str): The Name of the Figure
            - canonname (str): The Name of the Character
            - origin (str): The Origin Series / Movie / Manga of the Character
            - releasedate (datetime): The release date of the Figure
            - weight (int): The weight of the figure, in grams (g)
            - price (float): The Price of the figure, in Euro (€)"""
        
        figure_data = [name, canonname, origin, releasedate.strftime("%d.%m.%Y"), f'{weight}g', f'{price}€']

        self.maintable.add_row(index=1, height=10, values=figure_data)

    def ClearTable(self):
        """Clears the Table completely, only leaving the first row"""

        for i in range(1, len(self.maintable.get())):
            self.maintable.delete_row(i)

    def LoadAllFiguresFromDatabase(self):
        """Clears the previous Table (Calls ClearTable()) and then loads all Figures from Database back in"""

        self.ClearTable()

        figures = data_access.get_all_figures()

        
        if figures:
            for figure in figures:
                figure: FiguyoFigure
                figure_data = [figure.name, figure.canonname, figure.herkunft, figure.erscheinungsdatum.strftime("%d.%m.%Y"), f'{figure.gewicht}g', f'{figure.preis}€']

                self.maintable.add_row(index=1, height=10, values=figure_data)

    def UpdateStats(self):
        """Updates the Stats with the Information that is currently viewed"""

        figures = len(self.maintable.get()) - 1 
        total = 0.0
        
        for price in self.maintable.get_column(5):
            if price != "Price":
                price = price.replace("€", "")
                total = float(price) + total

        self.infolabel.configure(text=f"Figures: {figures} - Total: {round(total, 2)}€")
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
