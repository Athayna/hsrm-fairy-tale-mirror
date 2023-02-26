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
        self.imageDict.update({"kind": "baby.png"})
        self.imageDict.update({"??": "babyPrinzessin.png"})
        self.imageDict.update({"stiefkoenigin": "böseKönigin.png"})
        self.imageDict.update({"dreizehnte": "böseKönigin.png"})
        self.imageDict.update({"brunnen": "brunnen.png"})
        self.imageDict.update({"dornroeschen": "dornröschen.png"})
        self.imageDict.update({"dornenhecke": "dornen.png"})
        self.imageDict.update({"dornen": "dornen.png"})
        self.imageDict.update({"frau": "frau.png"})
        self.imageDict.update({"mutter": "frau.png"})
        self.imageDict.update({"frosch": "frosch.png"})
        self.imageDict.update({"großmutter": "großmutter.png"})
        self.imageDict.update({"hexe": "hexe.png"})
        self.imageDict.update({"kraemerin": "hexe.png"})
        self.imageDict.update({"alte-muetterchen": "hexe.png"})
        self.imageDict.update({"alte-frau": "hexe.png"})
        self.imageDict.update({"weibes": "hexe.png"})
        self.imageDict.update({"jaeger": "jäger.png"})
        self.imageDict.update({"koenig": "könig.png"})
        self.imageDict.update({"kugel": "kugel.png"})
        self.imageDict.update({"rapunzeln": "magische-blume.png"})
        self.imageDict.update({"mann": "mann.png"})
        self.imageDict.update({"pferd": "pferd.png"})
        self.imageDict.update({"prinz": "prinz.png"})
        self.imageDict.update({"koenigssohn": "prinz.png"})
        self.imageDict.update({"koenigstochter": "prinzessin.png"})
        self.imageDict.update({"prinzessin": "prinzessin.png"})
        self.imageDict.update({"rapunzel": "rapunzel.png"})
        self.imageDict.update({"rotkaeppchen": "rotkäppchen.png"})
        self.imageDict.update({"schlaf": "schlafen.png"})
        self.imageDict.update({"schloss": "schloss.png"})
        self.imageDict.update({"schneewittchen": "schneewittchen.png"})
        self.imageDict.update({"schnee": "schnee.png"})
        self.imageDict.update({"spindel": "spinnrad.png"})
        self.imageDict.update({"rapunzel": "rapunzel.png"})
        self.imageDict.update({"turm": "turm.png"})
        self.imageDict.update({"wald": "wald.png"})
        self.imageDict.update({"haeuschen": "waldhütte.png"})
        self.imageDict.update({"haube-tief-ins-gesicht": "wolf-verkleidet.png"})
        self.imageDict.update({"wolf": "wolf.png"})
        self.imageDict.update({"zauberin": "zauberin.png"})
        self.imageDict.update({"zwerge": "zwerg.png"})
        self.imageDict.update({"zwergen": "zwerg.png"})




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