import tkinter as tk
from tkinter import ttk

class Selector(ttk.Combobox):
    def __init__(self, master, ls,var):
        super().__init__(master=master, values=ls)
        self.master = master
        self.bind('<<ComboboxSelected>>', self.show_selected)
        self.var = var

    def show_selected(self, event):
        if self.var is not None:
            self.var.set(self.get())
        print(self.get())

class SelectorWithText(tk.Frame):
    def __init__(self,master,text,ls,var):
        super().__init__(master=master)
        self.label=tk.Label(self,text=text)
        self.selector=Selector(self,ls,var)
        self.label.grid(column=0,row=0)
        self.selector.grid(column=1,row=0)

class ColorSelector(SelectorWithText):
    def __init__(self, frame,text,var=None):
        ls = ["default", "black", "white", "blue", "red", "green"]
        super().__init__(master=frame, ls=ls,text=text,var=var)
class CharacterSelector(SelectorWithText):
    def __init__(self,frame,text,var=None):
        ls=["Player","NPC"]
        super().__init__(master=frame, ls=ls,text=text,var=var)


def main():
    h=475
    w=425
    root = tk.Tk()
    root.geometry(str(w)+"x"+str(h))
    root.title(u"設定")

    var = tk.StringVar(master=root)
    ch1=CharacterSelector(root,"Character1")
    ch2=CharacterSelector(root,"Character2")
    ch1.grid(column=0,row=0)
    ch2.grid(column=1,row=0)
    p1=ColorSelector(root,"Player1")
    p1.grid(column=0,row=1)
    p2=ColorSelector(root,"Player2")
    p2.grid(column=1,row=1)

    root.mainloop()

if __name__=="__main__":
    main()