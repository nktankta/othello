import tkinter as tk
import numpy as np
from Mask import Mask
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

    def __init__(self,canvas,px,py,length,value=0,board="green"):
        '''
        初期化処理で六角形も作成する
        :param canvas:TK.Canvasオブジェクト
        :param px: 左上x座標
        :param py: 左上y座標
        :param length: 一辺の長さ
        '''
        self.canvas=canvas
        self.px=px
        self.py=py
        self.value=value
        self.cid=-1
        self.len=length
        self.clen=length*0.7
        self.create_hexagon(fill=board)

    def circle(self,color):
        '''
        円を指定した色で作成する
        :param color:円に塗りたい色
        '''
        if self.cid is -1:
            self.create_circle(fill=color)
        else:
            self.change_color(fill=color)

    def create_hexagon(self,fill="green",outline="black"):
        '''
        六角形を作成するメソッド
        :param fill: 塗る色
        :param outline: 外枠の色
        :return:
        '''
        self.id=self.canvas.create_polygon(CellBase.get_hex_top(self.px,self.py,self.len),fill=fill,outline=outline)

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
            self.id=-1
            self.delete_circle()
        else:
            pass

    def set_value(self,v,color1="white",color2="black"):
        '''
        指定した値をvalueに代入し再描画するメソッド
        :param v: valueに入れたい値
        '''
        self.value = v
        self.update(color1=color1,color2=color2)

    def update(self,color1,color2):
        '''
        valueに基づいて再描画するメソッド
        '''
        if self.id==-1 and self.value!=-1:
            self.create_hexagon()
        if self.value==0:
            self.delete_circle()
        elif self.value==1:
            self.circle(color1)
        elif self.value==2:
            self.circle(color2)
        elif self.value==-1:
            self.delete()
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
        self.func=lambda x,y:None
        self.setColor()

    def set_func(self,func):
        '''
        クリック時に実行する関数
        :param func: lamda x,y:process のような形
        '''
        self.func=func

    def clear_cells(self):
        '''
        Cellsの初期化
        '''
        if len(self.cells)==0:
            return
        else:
            for i in self.cells:
                for j in i:
                    i.delete()
        self.cells=[]

    def get(self,x,y):
        '''
        x,yのセルの情報を返すメソッド
        :param x: x位置
        :param y: y位置
        :return: x,y位置のCell.value
        '''
        return self.cells[x][y].value
    def setColor(self,board="green",cell1="white",cell2="black"):
        self.board_color=board if board!="default" else "green"
        self.cell1_color=cell1 if cell1!="default" else "white"
        self.cell2_color=cell2 if cell2!="default" else "black"
    def getBoard(self):
        '''
        ボード全体の状態を返すメソッド
        :return: np.array型で盤面の状態
        '''
        ls=[]
        for i in range(self.y):
            c=[]
            for j in range(self.x):
                c.append(self.get(j,i))
            ls.append(c)
        return np.array(ls)

    def getVirtualBoard(self):
        '''
        ボード全体の実際の状態を返すメソッド
        :return: np.array型で盤面の状態
        '''
        ls=[]
        for i in range(-1,self.y+1):
            c=[]
            for j in range(-1,self.x+1):
                c.append(self.get(j,i))
            ls.append(c)
        return np.array(ls)

    def clicked(self,x,y):
        '''
        あるセルが選択されたときに呼ばれるメソッド
        現在は駒の書き換えのみを行う
        :param x: 選択されたCellのx位置
        :param y: 選択されたCellのy位置
        '''
        self.func(x,y)

    def create_boad(self,x,y):
        '''
        盤面全体を作成するクラス
        :param x: 横の個数
        :param y: 縦の個数
        '''
        self.clear_cells()
        self.x=x
        self.y=y
        def l(x, y):
            return lambda e: self.clicked(x, y)
        for i in range(x+1):
            cs=[]
            for j in range(y+1):
                if i%2==0:
                    cell=CellBase(self.canvas,1.5*i*self.length+0.5*self.length,j*self.length*1.732,self.length,board=self.board_color)
                else:
                    cell = CellBase(self.canvas, 1.5 * i * self.length + 0.5*self.length, j * self.length*1.732+0.866*self.length, self.length,board=self.board_color)
                cs.append(cell)

                self.canvas.tag_bind(cell.id,"<1>",l(i,j))
            self.cells.append(cs)
        for i in range(x+1):
            self.set_cell_value(i,-1,-1)
        for i in range(y+1):
            self.set_cell_value(-1,i,-1)

    def set_cell_value(self,x,y,value):
        '''
        指定した位置のCellをvalueに変更する
        :param x: x位置
        :param y: y位置
        :param value: 設定したい値
        '''
        self.cells[x][y].set_value(value,color1=self.cell1_color,color2=self.cell2_color)

    def apply_mask(self,mask):
        '''
        マスクを適用して盤面を変更する
        :param mask: np.array型で適用したいマスク
        '''
        for i in range(mask.shape[1]):
            for j in range(mask.shape[0]):
                self.set_cell_value(i,j,mask[j][i])
