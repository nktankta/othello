import tkinter as tk
from Othello_Controll import OthelloController as oc
from Mask import Mask
def main():
    h=475
    w=425
    root = tk.Tk()
    root.geometry(str(w)+"x"+str(h))
    canvas = tk.Canvas(root, width=w, height=h)
    c=oc(canvas,Mask.hexagon)
    canvas.pack()
    root.mainloop()

if __name__=="__main__":
    main()