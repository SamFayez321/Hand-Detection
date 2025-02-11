import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDrw = mp.solutions.drawing_utils

pT = 0
cT = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                #print(id,lm)

                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)

                #if id ==0:
                cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
            
            mpDrw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    

    imgf = cv2.flip(img,1)

    cT = time.time()
    fps = 1/(cT-pT)
    pT = cT

    cv2.putText(imgf, str(int(fps)), (10,100), cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255), 3)

    cv2.imshow('Image', imgf)
    cv2.waitKey(1)
    if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) <1:
        break
cv2.destroyAllWindows()