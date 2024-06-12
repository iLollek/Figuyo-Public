import os
import sys
import sillyorm
from sillyorm.dbms import sqlite
import PopupView
import logging
import signal
from FiguyoDataAccess import FiguyoFigure
import customtkinter as ctk
from MainGUI import App

if getattr(sys, 'frozen', False):
    print(f'Running in Productive (PROD) Environment (.exe)')
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
    ENV = "PROD"
    logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(funcName)20s() - %(message)s', level=logging.DEBUG, force=True)
else:
    print(f'Running in Development (DEV) Environment (.py)')
    program_directory = os.path.dirname(os.path.abspath(__file__))
    ENV = "DEV"
    logging.basicConfig(stream=sys.stdout, format='%(name)s - %(levelname)s - %(funcName)20s() - %(message)s', level=logging.DEBUG, force=True)
os.chdir(program_directory)

def closing_protocol():
    """Closes Figuyo and executes some last saving lines of Code."""
    logging.info(f'Closing Figuyo')
    os.kill(os.getpid(), signal.SIGTERM) # This is the last line that gets executed.

def check_db_health():
    """Checks if the Database contains the SillyORM FiguyoFigure Table. Returns True if everything is alright, False otherwise."""
    try:
        # Create the environment
        env = sillyorm.Environment(
            sqlite.SQLiteConnection("Figuyo.db").cursor()
        )
        
        # Register the FiguyoFigure model in the environment
        env.register_model(FiguyoFigure)
        
        return True
    except Exception as e:
        # Log the exception if necessary
        logging.error(f"An error occurred: {e}")
        return False

def create_figuyo_db():
    # define a model, a model abstracts a table in the database
    class FiguyoFigure(sillyorm.model.Model):
        _name = "FiguyoFigure"  # database table name & name in environment

        # fields
        name = sillyorm.fields.String(length=255)
        canonname = sillyorm.fields.String(length=255)
        herkunft = sillyorm.fields.String(length=255)
        erscheinungsdatum = sillyorm.fields.Date()
        preis = sillyorm.fields.Float()
        gewicht = sillyorm.fields.Integer()
        photo = sillyorm.fields.Text() # Contains Base64 Image Data


    # Create the environment
    env = sillyorm.Environment(
        sqlite.SQLiteConnection("Figuyo.db").cursor()
    )

    # register the model in the environment
    env.register_model(FiguyoFigure)

def check_first_time_run():
    logging.info(f'Checking if Figuyo is being run for the first Time...')
    if os.path.isfile("Figuyo.db"):
        logging.info(f'Figuyo is not being run for the first time, Figuyo.db exists. Checking Figuyo.db...')
        if check_db_health():
            logging.info(f'Database verified!')
        else:
            logging.error(f'Figuyo.db Error!')
            PopupView.show_error_box(f'Figuyo | Critical Error', f'A Critical Error occoured: Your Figuyo Database is not set up correctly, it is likely corrupted.\nPlease delete Figuyo.db and restart Figuyo.')
            closing_protocol()
    else:
        logging.warn(f'Figuyo.db does not exist, creating...')
        create_figuyo_db()

def start_GUI():
    logging.info(f'Starting GUI...')
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
    logging.info(f'GUI Closed. Closing Figuya...')
    closing_protocol()

check_first_time_run()
start_GUI()