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
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)
#cv2.imshow('watermark',watermark)
#print(watermark.shape)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
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
    
    frame_h, frame_w, frame_c = frame.shape
    #print(frame.shape)
    # gray=cv2.cvtColor(frame.copy(),cv2.COLOR_BGR2GRAY)
    # print(gray.shape)


    # overlay with 4 channels BGR and Alpha
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    #overlay[100:250,100:125]=(255,0,0,1)  #  overlay[y:x]      B,G,R,A
    #overlay[100:250,150:225]=(0,250,0,1)  #  overlay[y:x]      B,G,R,A
    #overlay[start_y:end_y,start_x:end_x]=(0,250,0,1)   B,G,R,A
    #cv2.imshow("overlay",overlay)

    watermark_h, watermark_w, watermark_c = watermark.shape
     # replace overlay pixels with watermark pixel values
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i,j][3] != 0:
                overlay[100+i,150+j]=watermark[i,j]
               
 
    cv2.addWeighted(overlay, 0.25, frame, 1.0, 0, frame)
    
    
    
    #out.write(frame)  #saving video frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
     break


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()