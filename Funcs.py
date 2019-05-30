import numpy as np

class BeforeFuncs():
    @staticmethod
    def passing(cells):
        return cells


class PutableFuncs:
    @staticmethod
    def alwaysTrue(cells, x, y,turn):
        c=np.copy(cells)
        c[y][x]=turn
        return True,c


class TurnFuncs:
    @staticmethod
    def nextPlayer(value,turnnum):
        return value%2+1

class WinnerFunc:
    '''
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