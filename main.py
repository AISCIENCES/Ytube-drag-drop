import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
centerPoint = [120, 100]
red = (0, 0, 255)
green = (0, 255, 0)
inside = False

radius, color, thickness = 60, red, 20

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandMarks = results.multi_hand_landmarks

    if multiLandMarks:
        handPoints = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idx, lm in enumerate(handLms.landmark):
                # print(idx,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handPoints.append((cx, cy))

        for point in handPoints:
            cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)

        firstFingerOpen = False
        secondFingerOpen = False

        if handPoints[8][1] < handPoints[6][1]:
            firstFingerOpen = True
        if handPoints[12][1] < handPoints[10][1]:
            secondFingerOpen = True

        # print()

        d = int(radius ** 2 - ((centerPoint[0] - handPoints[8][0]) ** 2 + (centerPoint[1] - handPoints[8][1]) ** 2))

        if d >= 0:
            inside = True
        else:
            inside = False


        if inside:
            if firstFingerOpen and secondFingerOpen:
                color = green
                centerPoint = handPoints[8]
        else:
            color = red

    cv2.circle(img, centerPoint, radius, color, thickness)

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)
