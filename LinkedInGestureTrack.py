import cv2
import time
import HandTrackingModule as htm
import webbrowser as wb
import psutil
import pygetwindow as gw
from pywinauto import Application

# Camera size
wCam,hCam = 1280,720

# Linkedin URL and flag
url = "https://www.linkedin.com/in/samerfayez/"
li_flag = 0

# Previous and current time
pT = 0
cT = 0

# Initialize hand detection opencv and mediapipe
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetect(detectionCon=0.7)

# Check if chrome is already running
def is_chrome_open():
    return any("chrome.exe" in p.name().lower() for p in psutil.process_iter())

# Bring chrome to the foreground
def bring_chrome_front():
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if "Chrome" in window.title:
            if window.isMinimized:
                print("Restoring Chrome window...")
                window.restore()  # Restore the window if it's minimized
                time.sleep(1)
            if not window.isActive:
                print("Bringing Chrome to front...")
                window.activate()  # Activate window
                time.sleep(1)  # Small delay to ensure activation
                return True
            else:
                print("Chrome is already the active window.")
                return True
    print("Chrome window not found.")
    return False

# Open Linkedin
def open_lin():
    if is_chrome_open():
        if bring_chrome_front():
            app = Application(backend='uia')
            app.connect(title_re=".*Chrome.*")
            element_name="Address and search bar"
            dlg = app.top_window()
            urlo = dlg.child_window(title=element_name, control_type="Edit").get_value()
            #print(urlo)
            if urlo != "linkedin.com/in/samerfayez/":
                wb.open(url)
    else:
        print("Chrome is not running. Opening a new instance...")
        wb.open(url)


while True:
    success, img = cap.read()

    # Run hand detector module
    img = detector.findHands(img)

    # Get hand point positions
    lmList = detector.findPos(img, draw=False)

    # If a hand is detected
    if len(lmList) !=0:
        
        x0,y0 = lmList[0][1],lmList[0][2]
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        x3,y3 = lmList[12][1],lmList[12][2]
        x4,y4 = lmList[16][1],lmList[16][2]
        x5,y5 = lmList[20][1],lmList[20][2]


        # Distances
        lineCt = ((x0-x1)**2 + (y0-y1)**2)**0.5 # Center to thumb
        lineCf = ((x0-x2)**2 + (y0-y2)**2)**0.5 # Center to first finger
        lineTf = ((x1-x2)**2 + (y1-y2)**2)**0.5 # Thumb to first finger
        lineCf2 = ((x0-x3)**2 + (y0-y3)**2)**0.5 # Center to second finger
        lineCf3 = ((x0-x4)**2 + (y0-y4)**2)**0.5 # Center to third finger
        lineCf4 = ((x0-x5)**2 + (y0-y5)**2)**0.5 # Center to fourth finger

        # Print distances
        print ('Center to thumb:',int(lineCt),'Center to first finger:',int(lineCf),'Thumb to first finger:',int(lineTf),
               'Center to second finger:',int(lineCf2), 'Center to third finger:',int(lineCf3), 'Center to fourth finger:',int(lineCf4))

        # Check for "L" gesture
        if (0.6< (lineCt/lineCf) <0.763) and (lineCf2/lineCt)<0.5 and (lineCf3/lineCt)<0.5 and (lineCf4/lineCt)<0.5:
            li_flag+=1 # Increment flag
        else:
            li_flag = 0 # Reset flag if gesture not maintained

        # Check for maintained "L"
        if li_flag == 20:
            open_lin()
            li_flag = 0 # Reset flag


    # Count time
    cT = time.time()
    fps = 1/(cT-pT)
    pT = cT

    # Flip image for mirror effect
    imgf = cv2.flip(img,1)

    # Display FPS
    cv2.putText(imgf, f'FPS:{int(fps)}', (10,50), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), 3)

    # Display camera
    cv2.imshow('Image', imgf)
    cv2.waitKey(1)

    # End if camera closed
    if cv2.getWindowProperty('Image', 0) <0:
        break
cv2.destroyAllWindows()