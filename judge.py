import cv2
import numpy as np
from PIL import Image
from yakiniku_service import YakinikuService

service = YakinikuService("7nkse", "pRTV90grGe2zuOlMaAKy3AlabEDqLtgP3BlFP5GX", "ck8mlYWIBODtYXG05OpFW0oe616lZSKXXicgF3G0")

def judge(image, rects):
    img = image
    for rect in rects:
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        rect_img = img[y:y+height, x:x+width]
        cv2.imshow("rect", rect_img)

        hsv = cv2.cvtColor(rect_img, cv2.COLOR_BGR2HSV_FULL)
        lower_bake = np.array([0, 0, 0])
        upper_bake = np.array([190, 190, 180])
        img_mask = cv2.inRange(hsv, lower_bake, upper_bake)

        img_color = cv2.bitwise_and(rect_img, rect_img, mask=img_mask)

        imgray = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        
        #out_img = cv2.drawContours(img, contours, 0, (0,255,0), 3)


        ans = abs(x - width) * abs(y - height)
        #print(ans)
        area = cv2.contourArea(contours[0])
        #print(area)
        
        if(area >= ans / 2):
            cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 0, 0), thickness=2)
    cv2.imwrite("baked.jpg", img)
    service.marker().push(Image.open("baked.jpg"))
    return img