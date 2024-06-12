# Starry eyes tight as star-crossed lovers

from tkinter import Label, Entry, Button, messagebox
import tkinter as tk

def show_info_box(title, body):
    """Shows a tkinter Info box with a Info Icon."""
    # Create a Tkinter window (optional if you already have a Tkinter window created)
    window = tk.Tk()
    window.withdraw()  # Hide the window to only show the message box

    # Show the message box with the given title and body
    messagebox.showinfo(title, body)

    # Destroy the Tkinter window (optional if you already have a Tkinter window created)
    window.destroy()

def show_error_box(title, body):
    """Shows a tkinter Info box with a Error Icon."""
    # Create a Tkinter window (optional if you already have a Tkinter window created)
    window = tk.Tk()
    window.withdraw()  # Hide the window to only show the message box

    # Show the message box with the given title and body
    messagebox.showerror(title, body)

    # Destroy the Tkinter window (optional if you already have a Tkinter window created)
    window.destroy()

def show_warning_box(title, body):
    """Shows a tkinter Info box with a Warning Icon."""
    # Create a Tkinter window (optional if you already have a Tkinter window created)
    window = tk.Tk()
    window.withdraw()  # Hide the window to only show the message box

    # Show the message box with the given title and body
    messagebox.showwarning(title, body)

    # Destroy the Tkinter window (optional if you already have a Tkinter window created)
    window.destroy()

def question_box(title: str, message: str, icon='info'):
    """Shows a tkinter Question Box with a Yes & No Answer. Returns the Answer. Icon can be set; defaults to info icon."""
    # Create a root window for the message box
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show the message box and get the user's choice
    result = messagebox.askquestion(title, message, icon=icon, type=messagebox.YESNO, default=messagebox.YES)

    # Close the root window
    root.destroy()

    return result