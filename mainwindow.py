import tkinter as tk
from window_class import Cells
def main():
    root = tk.Tk()

    root.geometry("800x800")
    canvas = tk.Canvas(root, width=800, height=800)
    cells=Cells(canvas,30)

    canvas.pack()
    cells.create_boad(15,10)
    root.mainloop()

if __name__=="__main__":
    main()