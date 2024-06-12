# > curl -i --socks4a 127.0.0.1:9050 http://c1c4d4pr1me5330i.onion/
# Server version: 2014 v3.0
# Web browsers are useless here. For all is sacred!

import customtkinter as ctk
import os
from PIL import Image, ImageTk
import webbrowser
from ResourceFetcher import ResourceFetcher

resource_fetcher = ResourceFetcher()

class FiguyoApp:
    def __init__(self, root):
        root.title("Figuyo | About")
        root.geometry("400x400")
        root.resizable(False, False)
        
        self.title_label = ctk.CTkLabel(root, text="Figuyo", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.sample_text1_label = ctk.CTkLabel(root, text="Figuyo is planned, developed and released by iLollek", font=("Arial", 16))
        self.sample_text1_label.pack(pady=10)
        
        self.sample_text2_label = ctk.CTkLabel(root, text="Database ORM used: sillyORM by theverygaming", font=("Arial", 16))
        self.sample_text2_label.pack(pady=10)
        
        button_image = ctk.CTkImage(Image.open(resource_fetcher.GetResource("twitter_logo.png")), size=(16, 16))
        self.twitter_button = ctk.CTkButton(master=root, text="@ilollek on Twitter", image=button_image, compound="left", command=self.open_twitter)
        self.twitter_button.pack(side="bottom", padx=10, pady=10)
        
        self.mywebsitebutton = ctk.CTkButton(root, text="About iLollek", command=self.open_ilollekwebsite)
        self.mywebsitebutton.pack(side="bottom", padx=10, pady=10)

        self.sillyorm_button = ctk.CTkButton(root, text="sillyORM on GitHub", command=self.open_sillyorm)
        self.sillyorm_button.pack(side="bottom", padx=10, pady=10)

        self.load_gif(resource_fetcher.GetResource('asuka.gif'), root)

    def load_gif(self, gif_path: str, root):
        # Load GIF image
        original_gif = Image.open(gif_path)
        original_gif_frames = []

        try:
            while True:
                original_gif_frames.append(original_gif.copy())
                original_gif.seek(len(original_gif_frames))  # Go to next frame
        except EOFError:
            pass

        # Resize GIF frames using Lanczos resampling
        self.gif_frames = [ctk.CTkImage(size=(40, 40), light_image=frame) for frame in original_gif_frames]

        # Show GIF on a label
        self.gif_label = ctk.CTkLabel(root, image=self.gif_frames[0], text=None)
        self.gif_label.pack()

        # Animation
        self.animate(0)

    def animate(self, frame):
        self.gif_label.configure(image=self.gif_frames[frame])
        self.gif_label.after(250, lambda: self.animate((frame + 1) % len(self.gif_frames)))

    def open_ilollekwebsite(self):
        webbrowser.open('https://ilollek.net/aboutme')

    def open_twitter(self):
        webbrowser.open('https://twitter.com/LoliTheGamer')

    def open_sillyorm(self):
        webbrowser.open('https://github.com/theverygaming/sillyORM')

if __name__ == "__main__":
    root = ctk.CTk()
    app = FiguyoApp(root)
    root.mainloop()
