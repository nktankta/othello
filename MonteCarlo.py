import numpy as np
import random
import concurrent.futures as futures

class Node:
    '''
    RootとChildの親クラス
    '''
    def __init__(self, board, player, putableFunc, winFunc,*args):
        '''
        初期化処理
        :param board:ボードの現在の状態
        :param player: プレーヤー番号
        :param putableFunc: 置ける場所かどうか返す関数
        :param winFunc: 勝者を返す関数
        :param args: その他引数
        '''
        self.board = board
        self.player = player
        self.putable = putableFunc
        self.win = winFunc
        self.wins = 0
        self.n = 0
        self.args=args
    def get_Putable(self, board, player):
        '''
        置ける場所全て返す関数
        :param board: ボードの現在の状態
        :param player: プレイヤー番号
        :return: 設置できる場所とボードのリスト
        '''
        ls = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] != 0:
                    continue
                ret = self.putable(board, j, i, player)
                if ret is not None:
                    ls.append(((j, i), ret))
        return ls
    def random_putable(self,board,player):
        for i in random.sample(list(range(board.shape[0])),board.shape[0]):
            for j in random.sample(list(range(board.shape[1])),board.shape[1]):
                if board[i,j] != 0:
                    continue
                ret = self.putable(board, j, i, player)
                if ret is not None:
                    return((j, i), ret)
        return None

    def get_values(self):
        '''
        現在の状態を表す関数
        :return:
        '''
        return (self.n, self.wins, self.player)
    def next_player(self):
        '''
        次のプレイヤー番号を返す関数
        :return: 次のプレイヤー番号
        '''
        return self.player%2+1


class Root(Node):
    '''
    親ノードで、ここから子ノードを作成する
    '''
    def tree_search(self, num):
        '''
        通常のモンテカルロ木探索
        :param num: 試行回数
        :return: 設置する場所
        '''
        self.create_children()
        while self.n < num:
            nd = self.selectNode()
            w=nd.playout()
            self.n+=1
            self.wins+= w
        return self.children[np.argmax([c.n for c in self.children])].args[0]
    def old_tree_search(self,num):
        '''
        モンテカルロシミュレーションで、マルチプロセスなのでこっちのほうがよさげ
        :param num: 子ノード1つ当たりの試行回数
        :return: 置く場所
        '''
        self.create_children(isPassFirstPlayout=True)
        if len(self.children)==1:
            return self.children[0].args[0]
        log=[]
        with futures.ProcessPoolExecutor() as executor:
            for ch in self.children:
                log.append(executor.submit(ch.playout_num,num))
        res=[]
        for i in log:
            res.append(i.result())
        max_args=np.argmax(res)
        print(self.children[max_args].args[0])
        return self.children[max_args].args[0]
    def selectNode(self):
        '''
        もっともよい子ノードの選出（UCT）
        :return:
        '''
        return self.children[np.argmax([ch.get_UCT(self.n) for ch in self.children])]
    def create_children(self,isPassFirstPlayout=False):
        '''
        子ノードの作成
        :param isPassFirstPlayout:初期に子ノードの初期化を行うかどうか
        :return:
        '''
        boards=self.get_Putable(self.board,self.player)
        player=self.next_player()
        self.children=[Child(board,player,self.putable,self.win,xy) for xy,board in boards]
        if not isPassFirstPlayout:
            for ch in self.children:
                w=ch.playout()
                self.wins+= w
                self.n+=1

class Child(Node):
    '''
    子ノードでプレイアウトのみを提供する
    '''
    UCT = lambda win, n, N: win / n + 1.4 * np.sqrt(np.log(N) / n)
    def playout_num(self,num):
        '''
        プレイアウトを指定回数行いその結果を返すメソッド
        :param num:試行回数
        :return: 勝率
        '''
        for i in range(num):
            self.playout(isRandom=True)
        print(self.args[0],":",(self.n-self.wins)/self.n,"(",self.n-self.wins,"/",self.n,")")
        return (self.n-self.wins)/self.n

    def playout(self,isRandom=False):
        '''
        プレイアウトを行う関数
        :return: 勝敗
        '''
        isPassed=False
        board=self.board
        player=self.player
        played=[]
        while True:
            if not isRandom:
                tup=self.get_Putable(board,player)
                try:
                    rand=random.choice(tup)
                    isPassed=False
                except:
                    if isPassed:
                        break
                    else:
                        isPassed=True
                        continue
            else:
                tup=self.random_putable(board,player)
                if tup is not None:
                    rand=tup
                    isPassed=False
                else:
                    if isPassed:
                        break
                    else:
                        isPassed=True
                        continue
            board=rand[1]
            played.append(rand[0])
            player=player%2+1
        w=self.win(board)
        if w==self.player:
            wins=1
        elif w==self.next_player():
            wins=0
        else:
            wins=0.5
        self.wins+=wins
        self.n+=1
        return wins
    def get_UCT(self,N):
        '''
        自分のUCT値を計算する関数
        :param N: 全体試行回数
        :return: UCT値
        '''
        return Child.UCT(self.wins,self.n,N)

class NPC:
    def __init__(self,player,putableFunc,winFunc):
        '''
        Controllerに入れるプレイヤーとして使える
        :param player: プレイヤー番号
        :param putableFunc: 設置可能関数
        :param winFunc: 勝敗関数
        '''
        self.player=player
        self.put=putableFunc
        self.win=winFunc
    def reset(self):
        '''
        状態のリセット
        :return:
        '''
        self.root=None
    def getValue(self,board,turns):
        '''
        どの場所に設置するかを返すメソッド
        :param board: 現在の盤面の状態
        :param turns: 現在のターン数
        :return: 設置場所
        '''
        self.root=Root(board,self.player,self.put,self.win)
        return self.root.old_tree_search(min(30+turns*turns,300))
    def clicked(self,*args):
        pass
