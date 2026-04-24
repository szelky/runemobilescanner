import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    d = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # now we compute the width and height of image
    # by using Euclidean Distance which is
    # sqrt((x2-x1)**2 + (y2-y1)**2)
    # and np.linalg.norm is just doing this formula
    widthTop = np.linalg.norm(tr - tl)
    widthBottom = np.linalg.norm(br - bl)
    maxWidth = max(int(widthTop), int(widthBottom))

    heightLeft = np.linalg.norm(tl - bl)
    heightRight = np.linalg.norm(tr - br)
    maxHeight = max(int(heightLeft), int(heightRight))

    # now we can create our destination points
    dst = np.array(
        [[0, 0],
         [maxWidth - 1, 0],
         [maxWidth - 1, maxHeight - 1],
         [0, maxHeight - 1]],
         dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped
