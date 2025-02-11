import cv2
import mediapipe as mp
import time


class handDetect:

    def __init__(self,mode=False,maxHands=2,complex=1,detectionCon=0.5,trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.complex = complex
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.complex,self.detectionCon,self.trackCon)
        self.mpDrw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:                
                    self.mpDrw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        
        return img


    def findPos(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)

                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])
                #if id ==0:
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,255), cv2.FILLED)
        return lmList
    
    def main():
        pT = 0
        cT = 0
        cap = cv2.VideoCapture(0)
        detector = handDetect()

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


if __name__ == "__main__":
    main()