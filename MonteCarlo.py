import numpy as np
import random
import concurrent.futures as futures

class Node:
    def __init__(self, board, player, putableFunc, winFunc,*args):
        self.board = board
        self.player = player
        self.putable = putableFunc
        self.win = winFunc
        self.wins = 0
        self.n = 0
        self.args=args
    def get_Putable(self, board, player):
        ls = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] != 0:
                    continue
                ret = self.putable(board, j, i, player)
                if ret is not None:
                    ls.append(((j, i), ret))
        return ls
    def get_values(self):
        return (self.n, self.wins, self.player)
    def next_player(self):
        return self.player%2+1


class Root(Node):
    def tree_search(self, num):
        while self.n < num:
            nd = self.selectNode()
            w=nd.playout()
            self.n+=1
            self.wins+= w
        return self.children[np.argmax([c.n for c in self.children])].args[0]
    def old_tree_search(self,num):
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
        return self.children[np.argmax([ch.get_UCT(self.n) for ch in self.children])]
    def create_children(self,isPassFirstPlayout=False):
        boards=self.get_Putable(self.board,self.player)
        player=self.next_player()
        self.children=[Child(board,player,self.putable,self.win,xy) for xy,board in boards]
        if not isPassFirstPlayout:
            for ch in self.children:
                w=ch.playout()
                self.wins+= w
                self.n+=1

class Child(Node):
    UCT = lambda win, n, N: win / n + 1.4 * np.sqrt(np.log(N) / n)
    def playout_num(self,num):
        for i in range(num):
            self.playout()
        print(self.args[0],":",(self.n-self.wins)/self.n,"(",self.n-self.wins,"/",self.n,")")
        return (self.n-self.wins)/self.n

    def playout(self):
        isPassed=False
        board=self.board
        player=self.player
        played=[]
        while True:
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
        return Child.UCT(self.wins,self.n,N)

class NPC:
    def __init__(self,player,putableFunc,winFunc):
        self.player=player
        self.put=putableFunc
        self.win=winFunc
    def reset(self):
        self.root=None
    def getValue(self,board):
        self.root=Root(board,self.player,self.put,self.win)
        self.root.create_children(isPassFirstPlayout=True)
        return self.root.old_tree_search(50)
    def clicked(self,*args):
        pass
