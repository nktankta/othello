import time
class Player:
    def __init__(self,value,*args):
        self.value=value
        self.starttime=None
        self.x,self.y=None,None
    def clicked(self,x,y,value):
        if self.value==value:
            self.x,self.y=x,y
    def reset(self):
        self.x,self.y=None,None
    def resetTime(self):
        self.starttime=None
    def getValue(self,*args):
        if self.starttime is None:
            self.starttime=time.time()
        while self.x is None and time.time()-self.starttime<0:
            time.sleep(0.1)
        if self.x is not None:
            return self.x,self.y
        else:
            return None,None