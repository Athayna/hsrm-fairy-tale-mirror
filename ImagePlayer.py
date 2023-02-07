import tkinter as tk
from PIL import ImageTk, Image
import sys

class ImagePlayer:
    def __init__(self):
        self.window = tk.Tk()
        self.wWidth = self.window.winfo_screenwidth()
        self.wHeight = self.window.winfo_screenheight()
        self.imageDict = dict()
        self.image = Image.open("./cat.png")
        self.path = "./pictures/"
        self.imageToDisplay = ImageTk.PhotoImage(self.image)

    def fillDict(self) -> None:
        self.imageDict.update({"cat": "cat.png"})
        self.imageDict.update({"dog": "dog.jpg"})
        self.imageDict.update({"snow_white": "snow_white.png"})

    def start(self):
        self.fillDict()
        self.window.attributes("-fullscreen", True)
        self.setImage("cat")
        self.window.mainloop()

    def setImage(self, image):
        self.image = Image.open(f'{self.path}{self.imageDict.get(image)}')
        for img in self.window.winfo_children():
            img.destroy()
        self.imgToDisplay = ImageTk.PhotoImage(self.image)
        labelToAdd = tk.Label(image=self.imgToDisplay)
        labelToAdd.place(relx=0.5, rely=0.5, anchor="center")

    def resizeImage(self, image):
        iWidth, iHeight = image.size # (breite | höhe)
        if((self.wWidth / iHeight) < (self.wHeight / iHeight)):
            return image.resize(self.wWidth, (int(iHeight * (self.wWidth / iWidth))), Image.Resampling.LANCZOS)
        else:
            return image.resize((int(iWidth* (self.wHeight / iHeight)), self.wHeight), Image.Resampling.LANCZOS)