import cv2
import math
import matplotlib.pyplot as plt


def fun(frame):
    #    size = frame.shape
    b, g, r = cv2.split(frame)
    ori = frame.copy()
    ret, thresh1 = cv2.threshold(b, 200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours
    cnt1 = []
    cnt2 = []
    lens = []
    box = []
    box1 = []
    for i in cnt:
        l = cv2.arcLength(i, True)
        if l > 100:
            cnt1.append(i)
    for i in cnt1:
        lens.append(cv2.arcLength(i, True))
    for i in range(len(lens)):
        if abs((lens[i] - min(lens))) < 50:
            cnt2.append(cnt1[i])
    for i in range(len(cnt2)):
        x, y, w, h = cv2.boundingRect(cnt2[i])
        box.append((x, y, w, h))
    if len(box) == 2 and abs(box[0][1] - box[1][1]) < 50:
        box1 = ((box[0][0], box[0][1]),
                (box[0][0] + box[0][2], box[0][1] + box[0][3]),
                (box[1][0] + box[1][2], box[1][1] + box[1][3]),
                (box[1][0], box[1][1]))
    if len(box1) == 4:
        res = cv2.line(ori, box1[0], box1[1], (0, 0, 255), 2)
        res = cv2.line(res, box1[1], box1[2], (0, 0, 255), 2)
        res = cv2.line(res, box1[2], box1[3], (0, 0, 255), 2)
        res = cv2.line(res, box1[3], box1[0], (0, 0, 255), 2)
        # res = cv2.rectangle(ori, box[1][0], box[0][1], (0, 0, 255), 2)
        return res
    # res = cv2.drawContours(ori, cnt2, -1, (0, 0, 255), 2)
    else:
        return ori


vc = cv2.VideoCapture('1234567.mp4')
if vc.isOpened():
    open, frame = vc.read()
else:
    open = False
while open:
    ret, frame = vc.read()
    if frame is None:
        break
    if ret == True:
        cv2.imshow('result', fun(frame))
        if cv2.waitKey(5) & 0xFF == 27:
            break
vc.release()
cv2.destroyWindow()
