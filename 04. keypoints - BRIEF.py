# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
from os import listdir
from os.path import isfile, join

#задаём путь к файлам
pathIn  = "Image Registraion Feature-based/"             #откуда брать файлы
pathOut = "Image Registraion Feature-based Out/BRIEF + STAR/"   #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]         #сами картинки
if not os.path.exists(pathOut):    os.makedirs(pathOut)                 #создать путь, если ещё нет

#задаём эталон
ref = cv2.imread(join(pathIn, files[0]))
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

#PROCESS OF CONVERTION 
#обрабатываем картинки каждый раз разным количеством контрольных точек
k = 10                                                                  #Начальное количество точек
while k <= 100:                                                      #Конечное количество точек
    for i in range(1,len(files)):
        #задаём объект для обработки
        mov = cv2.imread(join(pathIn,files[i]))
        mov = cv2.cvtColor(mov, cv2.COLOR_RGB2GRAY)

        #поиск контрольных точек и дескрипторов - STAR + BRIEF
        star1 = cv2.xfeatures2d.StarDetector_create(k)                    #STAR
        star2 = cv2.xfeatures2d.StarDetector_create(k)                    #STAR
        brief1 = cv2.xfeatures2d.BriefDescriptorExtractor_create()        #BRIEF
        brief2 = cv2.xfeatures2d.BriefDescriptorExtractor_create()        #BRIEF
        kp1 = star1.detect(mov,None)
        kp2 = star2.detect(ref,None)
        kp1, des1 = brief1.compute(mov, kp1)
        kp2, des2 = brief2.compute(ref, kp2)

        #сопоставление точек - по дескрипторам
        matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        matches = matcher.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)

        #отсев плохих точек RANSAC
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)
        for j , match in enumerate(matches):
            points1[j, :] = kp1[match.queryIdx].pt
            points2[j, :] = kp2[match.trainIdx].pt
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        #преобразование - Perspective
        height, width = ref.shape
        out = cv2.warpPerspective(mov, h, (width, height)) 

        #сохранить картикну
        savePath = pathOut+"Test["+str(k)+"]/"
        if not os.path.exists(savePath):    os.makedirs(savePath)
        cv2.imwrite(savePath+files[i],out)

        #среднее СКО k-ой последовательности
        sko = np.sum((out.astype("float") - ref.astype("float")) ** 2) 
        sko /= float(ref.shape[0] * ref.shape[1])
        sko += sko
    sko = sko/50
    print ("[BRIEF] average standard deviation of the sequence from ", k, "points:", sko)
    sko = 0
    k += 10                                    #Шаг увеличения количества точек
#вывод примера на экран
img3 = cv2.drawMatches(mov, kp1, ref, kp2, matches[:20], None)
cv2.imshow("Keypoint matches BRIEF", img3)
cv2.imshow("Registered image BRIEF", out)
cv2.waitKey(0)