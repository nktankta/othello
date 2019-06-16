from CellBase import Cells
from Funcs import BeforeFuncs as bef
from Funcs import PutableFuncs as put
from Funcs import WinnerFunc as win
import numpy as np
from Player import Player
from MonteCarlo import NPC
import threading
class OthelloController:
    def __init__(self,canvas,mask,beforeFunc=bef.passing,putableFunc=put.simple_putable,winnerFunc=win.more,player=None,color=None,endfunc=None):
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
        self.winner=winnerFunc
        self.endfunc=endfunc
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

        print(self.winner(self.cells.getBoard()))
        if self.endfunc is not None:
            self.endfunc()
        exit()

    def pass_(self):
        '''
        パスされた場合に呼ばれるメソッド
        '''
        self.player=self.player%2+1
        if self.isPass():
            self.end()


    def playing(self):
        '''
        常時呼び出されるメソッド
        '''
        if self.player==1:
            x,y=self.p1.getValue(self.cells.getBoard(),self.turn_number)
        else:
            x,y=self.p2.getValue(self.cells.getBoard(),self.turn_number)
        c=self.putable(self.cells.getBoard(),x,y,self.player)
        if c is None:
            pass
        else:
            self.cells.apply_mask(c)
            self.turn_number+=1
            self.player=self.player%2+1
            if self.isPass():
                print("passed")
                self.pass_()
        self.p1.reset()
        self.p2.reset()
        self.playing()
