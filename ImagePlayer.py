import tkinter as tk
from PIL import ImageTk, Image

class ImagePlayer:
    """ImagePlayer class that displays images in fullscreen mode."""

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.wWidth = self.window.winfo_screenwidth()
        self.wHeight = self.window.winfo_screenheight()
        self.imageDict = dict()
        self.image = Image.open("./pictures/cat.png")
        self.imageTxt = "cat"
        self.path = "./pictures/"
        self.imageToDisplay = ImageTk.PhotoImage(self.image)

    def fillDict(self) -> None:
        self.imageDict.update({"cat": "cat.png"})
        self.imageDict.update({"dog": "dog.jpg"})
        self.imageDict.update({"snow_white": "snow_white.png"})
        self.imageDict.update({"ende": "ende.jpg"})
        self.imageDict.update({"blaubarsch": "blaubarsch.jpg"})
        self.imageDict.update({"dornröschen": "dornröschen.png"})

    def start(self) -> None:
        self.fillDict()
        self.window.attributes("-fullscreen", True)
        self.setImage("cat")
        self.window.mainloop()

    def setImage(self, imageKey:str) -> None:
        print("change pic")
        print(self.imageDict.get(imageKey))
        self.imageTxt = imageKey
        self.image = Image.open(f'{self.path}{self.imageDict.get(imageKey)}')
        for img in self.window.winfo_children():
            img.destroy()
        self.imgToDisplay = ImageTk.PhotoImage(self.image)
        labelToAdd = tk.Label(image=self.imgToDisplay)
        labelToAdd.place(relx=0.5, rely=0.5, anchor="center")

    def resizeImage(self, image:Image) -> Image:
        iWidth, iHeight = image.size
        if((self.wWidth / iHeight) < (self.wHeight / iHeight)):
            return image.resize(self.wWidth, (int(iHeight * (self.wWidth / iWidth))), Image.Resampling.LANCZOS)
        else:
            return image.resize((int(iWidth* (self.wHeight / iHeight)), self.wHeight), Image.Resampling.LANCZOS)