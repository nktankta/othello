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
    '''
    @staticmethod
    def alwaysTrue(cells, x, y,turn):
        c=np.copy(cells)
        c[y][x]=turn
        return c
    @staticmethod
    def NotPlaced(cells,x,y,turn):
        if cells[y][x]!=0:
            return None
        else:
            ret=np.copy(cells)
            ret[y][x]=turn
        return ret
    @staticmethod
    def alwaysFalse(cells,x,y,turn):
        return None


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
        '''
        数が多いほうが勝ち（2人用）
        :param cells: 置けなくなった盤面
        :return: 勝者がiの時はiを返す。それ以外の時は0を返す
        '''
        c=0
        one=np.sum(cells==1)
        two=np.sum(cells==2)
        if one>two:
            c=1
        elif one<two:
            c=2
        return c