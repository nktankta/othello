import tkinter as tk
from tkinter import ttk

class Selector(ttk.Combobox):
    '''
    コンポボックスで、デフォルト値と値変更時に変数変更を行う
    '''
    def __init__(self, master, ls,var):
        '''
        初期化処理
        :param master:上位のtk.Frame
        :param ls: 表示したい内容
        :param var: tk.StringVar型で自動的に更新される
        '''
        super().__init__(master=master, values=ls)
        self.set(ls[0])
        self.master = master
        self.bind('<<ComboboxSelected>>', self.show_selected)
        self.var = var

    def show_selected(self, event):
        '''
        値変更時に呼ばれるメソッド
        :param event: イベント
        '''
        if self.var is not None:
            self.var.set(self.get())

class SelectorWithText(tk.Frame):
    def __init__(self,master,text,ls,var):
        '''
        セレクターとラベルを一緒にしたもの
        :param master: 上位tk.Frame
        :param text: 表示したいテキスト
        :param ls: 表示したいリスト
        :param var: 更新する変数
        '''
        super().__init__(master=master)
        self.label=tk.Label(self,text=text)
        self.selector=Selector(self,ls,var)
        self.label.grid(column=0,row=0)
        self.selector.grid(column=1,row=0)

class ColorSelector(SelectorWithText):
    def __init__(self, frame,text,var=None):
        '''
        色の選択を可能にしたもの
        :param frame: 上位Frame
        :param text: 表示したい文字
        :param var: 変更したい変数
        '''
        ls = ["default","cyan", "black", "white", "blue", "red", "green","pink","gold","purple","sky blue","light grey"]
        super().__init__(master=frame, ls=ls,text=text,var=var)
class CharacterSelector(SelectorWithText):
    def __init__(self,frame,text,var=None):
        '''
        プレーヤーかNPCかの選択を可能にしたもの
        :param frame: 上位Frame
        :param text: 表示したい文字
        :param var: 変更したい変数
        '''
        ls=["Player","NPC"]
        super().__init__(master=frame, ls=ls,text=text,var=var)
class SettingFrame(tk.Frame):
    def __init__(self,master,endfunc=lambda e:print(None)):
        '''
        設定画面（仮）の初期化処理
        :param master:上位Frame
        :param endfunc: 決定時に呼ばれる関数
        '''
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
        '''
        終了時に呼ばれる関数
        :param event: event
        '''
        self.endfunc(self.getValue())
        self.destroy()
    def getValue(self):
        '''
        自分の変数を辞書型で返す
        :return:
        '''
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