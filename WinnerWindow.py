import tkinter as tk
from PIL import ImageTk,Image
class WinnerFrame(tk.Frame):
    def __init__(self,master,width=400,height=400,image="./icon/1.png",bg="green",endfunc=None):
        super().__init__(master,bg=bg,width=width,height=height)
        self.images=[]
        self.endfunc=endfunc
        self.cv=tk.Canvas(self,width=width,height=height-30,bg=bg)
        self.cv.config(highlightbackground=bg)
        self.cv.create_image(width//2,height//2,image=self.loadImage("./WinImages/star.png",w=300,h=300))
        self.cv.create_image(width//2,height//2*0.7,image=self.loadImage(image,w=200,h=200))
        self.cv.create_text(width//2,height//2*1.5,text="WIN",font=("",80),fill="white")
        self.cv.pack()
        bt=tk.Button(self,text=u"スタートに戻る")
        bt.bind("<Button-1>", self.end)
        bt.pack(anchor="e")
    def end(self,e):
        if self.endfunc is not None:
            self.endfunc()
        self.destroy()


    def loadImage(self,image,w=50,h=50):
        img = Image.open(image)
        img.thumbnail((w, h))
        img1 = ImageTk.PhotoImage(img)
        self.images.append(img1)
        return img1


def main():
    '''
    ゲーム画面だけのテスト時
    :return:
    '''
    h = 480
    w = 425
    root = tk.Tk()
    root.geometry(str(w) + "x" + str(h))

    gc=WinnerFrame(root,image="./icon/1.png",width=w,height=h)
    gc.pack()
    root.mainloop()

if __name__=="__main__":
    main()