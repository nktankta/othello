import tkinter as tk

def make_square(canvas,x,y,length):
    id = canvas.create_polygon(x,y,x+length,y,x+length,y+length,x,y+length, fill="green", outline="black",tags=str(x)+"_"+str(y))
    return id

def get_hex_top(x,y,length):
    l=0.866
    return x,y,x+length,y,x+1.5*length,y-l*length,x+length,y-2*l*length,x,y-2*l*length,x-0.5*length,y-l*length
def make_hexagon(canvas,x,y,len):
    id = canvas.create_polygon(get_hex_top(x,y,len), fill="green", outline="black")
    return id

root=tk.Tk()

root.geometry("800x800")
canvas=tk.Canvas(root,width=800,height=800)

def call(x,y):
    return lambda event:print(x,y)

for i in range(10):
    for j in range(10):
        if i%2==0:
            id=make_hexagon(canvas, 30*i+100, 40*j*0.866+100, 20)
        else:
            id = make_hexagon(canvas, 30 * i+100, 40 * j * 0.866-0.866*20+100, 20)
        canvas.tag_bind(id,"<1>",call(i,j))
canvas.pack()
root.mainloop()