from PIL import Image,ImageTk
import tkinter as tk
class ImageCanvas(tk.Canvas):
    def __init__(self,master,width,height,bg="green",image="./icon/1.png"):
        super().__init__(master,width=width,height=height,bg=bg)
        self.config(highlightbackground=bg)
        self.img = Image.open(image)
        self.img.thumbnail((50, 50))
        self.img1 = ImageTk.PhotoImage(self.img)
        self.create_image(0,0,image=self.img1,anchor=tk.NW)
    def changeIcon(self,image):
        self.delete("all")
        self.img = Image.open(image)
        self.img.thumbnail((50, 50))
        self.img1 = ImageTk.PhotoImage(self.img)
        self.create_image(0, 0, image=self.img1, anchor=tk.NW)
