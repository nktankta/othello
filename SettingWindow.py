import tkinter as tk
from tkinter import ttk

class Selector(ttk.Combobox):
    def __init__(self, master, ls,var):
        super().__init__(master=master, values=ls)
        self.set(ls[0])
        self.master = master
        self.bind('<<ComboboxSelected>>', self.show_selected)
        self.var = var

    def show_selected(self, event):
        if self.var is not None:
            self.var.set(self.get())

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
class SettingFrame(tk.Frame):
    def __init__(self,master,endfunc=lambda e:print(None)):
        super().__init__(master=master)
        self.endfunc=endfunc
        self.vars=[]
        [self.vars.append(tk.StringVar(master=self,value="default")) for x in range(5) ]
        ch1 = CharacterSelector(self, "Character1",var=self.vars[0])
        ch2 = CharacterSelector(self, "Character2",var=self.vars[1])
        ch1.grid(column=0, row=0)
        ch2.grid(column=1, row=0)
        p1 = ColorSelector(self, "Player1",var=self.vars[2])
        p1.grid(column=0, row=1)
        p2 = ColorSelector(self, "Player2",var=self.vars[3])
        p2.grid(column=1, row=1)
        board = ColorSelector(self, "Board Color",var=self.vars[4])
        board.grid(column=0, row=2)
        bt=tk.Button(self,text="OK")
        bt.bind("<Button-1>",self.endCall)
        bt.grid(column=0,row=3)
    def endCall(self,event):
        self.endfunc(self.getValue())
        self.destroy()
    def getValue(self):
        ls= [x.get() for x in self.vars]
        dic={}
        dic["player"]=[ls[0],ls[1]]
        dic["color"]=[ls[4],ls[2],ls[3]]
        return dic

def main():
    h=475
    w=425
    root = tk.Tk()
    root.geometry(str(w)+"x"+str(h))
    root.title(u"設定")
    fr=SettingFrame(root)
    fr.pack()
    root.mainloop()

if __name__=="__main__":
    main()