import cv2
import imutils
import numpy as np

def find_document_contour(image, min_area_ratio=0.1):
    ratio = image.shape[0] / 500.0
    image_res = imutils.resize(image, height=500)
    
    gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    image_total_area = image_res.shape[0] * image_res.shape[1]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        area = cv2.contourArea(c)
        
        if len(approx) == 4 and area > (image_total_area * min_area_ratio):
            return approx, ratio
            
    return None, ratio

def get_best_scan(orig_image):
    # 1. Deneme: Orijinal
    screenCnt, ratio = find_document_contour(orig_image)
    target_img = orig_image
    
    # 2. Deneme: Padding (Kenarlar sıfırdaysa)
    if screenCnt is None:
        pad = 20
        padded = cv2.copyMakeBorder(orig_image, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        screenCnt, ratio = find_document_contour(padded)
        target_img = padded
        
    return screenCnt, ratio, target_img
