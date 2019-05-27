import tkinter as tk
class CellBase:
    @staticmethod
    def get_hex_top(x, y, length):
        l = 0.866
        return x, y, x + length, y, x + 1.5 * length, y +l * length, x + length, y + 2 * l * length, x, y + 2 * l * length, x - 0.5 * length, y + l * length

    def __init__(self,canvas,px,py,length):
        self.canvas=canvas
        self.px=px
        self.py=py
        self.id=canvas.create_polygon(CellBase.get_hex_top(px,py,length),fill="green",outline="black")
        self.value=0
        self.cid=-1
        self.len=length
        self.clen=length*0.7
    def circle(self,color):
        if self.cid is -1:
            self.create_circle(fill=color)
        else:
            self.change_color(fill=color)
    def create_circle(self,fill="white"):
        l=self.clen
        center=(self.px+0.5*self.len,self.py+0.886*self.len)
        self.cid=self.canvas.create_oval(center[0]-l,center[1]-l,center[0]+l,center[1]+l,fill=fill)
    def change_color(self,fill="black"):
        self.canvas.itemconfigure(self.cid,fill=fill)
    def delete_circle(self):
         if self.cid is not -1:
            self.canvas.delete(self.cid)
            self.cid=-1
    def delete(self):
        if self.id is not -1:
            self.canvas.delete(self.id)
            self.delete_circle()
        else:
            pass
    def set_value(self,v):
        self.value = v
        self.update()
    def update(self):
        if self.value==0:
            self.delete_circle()
        elif self.value==1:
            self.circle("white")
        elif self.value==2:
            self.circle("black")
        else:
            pass


class Cells():
    def __init__(self,canvas,length):
        self.canvas=canvas
        self.length=length
        self.cells=[]
    def clear_cells(self):
        self.cells=[]
    def clicked(self,x,y):
        self.cells[x][y].set_value((self.cells[x][y].value+1)%3)
    def create_boad(self,x,y):
        self.clear_cells()
        def l(x, y):
            return lambda e: self.clicked(x, y)
        for i in range(x):
            cs=[]
            for j in range(y):
                if i%2==0:
                    cell=CellBase(self.canvas,1.5*i*self.length+0.5*self.length,j*self.length*1.732,self.length)
                else:
                    cell = CellBase(self.canvas, 1.5 * i * self.length + 0.5*self.length, j * self.length*1.732+0.866*self.length, self.length)
                cs.append(cell)

                self.canvas.tag_bind(cell.id,"<1>",l(i,j))
            self.cells.append(cs)

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