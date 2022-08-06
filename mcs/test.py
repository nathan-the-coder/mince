from graphics import *

def main():
    col_arr=["violet","indigo","blue","green","yellow","orange","red"]
    workArea = GraphWin('Rainbow Circle', 300, 300) # give title and dimensions
    x=workArea.getWidth()/2 # get x of middle of drawing area
    y=workArea.getHeight()/2 # get y of middle of drawing area

    i=0
    while i<len(col_arr):
        cir=Circle(Point(x, y), 10+10*i)# draw circle with center at middle of drawing area
        cir.setOutline(col_arr[i]) #get a next outline color from color array
        cir.setWidth(4)#set outline width
        cir.draw(workArea)#draw the current circle
        i+=1 # increment counter for iteration
        
    message = Text(Point(workArea.getWidth()/2, 250), 'Click to Exit')
    message.draw(workArea)
    workArea.getMouse()# get mouse to click on screen to exit
    workArea.close() # close the drawing window

main()

