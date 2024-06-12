import customtkinter as ctk
from tkinter import Toplevel
from PIL import Image, ImageTk
import base64
import io
from FiguyoDataAccess import FiguyoFigure

from ResourceFetcher import ResourceFetcher

rf = ResourceFetcher()

class FigureViewGUI:
    def __init__(self, master, figure: FiguyoFigure):
        self.master = master
        master.title(f"View Figure: {figure.name}")
        master.geometry("400x500")
        master.resizable(False, False)

        self.figure = figure

        self.name_label = ctk.CTkLabel(master, text=f"Figure Name: {figure.name}")
        self.name_label.pack(pady=5)

        self.canonname_label = ctk.CTkLabel(master, text=f"Character Name: {figure.canonname}")
        self.canonname_label.pack(pady=5)

        self.herkunft_label = ctk.CTkLabel(master, text=f"Origin: {figure.herkunft}")
        self.herkunft_label.pack(pady=5)

        self.erscheinungsdatum_label = ctk.CTkLabel(master, text=f"Release Date: {figure.erscheinungsdatum}")
        self.erscheinungsdatum_label.pack(pady=5)

        self.preis_label = ctk.CTkLabel(master, text=f"Price: {figure.preis} €")
        self.preis_label.pack(pady=5)

        self.gewicht_label = ctk.CTkLabel(master, text=f"Weight: {figure.gewicht} g")
        self.gewicht_label.pack(pady=5)

        self.photo_label = ctk.CTkLabel(master, text="Photo")
        self.photo_label.pack(pady=5)

        # Decode and display the photo
        photo_data = base64.b64decode(figure.photo)
        image = Image.open(io.BytesIO(photo_data))
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.photo_image_label = ctk.CTkLabel(master, image=photo, text="")
        self.photo_image_label.image = photo  # Keep a reference
        self.photo_image_label.pack(pady=5)

        self.close_button = ctk.CTkButton(master, text="Close", command=master.destroy)
        self.close_button.pack(pady=20)

    def GetInstancedataFigure(self):
        """Returns the FiguyoFigure Model currently loaded into the View.
        
        Returns:
            - FiguyoFigure: The Figuyo Figure that is currently loaded"""
        
        return self.figure

if __name__ == "__main__":
    from FiguyoDataAccess import FiguyoDataAccess

    # Create an instance of FiguyoDataAccess
    data_access = FiguyoDataAccess()

    # Fetch a figure for demonstration
    figure_list = data_access.get_all_figures()
    for figure in figure_list:
        print(figure)

        root = ctk.CTk()
        app = FigureViewGUI(root, figure)
        root.mainloop()

        break
