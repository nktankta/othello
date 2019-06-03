import tkinter as tk
from Othello_Controll import OthelloController as oc
from mask import Mask
def main():
    root = tk.Tk()

    root.geometry("500x500")
    canvas = tk.Canvas(root, width=800, height=800)
    c=oc(canvas,Mask.hexagon*Mask.random)
    canvas.pack()
    root.mainloop()

if __name__=="__main__":
    main()