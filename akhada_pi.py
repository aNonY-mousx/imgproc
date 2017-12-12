import numpy as np
import cv2
 
video_capture = cv2.VideoCapture(0)
#setting resolution to 160x120
video_capture.set(3, 160)
video_capture.set(4, 120)
 
while(True):
 
    # Capture the frames
    ret, frame = video_capture.read()
 
    # Crop the image
    crop_img = frame[60:120, 0:160]
    roi = frame #
    
    lower_red = np.array([0,70,50])
    upper_red = np.array([10,255,255])
    #Convert roi to HSV
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
  
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    #enemy
    enemy = cv2.inRange(roi_hsv, lower_red, upper_red)
    
    # Find the contours of the frame
    _,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
 
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
        
        print( "the boundary coordinates are ",cx,cy)
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
 
        if cx >= 120:
            print ("Turn Left!")
 
        if cx < 120 and cx > 50:
            print ("U r in the boundary")
 
        if cx <= 50:
            print ("Turn Right")
        
        if cy <=27 & cx>=75 & cx<=85:
            print("Turn Back")
    
    #find enemy contour
    _,contours2,_ = cv2.findContours(enemy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Find the biggest enemy contour (if detected)
    if len(contours2) > 0:
        c2 = max(contours2, key=cv2.contourArea)
        M2 = cv2.moments(c2)
        if M2['m00'] ==0:
            continue
        ex = int(M2['m10']/M2['m00'])
        ey = int(M2['m01']/M2['m00'])
 
        cv2.line(roi,(ex,0),(ex,720),(255,0,255),1)
        cv2.line(roi,(0,ey),(1280,ey),(255,0,255),1)
        
        print( "the enemy coordinates are ",ex,ey)
        cv2.drawContours(roi, contours, -1, (0,255,255), 1)
     
    #Display the resulting frame
    cv2.imshow('orig',frame)
    cv2.imshow('thresh',thresh)
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
