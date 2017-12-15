import cv2
import numpy as np

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(img,(x,y),100,(255,0,0),-1)
        print (x,y)
        mouseX,mouseY = x,y
# Create a black image, a window and bind the function to window
img = cv2.imread("result_1.jpg");
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',img)
    #print (mouseX,mouseY)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()