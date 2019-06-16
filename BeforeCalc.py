import pickle
import os
global bef_calc_around
bef_calc_around=None
def get_around(x,y):
    '''
    事前計算の結果を返す処理
    :param x: x位置
    :param y: y位置
    :return: その位置でつながってるセルの位置
    '''
    global bef_calc_around
    if bef_calc_around is None:
        if not os.path.exists("./around.pkl"):
            calc_get_around()
        with open("./around.pkl","rb") as around:
            bef_calc_around=pickle.load(around)
    return bef_calc_around[x][y]
def calc_get_around():
    '''
    セル全体に_get_aroundを実行し結果を保存する
    :return:
    '''
    bef_calc=[]
    for i in range(9):
        ls=[]
        for j in range(9):
            ls.append(_get_around(i,j))
        bef_calc.append(ls)
    with open("./around.pkl","wb") as f:
        pickle.dump(bef_calc,f)
def _get_around(x,y):
    '''
    周囲のセルを求める
    :param x: x位置
    :param y: y位置
    :return: 辞書型の周囲座標
    '''
    dic={}
    dic["RU"] = get_line_cells_(x,y,"U","R")
    dic["RD"] = get_line_cells_(x,y,"D","R")
    dic["LU"] = get_line_cells_(x,y,"U","L")
    dic["LD"] = get_line_cells_(x,y,"D","L")
    dic["U"] = get_line_cells_(x,y,"U",None)
    dic["D"] = get_line_cells_(x,y,"D",None)
    return dic
def get_line_cells_(x,y,vertical,holizon):
    '''
    直線上のセルを返すメソッド
    :param x: x位置
    :param y: y位置
    :param vertical:上または下
    :param holizon: 右、左またはなし
    :return: それぞれの位置のtuple
    '''
    ls1=[]
    ls2=[]
    bx=x
    by=y
    while True:
        ax,ay=calc_cell_point(bx,by,vertical,holizon)
        if 0<=ay<9 and 0<=ax<9:
            ls1.append(ax)
            ls2.append(ay)
        else:
            break
        bx,by=ax,ay
    return (tuple(ls2),tuple(ls1))

def calc_cell_point(x,y,vertical,holizon):
    '''
    実際の隣接セルを返すメソッド
    :param x: x位置
    :param y: y位置
    :param vertical:上または下
    :param holizon: 右、左またはなし
    :return:セル位置
    '''
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