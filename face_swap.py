# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:12:13 2019

@author: Lenovo
"""

import dlib
import cv2
import numpy as np

def extract_nparray(array):
    n=None
    for i in array[0]:
        n=i
        return n

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

img1=cv2.imread('1.jpg')
gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
faces=detector(gray)
for face in faces:
    landmark=predictor(gray,face)
    landmark_pts1=[]
    for i in range(0,68):
        x=landmark.part(i).x
        y=landmark.part(i).y
        landmark_pts1.append((x,y))
        
    pts1=np.array(landmark_pts1,np.int32)
    convexhull=cv2.convexHull(pts1)
    rect=cv2.boundingRect(convexhull)
    subdiv=cv2.Subdiv2D(rect)
    subdiv.insert(landmark_pts1)
    triangle=subdiv.getTriangleList()
    triangle=np.array(triangle,np.int32)
    triangle_index=[]
    for t in triangle:
        pt1=(t[0],t[1])
        pt2=(t[2],t[3])
        pt3=(t[4],t[5])
        
        t_p1=np.where((pt1==pts1).all(axis=1))
        t_p1=extract_nparray(t_p1)
        
        t_p2=np.where((pt2==pts1).all(axis=1))
        t_p2=extract_nparray(t_p2)
        
        t_p3=np.where((pt3==pts1).all(axis=1))
        t_p3=extract_nparray(t_p3)
        
        if t_p1 is not None and t_p2 is not None and t_p3 is not None:
            triangle_index.append([t_p1,t_p2,t_p3])
#Image-2         
img2=cv2.imread('2.jpg')
gray2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
new_img=np.zeros_like(img2)
faces2=detector(gray2)
for face in faces2:
    landmark=predictor(gray2,face)
    landmark_pts2=[]
    for i in range(0,68):
        x=landmark.part(i).x
        y=landmark.part(i).y
        landmark_pts2.append((x,y))
        #cv2.circle(img2,(x,y),2,(0,255,0),-1)
    pts2=np.array(landmark_pts2,np.int32)
    convexhull2=cv2.convexHull(pts2)

 
for ind in triangle_index:
    p1=landmark_pts1[ind[0]]
    p2=landmark_pts1[ind[1]]
    p3=landmark_pts1[ind[2]]
    
    tri1=np.array([p1,p2,p3],np.int32)
    rect=cv2.boundingRect(tri1)
    x,y,w,h=rect
    crop_tri1=img1[y:y+h,x:x+w]
    mask_tri1=np.zeros((h,w),np.uint8)
    
    points1=np.array([[p1[0]-x,p1[1]-y],
                      [p2[0]-x,p2[1]-y],
                      [p3[0]-x,p3[1]-y]],np.int32)
    cv2.fillConvexPoly(mask_tri1,points1,255)
    tri1_img=cv2.bitwise_and(crop_tri1,crop_tri1,mask=mask_tri1)
    
    #cv2.line(img1,p1,p2,(0,0,255),1)
    #cv2.line(img1,p2,p3,(0,0,255),1)
    #cv2.line(img1,p3,p1,(0,0,255),1)
    
    #Image-2
    pt1=landmark_pts2[ind[0]]
    pt2=landmark_pts2[ind[1]]
    pt3=landmark_pts2[ind[2]]
    
    tri2=np.array([pt1,pt2,pt3],np.int32)
    rect=cv2.boundingRect(tri2)
    x,y,w,h=rect
    crop_tri2=img2[y:y+h,x:x+w]
    mask_tri2=np.zeros((h,w),np.uint8)
    
    points2=np.array([[pt1[0]-x,pt1[1]-y],
                      [pt2[0]-x,pt2[1]-y],
                      [pt3[0]-x,pt3[1]-y]],np.int32)
    cv2.fillConvexPoly(mask_tri2,points2,255)
    tri2_img=cv2.bitwise_and(crop_tri2,crop_tri2,mask=mask_tri2)
    
    #cv2.line(img2,pt1,pt2,(0,0,255),1)
    #cv2.line(img2,pt2,pt3,(0,0,255),1)
    #cv2.line(img2,pt3,pt1,(0,0,255),1)
    
    #Matrix
    points1=np.float32(points1)
    points2=np.float32(points2)
    M=cv2.getAffineTransform(points1,points2)
    #Warp
    warp=cv2.warpAffine(crop_tri1,M,(w,h))
    warp=cv2.bitwise_and(warp,warp,mask=mask_tri2)
    #New Image
    triangle_area=new_img[y:y+h,x:x+w]
    triangle_area_gray=cv2.cvtColor(triangle_area,cv2.COLOR_BGR2GRAY)
    _,thres=cv2.threshold(triangle_area_gray,1,255,cv2.THRESH_BINARY_INV)
    warp=cv2.bitwise_and(warp,warp,mask=thres)
    
    triangle_area=cv2.add(triangle_area,warp)
    new_img[y:y+h,x:x+w]=triangle_area
    
    
#Final
img2_new=np.zeros_like(gray2)
img2_noface=cv2.fillConvexPoly(img2_new,convexhull2,255)
img2_nohead=cv2.bitwise_not(img2_noface)

head_noface=cv2.bitwise_and(img2,img2,mask=img2_nohead)
swap_head=cv2.add(head_noface,new_img)
#Result

#seamless
x,y,w,h=cv2.boundingRect(convexhull2)
center=(int((x+x+w)/2),int((y+y+h)/2))
result=cv2.seamlessClone(swap_head,img2,img2_noface,center,cv2.NORMAL_CLONE)
        
        
cv2.imshow('Image1',swap_head)
cv2.imshow('Image2',img2)
cv2.imshow('crop',result)
cv2.imwrite('Swapped_face.jpg',result)
cv2.waitKey(0)
cv2.destroyAllWindows()