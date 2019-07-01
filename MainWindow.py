import tkinter as tk
import GameWindow as gw
import SettingWindow as sw
import WinnerWindow as ww
class RootController(tk.Tk):

    def __init__(self):
        super().__init__()
        self.h = 600
        self.w = 450
        self.bg = "sky blue"
        self.configure(bg=self.bg)
        self.geometry(str(self.w) + "x" + str(self.h)+"+400+20")
        self.createSetting()
        self.mainloop()

    def createSetting(self):
        fr = sw.SettingFrame(self, endfunc=self.createGame,bg=self.bg)
        fr.pack()
        self.title(u"設定")
    def createWin(self,img):
        fr = ww.WinnerFrame(self, width=self.w, height=self.h, image=img, bg=self.bg,endfunc=self.createSetting)
        fr.pack()
        self.title(u"リザルト")

    def createGame(self,e):  # 実際の画面遷移、もしこれ以上画面作成するなら別でメソッド、クラス化
        fr = gw.GameWindow(self, w=self.w, h=self.h, player=e["player"], icon=e["icon"],winfunc=e["winfunc"],mask=e["mask"], bg=self.bg,endfunc=self.createWin)
        fr.pack()
        self.title(u"オセろっかっけい")
def main():
    RootController()

if __name__=="__main__":
    main()