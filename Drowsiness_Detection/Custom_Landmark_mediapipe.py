import mediapipe
import cv2
import time

mp_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode = True)

cap = cv2.VideoCapture(0)
pTime = 0

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
        plot_landmark(results, facial_area_obj_right_eye,(0,0,255))
     
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break
cv2.destroyAllWindows()
cap.release()