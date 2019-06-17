import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
class Selector(ttk.Combobox):
    '''
    コンポボックスで、デフォルト値と値変更時に変数変更を行う
    '''
    def __init__(self, master, ls,var,bg="white"):
        '''
        初期化処理
        :param master:上位のtk.Frame
        :param ls: 表示したい内容
        :param var: tk.StringVar型で自動的に更新される
        '''
        super().__init__(master=master, values=ls,width=7,font=("",10))
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

class CharacterSetting(tk.Frame):
    def __init__(self,master,text="None",var=None,fill="white",bg="white"):
        super().__init__(master=master,bg=bg)
        tk.Label(self,text=text,font=("",20),bg=bg).pack(side="left",padx=10)
        Selector(self,["Player","NPC"],var=var,bg=bg).pack(side="left",padx=10)
        self.img=Image.open("./icon/1.png")
        self.img.thumbnail((50,50))
        self.img1=ImageTk.PhotoImage(self.img)
        cv=tk.Canvas(master=self,width=100,height=50,bg=bg)
        cv.config(highlightbackground=bg)
        cv.create_image(0,0,image=self.img1,anchor=tk.NW)
        cv.create_oval(55,5,95,45,fill=fill)
        cv.pack(padx=10)
class Title(tk.Frame):
    def __init__(self,master,text,font=("",10),width=400,height=100,bg="white"):
        super().__init__(master)
        delta=3
        cv=tk.Canvas(self,width=width,height=height,bg=bg)
        cv.create_text(width//2+delta
                       ,height//2+delta
                       ,text=text
                       ,fill="black"
                       ,font=font
                       ,justify="center")
        cv.create_text(width // 2
                       , height // 2
                       , text=text
                       , fill="white"
                       , font=font
                       , justify="center")
        cv.config(highlightbackground=bg)
        cv.pack()




class SettingFrame(tk.Frame):
    def __init__(self,master,endfunc=lambda e:print(None)):
        '''
        設定画面（仮）の初期化処理
        :param master:上位Frame
        :param endfunc: 決定時に呼ばれる関数
        '''
        bg="lawn green"
        super().__init__(master=master,bg=bg)
        self.endfunc=endfunc
        self.vars=[]
        pad=10
        title=Title(self,text="タイトル（仮）",font=(u'ＭＳ ゴシック',40),bg=bg)
        title.pack(pady=pad)
        [self.vars.append(tk.StringVar(master=self,value="default")) for x in range(2) ]
        CharacterSetting(self,u"先攻",self.vars[0],fill="white",bg=bg).pack(pady=pad)
        CharacterSetting(self,u"後攻", self.vars[1],fill="black",bg=bg).pack(pady=pad)

        bt=tk.Button(self,text="スタート",fg="yellow",font=("",20))
        bt.bind("<Button-1>",self.endCall)
        bt.pack(pady=pad)
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