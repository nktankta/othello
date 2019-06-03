from CellBase import Cells
from Funcs import BeforeFuncs as bef
from Funcs import PutableFuncs as put
from Funcs import TurnFuncs as turn
from Funcs import WinnerFunc as win
import numpy as np

class OthelloController:
    def __init__(self,canvas,mask,beforeFunc=bef.passing,putableFunc=put.alwaysTrue,turnFunc=turn.nextPlayer,winnerFunc=win.more):
        '''
        初期化処理
        :param canvas:Tk.Canvasオブジェクト
        :param mask: 初期化時に掛けるマスク
        :param beforeFunc: 盤面作成時に行う関数
        :param putableFunc: 置けるかどうか判断する関数
        :param turnFunc: 次のターンのプレイヤーを返す関数
        :param winnerFunc: 勝者を確定する関数
        '''
        self.canvas=canvas
        self.cells=Cells(canvas,30)
        self.mask=mask-1
        self.before=beforeFunc
        self.putable=putableFunc
        self.turn=turnFunc
        self.winner=winnerFunc
        self.create()

    def create(self):
        '''
        盤面を作成するメソッド
        '''
        self.cells.create_boad(9,9)
        self.cells.apply_mask(self.mask)
        self.cells=self.before(self.cells)
        self.turn_number=0
        self.player=1
        self.cells.set_func(self.clicked)
        self.isPassed=False
        for i,j,k in ((3,3,2),(4,3,1),(5,3,2),(3,4,1),(5,4,1),(4,5,2)):
            self.cells.set_cell_value(i,j,k)

    def isPass(self):
        '''
        パスかどうかを返すメソッド
        :return: 置けない場合はTrue置ける場合はFalse
        '''
        for i in range(len(self.cells.cells)):
            for j in range(len(self.cells.cells[i])):
                if self.putable(self.cells.getBoard(),i,j,self.player) is not None:
                    return False
        return True


    def end(self):
        '''
        終了時に呼ばれるメソッドで主に勝敗表示などに使う
        '''
        pass

    def pass_(self):
        '''
        パスされた場合に呼ばれるメソッドで、
        :return:
        '''
        if self.isPassed:
            self.end()
        else:
            self.isPassed=True
            self.player=self.player%2+1

    def clicked(self,x,y):
        '''
        クリックされたときに呼び出されるメソッド
        :param x: x位置
        :param y: y位置
        :return:
        '''
        c=self.putable(self.cells.getBoard(),x,y,self.player)
        if c is None:
            pass
        else:
            self.cells.apply_mask(c)
            self.turn_number+=1
            self.player=self.turn(self.player,self.turn_number)
            if self.isPass():
                self.pass_()
