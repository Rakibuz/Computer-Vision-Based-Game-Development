import numpy as np
import cv2

from utils import CFEVideoConf,image_resize

cap = cv2.VideoCapture(0)
save_path = 'saved-media/watermark.mp4v'
frames_per_seconds = 24
config = CFEVideoConf(cap, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type, frames_per_seconds, config.dims)

img_path = 'images/logo/cfe-coffee.png'
logo = cv2.imread(img_path, -1)
#cv2.imshow('watermark',logo)


watermark = image_resize(logo, height=50)
cv2.imshow('watermark',watermark)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()



    # print(frame[50,150])
    # start_cord_x=50
    # start_cord_y=150
    # color = (255,0,0)
    # stroke = 2
    # w=100
    # h=200
    # end_cord_x= start_cord_x+w
    # end_cord_y=start_cord_y+h
    # cv2.rectangle(frame, (start_cord_x,start_cord_y), (end_cord_x, end_cord_y), color, stroke)
    # print(frame[start_cord_x:end_cord_x,start_cord_y:end_cord_y])
    
    
    
    
    
    #out.write(frame)  #saving video frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
     break


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()