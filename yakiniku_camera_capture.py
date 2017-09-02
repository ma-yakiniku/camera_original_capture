import cv2
import numpy as np
from PIL import Image
from yakiniku_service import YakinikuService
from judge import judge

service = YakinikuService("7nkse", "pRTV90grGe2zuOlMaAKy3AlabEDqLtgP3BlFP5GX", "ck8mlYWIBODtYXG05OpFW0oe616lZSKXXicgF3G0")

def find_rect_of_target_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 20) | (h > 200)) & (s > 128)] = 255
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=cv2.contourArea, reverse=True)
    rects = []
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    return rects[:4]

def capture_camera():
    #captuqqre = cv2.VideoCapture(1)

    flag = 0
    rects = []
    frame = cv2.imread("nama.jpg")
    i = 0
    while True:
        #_, frame = capture.read()
        service.original().push(Image.open("cap.jpg"))
        if flag == 0:
            rects = find_rect_of_target_color(frame)
            flag = 1
            #for rect in rects:
                #cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
            #print(rects)
            #cv2.imshow('red', frame)
        elif flag == 1:
            frame = cv2.imread("bake.jpg")
            j_image = judge(frame, rects)
            cv2.imshow("baked", j_image)
            #cv2.imshow('test', frame)
            cv2.imwrite("cap.jpg", frame)
            k = cv2.waitKey(10000)
            if k == 27:
                break
    #capture.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_camera()