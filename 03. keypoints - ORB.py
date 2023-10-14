import cv2
import os
import numpy as np
from os import listdir
from os.path import isfile, join

#задаём путь к файлам
pathIn  = "Image Registraion Feature-based/"             #откуда брать файлы
pathOut = "Image Registraion Feature-based Out/ORB/"         #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]         #сами картинки
if not os.path.exists(pathOut):    os.makedirs(pathOut)                 #создать путь, если ещё нет

#задаём эталон
ref = cv2.imread(join(pathIn, files[0]))
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

#PROCESS OF CONVERTION 
#обрабатываем картинки каждый раз разным количеством контрольных точек
k = 100                                                                  #Начальное количество точек
sko_arr = [None] * (len(files)-1)
sko = 0
while k <= 100000:                                                      #Конечное количество точек
    for i in range(1,len(files)):
        #задаём объект для обработки
        mov = cv2.imread(join(pathIn,files[i]))
        mov = cv2.cvtColor(mov, cv2.COLOR_RGB2GRAY)

        #поиск контрольных точек и дескрипторов - ORB
        orb = cv2.ORB_create(k)
        kp1, des1 = orb.detectAndCompute(mov, None)
        kp2, des2 = orb.detectAndCompute(ref, None)

        #сопоставление точек - по дескрипторам
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(des1, des2, None)
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
        sko_arr[i-1] = np.sum((out.astype("float") - ref.astype("float")) ** 2) 
        sko_arr[i-1] /= float(ref.shape[0] * ref.shape[1])
        sko += sko_arr[i-1]
    sko = sko/50
    print ("[ORB] среднее СКО последовательности от", k, "точек:", sko)
    sko = 0
    k *= 2                                    #Шаг увеличения количества точек
#вывод примера на экран
img3 = cv2.drawMatches(mov, kp1, ref, kp2, matches[:20], None)
#img3 = cv2.resize(img3, (700, 350))
#out = cv2.resize(out, (350, 350))
cv2.imshow("Keypoint matches ORB", img3)
cv2.imshow("Registered image ORB", out)
cv2.waitKey(0)