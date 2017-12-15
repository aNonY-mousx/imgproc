import numpy as np
import cv2
 
video_capture = cv2.VideoCapture(0)
#setting resolution to 160x120
video_capture.set(3, 160)
video_capture.set(4, 120)
 
while(True):
    # Capture the frames
    ret, frame = video_capture.read()
    crop_img = frame[60:120, 0:160]
    
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
  
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    
    # Find the contours of the frame
    _,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    #_,contours,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] ==0:
            continue
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
 
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        
        leftmost = tuple(c[c[:,:,0].argmin()][0])
        rightmost = tuple(c[c[:,:,0].argmax()][0])
        topmost = tuple(c[c[:,:,1].argmin()][0])
        bottommost = tuple(c[c[:,:,1].argmax()][0])
        
        cv2.circle(crop_img,leftmost, 8, (0,0,255), -1)
        cv2.circle(crop_img,rightmost, 8, (0,0,255), -1)
        cv2.circle(crop_img,topmost, 8, (0,255,0), -1)
        cv2.circle(crop_img,bottommost, 8, (0,255,0), -1)
        
        x1,y1 = leftmost
        x2,y2 = rightmost
        horizontal= x2-x1
        
        '''_,y1= topmost
        _,y2= bottommost'''
        vertical= y2-y1
        print("horizontal",horizontal,"and vertical",vertical)
        if  horizontal>vertical:
            print("horizontal")
        else:
            print("vertical")
        #print( "the boundary coordinates are ",cx,cy)
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
 
        '''if cx >= 120:
            print ("Turn Left!")
 
        if cx < 120 and cx > 50:
            print ("U r in the boundary")
 
        if cx <= 50:
            print ("Turn Right")
        
        if cy <=27 & cx>=75 & cx<=85:
            print("Turn Back")'''
    #Display the resulting frame
    cv2.imshow('orig',frame)
    cv2.imshow('thresh',thresh)
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()