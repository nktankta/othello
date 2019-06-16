import tkinter as tk
from Othello_Controll import OthelloController as oc
from Mask import Mask
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
        super().__init__(master=master)
        canvas = tk.Canvas(self, width=w, height=h)
        mask=kwargs.get("mask",Mask.hexagon)
        col=kwargs.get("color",None)
        player=kwargs.get("player",["Player","Player"])
        endfunc=kwargs.get("endfunc",lambda: master.quit())
        self.oc = oc(canvas, mask,player=player,color=col, endfunc=endfunc)
        canvas.pack()
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