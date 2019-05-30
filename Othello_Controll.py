from window_class import Cells
from Funcs import BeforeFuncs as bef
from Funcs import PutableFuncs as put
from Funcs import TurnFuncs as turn
from Funcs import WinnerFunc as win

class OthelloController:
    def __init__(self,canvas,mask,beforeFunc=bef.passing,putableFunc=put.alwaysTrue,turnFunc=turn.nextPlayer,winnerFunc=win.more):
        self.canvas=canvas
        self.cells=Cells(canvas,30)
        self.mask=mask
        self.before=beforeFunc
        self.putable=putableFunc
        self.turn=turnFunc
        self.winner=winnerFunc

    def create(self):
        self.cells.create_boad(9,9)
        self.cells.apply_mask(self.mask)
        self.cells=self.before(self.cells)
        self.turn_number=0
        self.player=1
        self.cells.set_func(self.clicked)

    def end(self):
        pass

    def clicked(self,x,y):
        b,c=self.putable(self.cells.getBoard(),x,y,self.player)
        if not b:
            self.end()
        else:
            self.cells.apply_mask(c)
            self.turn_number+=1
            self.player=self.turn(self.player)

