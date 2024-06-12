# Figuyo
Figuyo is a school project of mine. It is made for digitally storing and keeping track of Anime Figures.

# Quickstart
1: Download or Clone this Repository

2: Get requirements (pip install -r requirements.txt)

3: Run Figuyo.py

... OR Download Figuyo.exe and run it (inside of the zip at Releases)

# Known Limitations / Issues
- When loading a lot of Anime Figures into the [CTkTable](https://github.com/akascape/ctktable), it starts lagging around. Especially when resizing the Window. I have addressed the [Issue](https://github.com/Akascape/CTkTable/issues/74), but i'm still waiting for an answer.

- Customtkinter has an Issue when loading the Icons into Subwindows (Windows opened via ``ctk.CTkToplevel()``), so I had to delete some lines off of customtkinter's ``ctk_toplevel.py``, so when installing Figuyo via the Source Code and getting Customtkinter via pip, please delete or comment out lines 41-47 from ``ctk_toplevel.py``
  
