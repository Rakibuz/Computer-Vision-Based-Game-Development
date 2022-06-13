import numpy as np
import cv2
import pygame


width =1280
height = 720
  
cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)

scale=4
widthKeybord = 287*scale
heightKeybord = 72*scale

#initialWarpPoints = [[122, 272], [1192, 258], [136, 541], [1192, 516]]
initialWarpPoints = [[176, 218], [1244, 213], [182, 484], [1238, 479]]
pts1 = np.float32(initialWarpPoints)
pts2 = np.float32([[0, 0], [widthKeybord, 0], [0, heightKeybord], [widthKeybord, heightKeybord]])


# Bounding box of each key and the correct finger
keyLocations = {
    # First Row
    'q': [28, 0, 16, 15, 'left_pinky'],
    'w': [47, 0, 16, 15, 'left_ring'],
    'e': [67, 0, 16, 15, 'left_middle'],
    'r': [86, 0, 16, 15, 'left_index'],
    't': [105, 0, 16, 15, 'left_index'],
    'y': [124, 0, 16, 15, 'right_index'],
    'u': [143, 0, 16, 15, 'right_index'],
    'i': [162, 0, 16, 15, 'right_middle'],
    'o': [182, 0, 16, 15, 'right_ring'],
    'p': [201, 0, 16, 15, 'right_pinky'],
    # Second Row
    'a': [32, 19, 16, 15, 'left_pinky'],
    's': [52, 19, 16, 15, 'left_ring'],
    'd': [71, 19, 16, 15, 'left_middle'],
    'f': [90, 19, 16, 15, 'left_index'],
    'g': [109, 19, 16, 15, 'left_index'],
    'h': [129, 19, 16, 15, 'right_index'],
    'j': [148, 19, 16, 15, 'right_index'],
    'k': [167, 19, 16, 15, 'right_middle'],
    'l': [187, 19, 16, 15, 'right_ring'],
    # Third Row
    'z': [42, 37, 16, 16, 'left_pinky'],
    'x': [62, 37, 16, 16, 'left_ring'],
    'c': [81, 37, 16, 16, 'left_middle'],
    'v': [100, 37, 16, 16, 'left_index'],
    'b': [119, 37, 16, 16, 'left_index'],
    'n': [138, 37, 16, 16, 'right_index'],
    'm': [158, 37, 16, 16, 'right_index']
}

pygame.init()
# Create Window/Display
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ai Typing Tutor")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()


while(cap.isOpened()):
      
    while True:
          
        ret, img = cap.read()
        cv2.imwrite('sample.jpg',img)

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img, matrix, (widthKeybord, heightKeybord))
        #imgWarp = cv2.flip(imgWarp, 1)
        
        for point in initialWarpPoints:
            cv2.circle(img,point,5,(0,0,255),cv2.FILLED)
        
        
        # Draw the bounding bbox on the warp image
        for key, value in keyLocations.items():
            x, y, w, h = value[0] * scale, value[1] * scale, value[2] * scale, value[3] * scale
            cv2.rectangle(imgWarp, (x, y), (x + w, y + h), (255, 0, 255), 2)


        cv2.imshow('img', img)
        cv2.imshow('img warp', imgWarp)
        if cv2.waitKey(30) & 0xff == ord('q'):
            break
        

         # OpenCV  Display
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))


        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
                
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Alert ! Camera disconnected")