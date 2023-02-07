import tkinter as tk
from PIL import ImageTk, Image
import sys

window = tk.Tk()
window.attributes("-fullscreen", True)
wWidth = window.winfo_screenwidth()
wHeight = window.winfo_screenheight()

index = 0
image1 = Image.open("./snow_white.jpg")
image2 = Image.open("./cat.jpg")
image3 = Image.open("./dog.jpg")
image4 = Image.open("./fairytale.gif")


def resize_Image(image):
    global wHeight, wWidth
    iWidth, iHeight = image.size  # (breite | hoehe)
    if(wWidth/iHeight<wHeight/iHeight):
        return image.resize(wWidth,(int(iHeight * (wWidth/iWidth)) ), Image.Resampling.LANCZOS)
    else:
        return image.resize((int(iWidth* (wHeight/iHeight)), wHeight), Image.Resampling.LANCZOS)
        
image1 = resize_Image(image1)
image2 = resize_Image(image2)
image3 = resize_Image(image3)
images = [image1, image2, image3, image4]
imgToDisplay = ImageTk.PhotoImage(image1)

def add_Image():
    global imgToDisplay, window
    for image in window.winfo_children():
        image.destroy()
    imgToDisplay = get_PhotoImage()
    labelToAdd = tk.Label(image=imgToDisplay)

    labelToAdd.place(relx=0.5, rely=0.5, anchor="center")

def get_PhotoImage():
    global index, images
    return ImageTk.PhotoImage(images[index])

def handle_keypress(event):
    global index, images, window
    if(event.char == 'q'):
        window.destroy()
        sys.exit()
    index += 1
    index %= len(images)
    add_Image()
    print(event.char)

def main():
    print('hello')

    add_Image()

    window.bind("<Key>", handle_keypress)

    window.mainloop()



if __name__ == "__main__":
    main()
