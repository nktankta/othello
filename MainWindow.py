import tkinter as tk
import GameWindow as gw
import SettingWindow as sw

def main():
    h=475
    w=425
    root = tk.Tk()
    root.geometry(str(w)+"x"+str(h))
    def switchWindow(e):
        print(e)
        fr=gw.GameWindow(root,w=w,h=h,player=e["player"],color=e["color"])
        fr.pack()
    fr=sw.SettingFrame(root,endfunc=switchWindow)
    fr.pack()
    root.mainloop()

if __name__=="__main__":
    main()