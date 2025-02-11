import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


pT = 0
cT = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetect()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPos(img)

    if len(lmList) !=0:
        print(lmList[4])

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