import tkinter as tk
from Othello_Controll import OthelloController as oc
from Mask import Mask
class GameWindow(tk.Frame):
    def __init__(self,master,w,h,**kwargs):
        super().__init__(master=master)
        canvas = tk.Canvas(self, width=w, height=h)
        mask=kwargs.get("mask",Mask.hexagon)
        col=kwargs.get("color",None)
        player=kwargs.get("player",["Player","Player"])
        endfunc=kwargs.get("endfunc",lambda: master.quit())
        self.oc = oc(canvas, mask,player=player,color=col, endfunc=endfunc)
        canvas.pack()
def main():
    h = 480
    w = 425
    root = tk.Tk()
    root.geometry(str(w) + "x" + str(h))

    gc=GameWindow(root,w=w,h=h)
    gc.pack()
    root.mainloop()

if __name__=="__main__":
    main()