import numpy as np

class BeforeFuncs():
    '''
    事前に行いたい処理の関数
    '''
    @staticmethod
    def passing(cells):
        return cells


class PutableFuncs:
    '''
    設置可能かどうかを返す関数
    必ず(Boolean,Cells)の状態になるように返す
    '''
    @staticmethod
    def alwaysTrue(cells, x, y,turn):
        c=np.copy(cells)
        c[y][x]=turn
        return (True,c)


class TurnFuncs:
    '''
    次の人のターンを返す関数
    '''
    @staticmethod
    def nextPlayer(value,turnnum):
        return value%2+1

class WinnerFunc:
    '''
    勝者を確定する関数
    1が多い場合は1
    同数は0
    2の場合は-1
    '''
    @staticmethod
    def more(cells):
        c=0
        one=np.sum(cells==1)
        two=np.sum(cells==2)
        if one>two:
            c=1
        elif one<two:
            c=-1
        return c