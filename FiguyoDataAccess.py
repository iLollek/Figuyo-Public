# Figuyo DataAccess - Enabling even faster Database Access!
# make me sad, make me mad, make me feel... alright?
# https://youtu.be/qqMxcydQmxI?si=631jv8jMdUY9rmbV

import sillyorm
from sillyorm.dbms import sqlite
import datetime


class FiguyoDataAccess:
    """
    Data Access class for the Figuyo application.
    Provides methods to interact with the FiguyoFigure database table.
    """

    def __init__(self, db_path="Figuyo.db"):
        """
        Initializes the FiguyoDataAccess instance and sets up the database environment.

        :param db_path: Path to the SQLite database file.
        """
        self.env = sillyorm.Environment(
            sqlite.SQLiteConnection(db_path).cursor()
        )
        self.env.register_model(FiguyoFigure)

    def create_figure(self, name, canonname, herkunft, erscheinungsdatum, preis, gewicht, photo):
        """
        Creates a new FiguyoFigure record in the database.

        :param name: The name of the figure.
        :param canonname: The canonical name of the figure.
        :param herkunft: The origin of the figure.
        :param erscheinungsdatum: The release date of the figure.
        :param preis: The price of the figure.
        :param gewicht: The weight of the figure.
        :param photo: Base64 encoded image data of the figure.
        :return: The created FiguyoFigure record.
        """
        figure_data = {
            "name": name,
            "canonname": canonname,
            "herkunft": herkunft,
            "erscheinungsdatum": erscheinungsdatum,
            "preis": preis,
            "gewicht": gewicht,
            "photo": photo
        }
        return self.env["FiguyoFigure"].create(figure_data)

    def get_all_figures(self):
        """
        Retrieves all FiguyoFigure records from the database.

        :return: A list of FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([])

    def find_figure_by_name(self, name):
        """
        Finds FiguyoFigure records by name.

        :param name: The name of the figure to search for.
        :return: A list of matching FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([("name", "=", name)])
    
    def find_figure_by_price(self, operator, price):
        """
        Finds FiguyoFigure records by price.

        :param operator: The operator for comparison (">", "<", ">=", "<=", "=").
        :param price: The price to compare against.
        :return: A list of matching FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([("preis", operator, price)])

    def find_figure_by_weight(self, operator, weight):
        """
        Finds FiguyoFigure records by weight.

        :param operator: The operator for comparison (">", "<", ">=", "<=", "=").
        :param weight: The weight to compare against.
        :return: A list of matching FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([("gewicht", operator, weight)])

    def find_figure_by_canonname(self, canonname):
        """
        Finds FiguyoFigure records by canonical name.

        :param canonname: The canonical name of the figure to search for.
        :return: A list of matching FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([("canonname", "=", canonname)])

    def find_figure_by_herkunft(self, herkunft):
        """
        Finds FiguyoFigure records by origin.

        :param herkunft: The origin of the figure to search for.
        :return: A list of matching FiguyoFigure records.
        """
        return self.env["FiguyoFigure"].search([("herkunft", "=", herkunft)])


class FiguyoFigure(sillyorm.model.Model):
    """
    Model class representing the FiguyoFigure table in the database.
    """
    _name = "FiguyoFigure"  # database table name & name in environment

    # fields
    name = sillyorm.fields.String(length=255)
    canonname = sillyorm.fields.String(length=255)
    herkunft = sillyorm.fields.String(length=255)
    erscheinungsdatum = sillyorm.fields.Date()
    preis = sillyorm.fields.Float()
    gewicht = sillyorm.fields.Integer()
    photo = sillyorm.fields.Text()  # Contains Base64 Image Data


if __name__ == "__main__":
    # Example usage:
    data_access = FiguyoDataAccess()

    # Create a new figure
    # new_figure = data_access.create_figure(
    #     name="Rei Ayanami Radio Eva Hobby Max Neuauflage",
    #     canonname="Rei Ayanami",
    #     herkunft="Neon Genesis Evangelion",
    #     erscheinungsdatum=datetime.date(2023, 5, 30),
    #     preis=199.90,
    #     gewicht=1000,
    #     photo="base64encodedstring"
    # )
    # print(f'Created Figure: {new_figure.name}')

    # # Retrieve all figures
    # all_figures = data_access.get_all_figures()
    # for figure in all_figures:
    #     print(f'Record: {figure.name}')
    
    # # Find a figure by name
    # found_figures = data_access.find_figure_by_name("Rei Ayanami Radio Eva Hobby Max Neuauflage")
    # for figure in found_figures:
    #     print(f'Found Figure: {figure.name}')


    for figure in data_access.get_all_figures():
        figure: FiguyoFigure
        print(f'Figure: {figure.name} - Release: {figure.erscheinungsdatum} - Price: {figure.preis}€')

