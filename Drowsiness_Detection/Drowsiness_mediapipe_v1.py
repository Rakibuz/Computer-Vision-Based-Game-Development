from xml.etree.ElementPath import find
import mediapipe as mp
import cv2
import time
import math
import winsound
 
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode = False)

cap = cv2.VideoCapture(0)
pTime = 0

#status marking for current state
frame_count = 0
min_frame = 9
min_tolerance = 1.8
status=''
 

def aspect_ratio(p1,p2,p3,p4,p5,p6):
    height, width,channel = img.shape  #chhannel is import without it show tpoo may values to unpack
            
    p1 = int(p1.x * width), int(p1.y * height)
    p2 = int(p2.x * width), int(p2.y * height)
    p3 = int(p3.x * width), int(p3.y * height)
    p4 = int(p4.x * width), int(p4.y * height)
    p5 = int(p5.x * width), int(p5.y * height)
    p6 = int(p6.x * width), int(p6.y * height)
    #print(p1[0])
    #print(p1[1])
    up=math.sqrt( ((p2[0]-p6[0])**2)+((p2[1]-p6[1])**2) )
    up_=math.sqrt( ((p3[0]-p5[0])**2)+((p3[1]-p5[1])**2) )
    left_right=math.sqrt( ((p1[0]-p4[0])**2)+((p1[1]-p4[1])**2) )

    numerator=up+up_
    denominator=2*left_right
    aspect_ratio=numerator/denominator
    #print(ratio)
    return aspect_ratio

facial_areas = {
    'Contours': mp_face_mesh.FACEMESH_CONTOURS
    , 'Lips': mp_face_mesh.FACEMESH_LIPS
    , 'Face_oval': mp_face_mesh.FACEMESH_FACE_OVAL
    , 'Left_eye': mp_face_mesh.FACEMESH_LEFT_EYE
    , 'Left_eye_brow': mp_face_mesh.FACEMESH_LEFT_EYEBROW
    , 'Right_eye': mp_face_mesh.FACEMESH_RIGHT_EYE
    , 'Right_eye_brow': mp_face_mesh.FACEMESH_RIGHT_EYEBROW
    , 'Tesselation': mp_face_mesh.FACEMESH_TESSELATION
}

def plot_landmark(img_, facial_area_obj,color):    
    for source_idx, target_idx in facial_area_obj:
        source = landmarks.landmark[source_idx]
        target = landmarks.landmark[target_idx]
 
        relative_source = (int(img.shape[1] * source.x), int(img.shape[0] * source.y))
        relative_target = (int(img.shape[1] * target.x), int(img.shape[0] * target.y))
 
        cv2.line(img, relative_source, relative_target, color, thickness = 1)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imgRGB)
    landmarks = results.multi_face_landmarks[0]
    

    for facial_area in facial_areas.keys():

        facial_area_obj_lips = facial_areas['Lips']
        plot_landmark(results, facial_area_obj_lips,(255,0,255))

        facial_area_obj_left_eye = facial_areas['Left_eye']
        plot_landmark(results, facial_area_obj_left_eye,(255,0,0))

        facial_area_obj_right_eye = facial_areas['Right_eye']
        plot_landmark(results, facial_area_obj_right_eye,(255,0,0))

        facial_area_obj_face_oval = facial_areas['Face_oval']
        plot_landmark(results, facial_area_obj_face_oval,(0,255,0))

        ratio_eye_left =  aspect_ratio(landmarks.landmark[33],landmarks.landmark[160], landmarks.landmark[158], landmarks.landmark[133], landmarks.landmark[153], landmarks.landmark[144])
        ratio_eye_right =  aspect_ratio(landmarks.landmark[362],landmarks.landmark[385], landmarks.landmark[387], landmarks.landmark[263], landmarks.landmark[373], landmarks.landmark[380])
        ratio_lips_ =  aspect_ratio(landmarks.landmark[61],landmarks.landmark[39], landmarks.landmark[269], landmarks.landmark[291], landmarks.landmark[405], landmarks.landmark[181])
        eye_ratio= ((ratio_eye_left + ratio_eye_right)/2.0)*10
        ratio_lips=ratio_lips_*10

        #print(eye_ratio)
        #print(ratio_lips*10)
        
    if eye_ratio <= min_tolerance:
            frame_count +=1
    else:
        frame_count = 0

            
    if ((frame_count > min_frame)or (ratio_lips>=5.6)):
        #Closing the eyes
        status='Drowsy'
        winsound.Beep(440, 500)
        color=(255,255,0)
    else:
        status='Active'
        color=(0,255,0)
              
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img,  f'{status}', (460, 70), cv2.FONT_HERSHEY_PLAIN, 3,color, 3)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break

cap.release()
cv2.destroyAllWindows()
