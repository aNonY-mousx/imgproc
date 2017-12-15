import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)
#setting resolution to 160x120
video_capture.set(3, 160)
video_capture.set(4, 120)
# enemy detection status
en_f = 0;
while(True):
 
    # Capture the frames
    ret, frame = video_capture.read()
 
    # declare ROI
    roi = frame #
    # region where enemy should lie..
    cv2.line(roi,(27,0),(27,120),(200,10,200))
    cv2.line(roi,(133,0),(133,120),(200,10,200))
    #setting the threshold of lower and upper red HSV values
    lower_red = np.array([0,70,50])
    upper_red = np.array([10,255,255])
    #Convert roi to HSV
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #enemy(thresholding ) 
    enemy = cv2.inRange(roi_hsv, lower_red, upper_red)
    #find enemy contour
    _,contours2,_ = cv2.findContours(enemy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Find the biggest enemy contour (if detected)
    if len(contours2) > 0:
        c2 = max(contours2, key=cv2.contourArea)
        # need to adjust ......
        if cv2.contourArea(c2)>100: # filtering false positives
            en_f = 1 # enemy status = found(1)
            M2 = cv2.moments(c2)
            if M2['m00'] ==0:
                continue
            ex = int(M2['m10']/M2['m00'])
            ey = int(M2['m01']/M2['m00'])
            
            if ex<27:
                print("left")
            elif ex > 133:
                print("right")
            else:
                print("forward")
            #only for debugging, ploting center of detected contour with two lines    
            cv2.line(roi,(ex,0),(ex,720),(255,0,255),1)
            cv2.line(roi,(0,ey),(1280,ey),(255,0,255),1)
        print (cv2.contourArea(c2))#debugging
        #print( "the enemy coordinates are ",ex,ey)
        cv2.drawContours(roi, contours2, -1, (0,255,255), 1)
     
    #Display the resulting frame
    cv2.imshow('orig',frame)
    cv2.imshow('frame',roi)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
