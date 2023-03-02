import tkinter as tk
from PIL import ImageTk, Image, ImageFont, ImageDraw

class ImagePlayer:
    """ImagePlayer class that displays images in fullscreen mode."""

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.configure(bg='black')
        self.wWidth = self.window.winfo_screenwidth()
        self.wHeight = self.window.winfo_screenheight()
        self.imageDict = dict()
        self.image = Image.open("./pictures/face-smiling-white.png")
        self.imageTxt = "gesicht-lachen"
        self.path = "./pictures/"
        self.imageToDisplay = ImageTk.PhotoImage(self.image)

    def fillDict(self) -> None:
        self.imageDict.update({"gesicht-schlafen": "face-sleeping-white.png"})
        self.imageDict.update({"gesicht-lachen": "face-smiling-white.png"})
        self.imageDict.update({"gesicht-denken": "face-thinking-white.png"})
        self.imageDict.update({"cat": "cat.png"})
        self.imageDict.update({"dog": "dog.jpg"})
        self.imageDict.update({"snow_white": "snow_white.png"})
        self.imageDict.update({"ende": "ende.jpg"})
        self.imageDict.update({"blaubarsch": "blaubarsch.jpg"})
        self.imageDict.update({"kind": "baby.png"})
        self.imageDict.update({"baby-prinzessin": "babyPrinzessin.png"})
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
        self.imageDict.update({"schneeflocken": "schnee.png"})
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
        self.imageDict.update({"zahn": "zahn.png"})

    def start(self) -> None:
        self.fillDict()
        self.window.attributes("-fullscreen", True)
        self.setImage("gesicht-lachen")
        self.window.mainloop()

    def setImage(self, imageKey:str) -> None:
        print("change pic")
        self.imageTxt = imageKey
        imagePath = f'{self.path}{self.imageDict.get(imageKey)}'
        self.setImageWithPath(imagePath)
    
    def setImageWithPath(self, imagePath:str) -> None:
        self.image = Image.open(imagePath)
        for img in self.window.winfo_children():
            img.destroy()
        self.imgToDisplay = ImageTk.PhotoImage(self.resizeImage(self.image))
        labelToAdd = tk.Label(image=self.imgToDisplay, background="black")
        labelToAdd.place(relx=0.5, rely=0.5, anchor="center")
    
    def setTextImage(self, imageText:str) -> None:
        image = Image.open('plain.png')
        draw = ImageDraw.Draw(image)
        txt = imageText
        fontsize = 40  
        font = ImageFont.truetype("arial.ttf", fontsize)
        draw.text((200, 50), txt, font=font) 
        image.save('text.png')
        self.imageTxt = imageText
        self.setImageWithPath("text.png")

    def setTimeImage(self, imageName:str) -> None:
        self.imageTxt = imageName
        pathTime = f'./pictures/clock/uhr{imageName}.png'
        self.setImageWithPath(pathTime)

    def resizeImage(self, image:Image) -> Image:
        iWidth, iHeight = image.size
        if((self.wWidth / iHeight) < (self.wHeight / iHeight)):
            return image.resize((self.wWidth, (int(iHeight * (self.wWidth / iWidth)))), Image.Resampling.LANCZOS)
        else:
            return image.resize((int(iWidth* (self.wHeight / iHeight)), self.wHeight), Image.Resampling.LANCZOS)