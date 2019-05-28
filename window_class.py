import tkinter as tk

class CellBase:
    '''
    Cellの描画のみを行うクラス
    六角形と駒となる円を作成できる
    '''
    @staticmethod
    def get_hex_top(x, y, length):
        '''
        六角形の頂点座標を返すメソッド
        :param x:左上のx座標
        :param y: 左上のy座標
        :param length: 一辺の長さ(px)
        :return: 頂点の座標
        '''
        l = 0.866
        return x, y, x + length, y, x + 1.5 * length, y +l * length, x + length, y + 2 * l * length, x, y + 2 * l * length, x - 0.5 * length, y + l * length

    def __init__(self,canvas,px,py,length):
        '''
        初期化処理で六角形も作成するメソッド
        :param canvas:TK.Canvasオブジェクト
        :param px: 左上x座標
        :param py: 左上y座標
        :param length: 一辺の長さ
        '''
        self.canvas=canvas
        self.px=px
        self.py=py
        self.id=canvas.create_polygon(CellBase.get_hex_top(px,py,length),fill="green",outline="black")
        self.value=0
        self.cid=-1
        self.len=length
        self.clen=length*0.7

    def circle(self,color):
        '''
        円を指定した色で作成する
        :param color:円に塗りたい色
        '''
        if self.cid is -1:
            self.create_circle(fill=color)
        else:
            self.change_color(fill=color)

    def create_circle(self,fill="white"):
        '''
        円を作成する
        :param fill:円に塗りたい色
        '''
        l=self.clen
        center=(self.px+0.5*self.len,self.py+0.886*self.len)
        self.cid=self.canvas.create_oval(center[0]-l,center[1]-l,center[0]+l,center[1]+l,fill=fill)

    def change_color(self,fill="black"):
        '''
        指定した色で円を塗りなおす
        :param fill:円の変える色
        '''
        self.canvas.itemconfigure(self.cid,fill=fill)

    def delete_circle(self):
        '''
        自身の円を削除する
        '''
        if  self.cid is not -1:
            self.canvas.delete(self.cid)
            self.cid=-1

    def delete(self):
        '''
        六角形を削除するメソッド
        '''
        if self.id is not -1:
            self.canvas.delete(self.id)
            self.delete_circle()
        else:
            pass

    def set_value(self,v):
        '''
        指定した値をvalueに代入し再描画するメソッド
        :param v: valueに入れたい値
        '''
        self.value = v
        self.update()

    def update(self):
        '''
        valueに基づいて再描画するメソッド
        '''
        if self.value==0:
            self.delete_circle()
        elif self.value==1:
            self.circle("white")
        elif self.value==2:
            self.circle("black")
        else:
            pass

class Cells():
    '''
    Cellの管理及び描画のコントロールを行うクラス
    指定したCellの色の変更などのAPIを提供する
    '''
    def __init__(self,canvas,length):
        '''
        初期化処理
        :param canvas:TK.Canvasオブジェクト
        :param length:一辺の長さ
        '''
        self.canvas=canvas
        self.length=length
        self.cells=[]

    def clear_cells(self):
        '''
        Cellsの初期化
        '''
        self.cells=[]

    def clicked(self,x,y):
        '''
        あるセルが選択されたときに呼ばれるメソッド
        現在は駒の書き換えのみを行う
        :param x: 選択されたCellのx位置
        :param y: 選択されたCellのy位置
        '''
        self.cells[x][y].set_value((self.cells[x][y].value+1)%3)

    def create_boad(self,x,y):
        '''
        盤面全体を作成するクラス
        :param x: 横の個数
        :param y: 縦の個数
        '''
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
    '''
    テスト用のメソッドで実際の操作はほかのクラスで行う
    '''
    root = tk.Tk()

    root.geometry("800x800")
    canvas = tk.Canvas(root, width=800, height=800)
    cells=Cells(canvas,30)

    canvas.pack()
    cells.create_boad(15,10)
    root.mainloop()

if __name__=="__main__":
    main()