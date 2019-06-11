import numpy as np
def get_around(board,x,y):
    dic={}
    up=y + y % 2
    down=y - 1 + y % 2
    dic["RU"] = get_line_cells(board,x,y,"U","R")
    dic["RD"] = get_line_cells(board,x,y,"D","R")
    dic["LU"] = get_line_cells(board,x,y,"U","L")
    dic["LD"] = get_line_cells(board,x,y,"D","L")
    dic["U"] = get_line_cells(board,x,y,"U",None)
    dic["D"] = get_line_cells(board,x,y,"D",None)
    return dic
def update_board(board,x,y,player):
    dic=get_around(board,x,y)
    bef=board
    aft=board
    for i in dic.values():
        aft=isPutable(i,bef,player)
        if aft is  not None:
            bef=aft
    return bef
def get_line_cells(board,x,y,vertical,holizon):
    ls=[]
    bx=x
    by=y
    while True:
        ax,ay=calc_cell_point(bx,by,vertical,holizon)
        if 0<=ay<board.shape[0] and 0<=ax<board.shape[1]:
            ls.append((ax,ay))
        else:
            break
        bx,by=ax,ay
    return ls
def calc_cell_point(x,y,vertical,holizon):
    if holizon==None:
        if vertical=="U":
            return (x,y-1)
        else:
            return (x,y+1)
    if holizon=="R":
        rx=x+1
    else:
        rx=x-1
    if vertical=="U":
        ry=y - 1 + (x % 2)
    else:
        ry= y + (x%2)
    return (rx,ry)
def isPutable(ls,board,player):
    include_otherPlayer=False
    ret=np.copy(board)
    if len(ls)==0:
        return None
    for x,y in ls:
        if board[y][x]==player%2+1:
            include_otherPlayer=True
            ret[y][x]=player
            continue
        if not include_otherPlayer:
            return None
        else:
            if board[y][x]==player:
                return ret
            break
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
    def simple_putable(cells,x,y,turn):
        if cells[y][x]!=0:
            return None
        ret=update_board(cells,x,y,turn)
        if np.allclose(ret,cells):
            return None
        ret[y][x]=turn
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