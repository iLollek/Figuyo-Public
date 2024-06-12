import customtkinter as ctk
from datetime import datetime
from FiguyoDataAccess import *
from ResourceFetcher import ResourceFetcher

rf = ResourceFetcher()


class SearchFigureGUI:
    def __init__(self, root, callback, callback_clear, callback_updatestats):
        self.root = root
        self.callback = callback
        self.callback_clear = callback_clear
        self.callback_updatestats = callback_updatestats

        self.root.title("Search Figure in Database")
        self.root.geometry("400x400")
        self.root.resizable(width=False, height=False)


        # Search Fields
        self.name_entry = ctk.CTkEntry(master=root, placeholder_text="Figure Name")
        self.name_entry.pack(pady=(20, 10))

        self.canonname_entry = ctk.CTkEntry(master=root, placeholder_text="Canonical Name")
        self.canonname_entry.pack(pady=(10, 10))

        self.origin_entry = ctk.CTkEntry(master=root, placeholder_text="Origin (Anime/Manga)")
        self.origin_entry.pack(pady=(10, 10))

        self.price_entry = ctk.CTkEntry(master=root, placeholder_text="Price")
        self.price_entry.pack(pady=(10, 10))

        self.price_operator_var = ctk.StringVar(value=">")
        self.price_operator_optionmenu = ctk.CTkOptionMenu(master=root, values=[">", "<", ">=", "<=", "="], variable=self.price_operator_var)
        self.price_operator_optionmenu.pack(pady=(10, 10))

        self.weight_entry = ctk.CTkEntry(master=root, placeholder_text="Weight")
        self.weight_entry.pack(pady=(10, 10))

        self.weight_operator_var = ctk.StringVar(value=">")
        self.weight_operator_optionmenu = ctk.CTkOptionMenu(master=root, values=[">", "<", ">=", "<=", "="], variable=self.weight_operator_var)
        self.weight_operator_optionmenu.pack(pady=(10, 10))

        # Search Button
        self.search_button = ctk.CTkButton(master=root, text="Search", command=self.search)
        self.search_button.pack(pady=(20, 20))

    def search(self):
        name = self.name_entry.get()
        canonname = self.canonname_entry.get()
        origin = self.origin_entry.get()
        price = self.price_entry.get()
        price_operator = self.price_operator_var.get()
        weight = self.weight_entry.get()
        weight_operator = self.weight_operator_var.get()

        results = []
        data_access = FiguyoDataAccess()

        if name:
            results.extend(data_access.find_figure_by_name(name))
        if canonname:
            results.extend(data_access.find_figure_by_canonname(canonname))
        if origin:
            results.extend(data_access.find_figure_by_herkunft(origin))
        if price:
            results.extend(data_access.find_figure_by_price(price_operator, float(price)))
        if weight:
            results.extend(data_access.find_figure_by_weight(weight_operator, int(weight)))

        self.callback_clear()

        # Load results into the main GUI view
        for figure in results:
            self.callback(
                name=figure.name,
                canonname=figure.canonname,
                origin=figure.herkunft,
                releasedate=figure.erscheinungsdatum,
                weight=figure.gewicht,
                price=figure.preis
            )

        self.callback_updatestats()
        self.root.destroy()
