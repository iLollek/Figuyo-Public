import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import base64
from tkcalendar import Calendar
from FiguyoDataAccess import FiguyoDataAccess, FiguyoFigure
from datetime import datetime
import PopupView
from ResourceFetcher import ResourceFetcher

rf = ResourceFetcher()


class AddFigureGUI:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        master.title("Add New Figuyo Anime Figure")
        master.geometry("400x900")
        master.resizable(False, False)

        self.name_label = ctk.CTkLabel(master, text="Figure Name")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(master, width=300)
        self.name_entry.pack(pady=5)

        self.canonname_label = ctk.CTkLabel(master, text="Character Name")
        self.canonname_label.pack(pady=5)
        self.canonname_entry = ctk.CTkEntry(master, width=300)
        self.canonname_entry.pack(pady=5)

        self.herkunft_label = ctk.CTkLabel(master, text="Origin")
        self.herkunft_label.pack(pady=5)
        self.herkunft_entry = ctk.CTkEntry(master, width=300)
        self.herkunft_entry.pack(pady=5)

        self.erscheinungsdatum_label = ctk.CTkLabel(master, text="Release Date")
        self.erscheinungsdatum_label.pack(pady=5)
        self.erscheinungsdatum_entry = Calendar(master)
        self.erscheinungsdatum_entry.pack(pady=5)

        self.preis_label = ctk.CTkLabel(master, text="Price (€)")
        self.preis_label.pack(pady=5)
        self.preis_entry = ctk.CTkEntry(master, width=300)
        self.preis_entry.pack(pady=5)

        self.gewicht_label = ctk.CTkLabel(master, text="Weight (g)")
        self.gewicht_label.pack(pady=5)
        self.gewicht_entry = ctk.CTkEntry(master, width=300)
        self.gewicht_entry.pack(pady=5)

        self.photo_label = ctk.CTkLabel(master, text="Photo")
        self.photo_label.pack(pady=5)
        self.photo_path = ctk.CTkEntry(master, width=200)
        self.photo_path.pack( pady=5)
        self.photo_button = ctk.CTkButton(master, text="Browse", command=self.load_photo)
        self.photo_button.pack(pady=5)

        self.photo_image_label = ctk.CTkLabel(master, text="")
        self.photo_image_label.pack()

        self.submit_button = ctk.CTkButton(master, text="Add Figure", command=self.submit)
        self.submit_button.pack(pady=20, anchor="s")

    def load_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.photo_path.delete(0, ctk.END)
            self.photo_path.insert(0, file_path)
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.photo_image_label.configure(image=photo, text="")
            self.photo_image_label.image = photo

    def submit(self):
        data_access = FiguyoDataAccess()

        name = self.name_entry.get()
        canonname = self.canonname_entry.get()
        herkunft = self.herkunft_entry.get()
        erscheinungsdatum = self.erscheinungsdatum_entry.get_date()
        print(erscheinungsdatum)
        preis = float(self.preis_entry.get().replace(",", "."))
        gewicht = int(self.gewicht_entry.get())
        photo_path = self.photo_path.get()

        with open(photo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        self.master.destroy()
        data_access.create_figure(name, canonname, herkunft, datetime.strptime(erscheinungsdatum, '%m/%d/%y').date(), preis, gewicht, encoded_string)
        PopupView.show_info_box(f'Figuyo | Figure added!', f'{name} has been added to the Database Successfully!')
        self.callback()


if __name__ == "__main__":
    root = ctk.CTk()
    app = AddFigureGUI(root)
    root.mainloop()
