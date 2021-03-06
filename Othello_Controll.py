from CellBase import Cells
from Funcs import BeforeFuncs as bef
from Funcs import PutableFuncs as put
from Funcs import WinnerFunc as win
import numpy as np
import random
from Player import Player
from MonteCarlo import NPC
import threading
class OthelloController:
    def __init__(self,canvas,mask,beforeFunc=bef.passing,putableFunc=put.simple_putable,winnerFunc=win.more,player=None,color=None,endfunc=None,updatefunc=lambda a:None ):
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
        self.passFunc=self.cells.printPass
        self.mask=mask-1
        self.before=beforeFunc
        self.putable=putableFunc
        self.winner=winnerFunc
        self.endfunc=endfunc
        self.updatefunc=updatefunc
        if color is not None:
            self.cells.setColor(color[0],color[1],color[2])
        if player is None:
            self.createPlayer(["Player","Player"])
        else:
            self.createPlayer(player)
        self.create()

    def createPlayer(self,ls):
        '''
        プレイヤーの作成
        :param ls: len=2で、PlayerまたはNPC
        '''
        self.p1=self.getPlayer(ls[0],1)
        self.p2=self.getPlayer(ls[1],2)
    def getPlayer(self,s,value):
        if s=="Player" or s=="default":
            return Player(value,self.putable,self.winner)
        else:
            return NPC(value,self.putable,self.winner)
    def create(self):
        '''
        盤面を作成するメソッド
        '''
        self.cells.create_boad(9,9)
        self.cells.apply_mask(self.mask)
        self.cells=self.before(self.cells)
        self.turn_number=0
        self.player=1
        def click(x,y):
            self.p1.clicked(x,y,self.player)
            self.p2.clicked(x,y,self.player)
        self.cells.set_func(click)
        self.isPassed=False
        for i,j,k in ((3,3,2),(4,3,1),(4,4,2),(5,3,2),(3,4,1),(5,4,1),(4,5,2)):
            self.cells.set_cell_value(i,j,k)
        self.printAvailable()

        threading.Thread(target=self.playing).start()

    def isPass(self):
        '''
        パスかどうかを返すメソッド
        :return: 置けない場合はTrue置ける場合はFalse
        '''
        for i in range(self.cells.y):
            for j in range(self.cells.x):
                if self.cells.get(j,i) != 0:
                    continue
                if self.putable(self.cells.getBoard(),j,i,self.player) is not None:
                    return False
        return True


    def end(self):
        '''
        終了時に呼ばれるメソッドで主に勝敗表示などに使う
        '''
        if self.endfunc is not None:
            self.endfunc(self.winner(self.cells.getBoard()))
        exit()
    def pass_(self):
        '''
        パスされた場合に呼ばれるメソッド
        '''
        self.player=self.player%2+1
        if self.isPass():
            self.end()
        else:
            if self.passFunc is not None:
                self.passFunc()
    def get_Putable(self):
        '''
        置ける場所全て返す関数
        :return: 設置できる場所
        '''
        board=self.cells.getBoard()
        ls = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] != 0:
                    continue
                ret = self.putable(board, j, i, self.player)
                if ret is not None:
                    ls.append((j, i))
        return ls
    def getCellNums(self):
        bd=self.cells.getBoard()
        n1=np.sum(np.where(bd==1,1,0))
        n2=np.sum(np.where(bd==2,1,0))
        return (n1,n2)
    def printAvailable(self):
        ls=self.get_Putable()
        for x,y in ls:
            self.cells.set_cell_value(x,y,4)
    def resetAvailable(self):
        self.cells.apply_mask(self.cells.getBoard())
    def playing(self):
        '''
        常時呼び出されるメソッド
        '''
        self.updatefunc(self.player, self.getCellNums())
        if self.player==1:
            x,y=self.p1.getValue(self.cells.getBoard(),self.turn_number)
        else:
            x,y=self.p2.getValue(self.cells.getBoard(),self.turn_number)
        if x is None:
            x,y=random.choice(self.get_Putable())
        c=self.putable(self.cells.getBoard(),x,y,self.player)
        if c is None:
            pass
        else:
            self.p1.resetTime()
            self.p2.resetTime()
            self.cells.apply_mask(c)
            self.turn_number+=1
            self.player=self.player%2+1
            if self.isPass():
                print("passed")
                self.pass_()
            self.resetAvailable()
            self.printAvailable()
        self.p1.reset()
        self.p2.reset()

        self.playing()
