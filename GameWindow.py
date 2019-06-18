import tkinter as tk
from Othello_Controll import OthelloController as oc
from Mask import Mask
from IconController import ImageCanvas
class NameCaller(tk.Frame):
    def __init__(self,master,icon,bg="green"):
        super().__init__(master,bg=bg)
        self.ic=ImageCanvas(self,width=50,height=50,image=icon,bg=bg)
        self.ic.pack(side="left")
        tk.Label(master=self,text=u"の番です！",bg=bg,font=("",20)).pack(side="left")
    def changeIcon(self,image):
        self.ic.changeIcon(image)
class CountCells(tk.Frame):
    def __init__(self,master,icons,bg="green"):
        super().__init__(master,bg=bg)
        self.template=u"の数は"
        self.var=[tk.StringVar(self,value=self.template+str(0)),tk.StringVar(self,value=self.template+str(0))]
        ImageCanvas(self,width=50,height=50,image=icons[0],bg=bg).pack(side="left")
        tk.Label(self,textvariable=self.var[0],font=("",20),bg=bg).pack(side="left")
        ImageCanvas(self, width=50, height=50, image=icons[1], bg=bg).pack(side="left")
        tk.Label(self, textvariable=self.var[1], font=("", 20),bg=bg).pack(side="left")
    def update(self,nums):
        v1,v2=nums
        self.var[0].set(self.template+str(v1))
        self.var[1].set(self.template + str(v2))
class GameWindow(tk.Frame):
    '''
    ゲームをtk.Frameとして作成することでレイアウトの簡易変更、画面遷移を容易にする
    '''
    def __init__(self,master,w,h,**kwargs):
        '''
        初期化処理だが独自部分のみの拡張
        :param master: 上位のFrame
        :param w: 横幅
        :param h: 縦幅
        :param kwargs:キーワード(mask：盤面の形,color：盤面、駒の色,player:PlayerかNPC,endfunc：終了時に呼ばれる関数)
        '''
        pady=3
        bg = kwargs.get("bg", "green")
        super().__init__(master=master,bg=bg)
        canvas = tk.Canvas(self, width=w, height=h-120,bg=bg)
        canvas.config(highlightbackground=bg)
        mask=kwargs.get("mask",Mask.hexagon)
        col=kwargs.get("color",None)
        player=kwargs.get("player",["Player","Player"])
        endfunc=kwargs.get("endfunc",lambda: master.quit())

        self.icon=kwargs.get("icon",["./icon/1.png","./icon/2.png"])
        self.nc=NameCaller(self,self.icon[0],bg=bg)
        self.nc.pack(pady=pady)
        canvas.pack(pady=pady)
        self.cc=CountCells(self,self.icon,bg=bg)
        self.cc.pack(pady=pady)
        def updateFunc(value,cells):
            self.nc.changeIcon(self.icon[value-1])
            self.cc.update(cells)
        self.oc = oc(canvas, mask, player=player, color=col, endfunc=endfunc, updatefunc=updateFunc)


def main():
    '''
    ゲーム画面だけのテスト時
    :return:
    '''
    h = 480
    w = 425
    root = tk.Tk()
    root.geometry(str(w) + "x" + str(h))

    gc=GameWindow(root,w=w,h=h)
    gc.pack()
    root.mainloop()

if __name__=="__main__":
    main()