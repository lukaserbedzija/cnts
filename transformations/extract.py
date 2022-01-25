import numpy as np
import cv2 as cv


lower_hand_color = np.array([0, 48, 80], dtype=np.uint8)
upper_hand_color = np.array([20, 255, 255], dtype=np.uint8)


def extract_hand_frame_thresh(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hand_mask = cv.inRange(hsv, lower_hand_color, upper_hand_color)

    kernel = np.ones((3, 3), np.uint8)

    dilated_img = cv.dilate(hand_mask, kernel, iterations=3)
    eroded_img = cv.erode(dilated_img, kernel, iterations=3)
    blured_img = cv.GaussianBlur(eroded_img, (5, 5), 90)
    _, thresh_img = cv.threshold(blured_img, 0, 255, cv.THRESH_BINARY)

    return thresh_img


def extract_max_hand_frame(img):
    thresh_img = extract_hand_frame_thresh(img)

    contours, _ = cv.findContours(thresh_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        max_cnt = max(contours, key=lambda x: cv.contourArea(x))
        x, y, w, h = cv.boundingRect(max_cnt)

        return thresh_img[y:y+h, x:x+w]

    return None


