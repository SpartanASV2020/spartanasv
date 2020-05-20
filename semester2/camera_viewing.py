# accessing both cameras through pi 

 

import numpy as np 

import cv2 

 

cap = cv2.VideoCapture(2) 

cap1 = cv2.VideoCapture(0) 

fourcc = cv2.VideoWriter_fourcc(*'MJPG') 

 

 

while(True): 

    # Capture frame-by-frame 

    ret, frame = cap.read() 

    ret, frame1 = cap1.read() 

    cap.set(cv2.CAP_PROP_FOURCC, fourcc); 

 

    # Display the resulting frame 

    cv2.imshow('frame',frame) 

    cv2.imshow('frame',frame1) 

    if cv2.waitKey(1) & 0xFF == ord('q'): 

        break 

 

# When everything done, release the capture 

cap.release() 

cap1.release() 

cv2.destroyAllWindows() 