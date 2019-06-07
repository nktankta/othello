import time
class Player:
    def __init__(self,value,*args):
        self.value=value
        self.x,self.y=None,None
    def clicked(self,x,y,value):
        if self.value==value:
            self.x,self.y=x,y
    def reset(self):
        self.x,self.y=None,None
    def getValue(self,*args):
        while self.x is None:
            time.sleep(0.1)
        return self.x,self.y