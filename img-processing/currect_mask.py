import cv2
import os
import numpy as np

ipath = "C:/Users/yubak/Desktop/2025/YoloTest/datasets/images/train/"
lpath = "C:/Users/yubak/Desktop/2025/YoloTest/datasets/labels/train/"
inamelist = os.listdir(ipath)
inamelist.sort()
lnamelist = os.listdir(lpath)
lnamelist.sort()
for iname,lname in zip(inamelist,lnamelist):
    print(iname,lname)
    # with open(lpath+lname,"r") as f:
    #     lines = f.readline()
    line = np.loadtxt(lpath+lname,dtype="float",delimiter=" ")
    img = cv2.imread(ipath+iname)
    h, w, _ = img.shape
    mask = np.zeros((h,w))
    x_top = int(line[1]*w)
    y_top = int(line[2]*h-h*line[4]//2)
    x_right = int(line[1]*w-line[3]*w//2)
    y_right = int(line[2]*h+h*line[4]//2)
    x_left = int(line[1]*w+line[3]*w//2)
    y_left = int(line[2]*h+h*line[4]//2)
    points = np.array(((x_top,y_top),(x_right,y_right),(x_left,y_left),))
    mask = cv2.fillConvexPoly(mask,points,(255,255,255))
    cv2.imwrite("./datasets/mask/"+iname,mask)
    cv2.imwrite("./datasets/raw/"+iname,img)