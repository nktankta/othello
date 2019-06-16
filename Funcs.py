import numpy as np
from BeforeCalc import get_around
def update_board(board,x,y,player):
    '''
    ボードの更新を行う（設置処理）
    :param board: ボードの更新前状態
    :param x: x位置
    :param y: y位置
    :param player: プレーヤー番号
    :return: 更新後
    '''
    dic=get_around(x,y)
    bef=board
    aft=board
    for i in dic.values():
        aft=isPutable(i,bef,player)
        if aft is  not None:
            bef=aft
    return bef

def isPutable(ls,board,player):
    '''
    実際におけるかどうかを判断するメソッド
    :param ls:対称の配列を抜き出すリスト
    :param board: ボードの状態
    :param player: プレーヤー番号
    :return: 設置できれば盤面、できなければNone
    '''
    include_otherPlayer=False
    if len(ls[0])==0:
        return None
    arr=board[ls]
    for i,a in enumerate(arr):
        if a==player%2+1:
            include_otherPlayer=True
            arr[i]=player
            continue
        if not include_otherPlayer:
            return None
        else:
            if arr[i]==player:
                ret=np.copy(board)
                ret[ls]=arr
                return ret
            return None
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
    def simple_putable(cells,x,y,player):
        '''
        通常のオセロと同じ
        :param cells: 現在のセル
        :param x: ｘ位置
        :param y: ｙ位置
        :param player: プレーヤー番号
        :return: 設置できればボードの状態、できなければNone
        '''
        if cells[y,x]!=0:
            return None
        ret=update_board(cells,x,y,player)
        if np.allclose(ret,cells):
            return None
        ret[y,x]=player
        return ret


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