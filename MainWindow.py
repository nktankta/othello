import tkinter as tk
import GameWindow as gw
import SettingWindow as sw

def main():
    h=600
    w=450
    bg="lawn green"
    root = tk.Tk()
    root.configure(bg=bg)
    root.title(u"設定")
    root.geometry(str(w)+"x"+str(h))
    def switchWindow(e):#実際の画面遷移、もしこれ以上画面作成するなら別でメソッド、クラス化
        fr=gw.GameWindow(root,w=w,h=h,player=e["player"],icon=e["icon"],bg=bg)
        fr.pack()
        root.title(u"Othello(仮)")
    fr=sw.SettingFrame(root,endfunc=switchWindow)
    fr.pack()
    root.mainloop()

if __name__=="__main__":
    main()