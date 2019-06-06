import numpy as np
import random


class Node:
    def __init__(self, board, player, putableFunc, winFunc):
        self.board = board
        self.player = player
        self.putable = putableFunc
        self.win = winFunc
        self.wins = 0
        self.n = 0
    def get_Putable(self, board, player):
        ls = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                ret = self.putable(board, j, i, player)
                if ret is not None:
                    ls.append(((j, i), ret))
        return ls
    def get_values(self):
        return (self.n, self.wins, self.player)


class Root(Node):
    UCT = lambda win, n, N: win / n + 1.4 * np.sqrt(np.log(N) / n)
    def add_child(self, ch):
        self.chldren.append(ch)
    def getResult(self, num):
        while self.n < num:
            nd = self.selectNode()
            nd.back()
        self.chldren[np.argmax([c.n for c in self.chldren])]
    def selectNode(self):
        return self.chldren[np.argmax([Node.UCT(win, n, self.N) for win, n, p in [c.get_value for c in self.chldren]])]


class Child(Node):
    def playout(self):
        board=self.board
        player=self.player
        played=[]
        while True:
            tup=self.get_Putable(board,player)
            try:
                rand=random.choice(tup)
            except:
                break
            board=rand[1]
            played.append(rand[0])
            player=player%2+1
        w=self.win(board)
        self.wins+=w
        self.n+=1
        return (1,w,player)