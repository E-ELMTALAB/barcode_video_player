import cv2
from pyzbar.pyzbar import decode
import numpy as np
import box_finder as box_finder

red = (0 ,0 ,255 )
blue = (255 ,0 ,0)
green = (0 ,255 ,0 )
magenta = (255 ,0 ,255)


def read_barcode(image , draw=False ):
    
    points = None
    found = 0
    bar = None
    if decode(image):
        found = 1
        for barcode in decode(image):
            bar = barcode.data.decode("utf_8")
            if bar == "erfan":

            # print(barcode.data.decode("utf_8"))
                points = np.array([barcode.polygon] ,np.int32)
                points = points.reshape(4 , 2)
                points = box_finder.rearange_points(points)
                
                if draw:

                    cv2.circle(image , points[0] , 10 , red , -1)
                    cv2.circle(image , points[1] , 10 , blue , -1)
                    cv2.circle(image , points[2] , 10 , green , -1)
                    cv2.circle(image , points[3] , 10 , magenta , -1)
                    cv2.polylines(image , [points] , True , (0 , 255 ,0) , 5)

                print(points)
                
                
            else :
                points = np.array([barcode.polygon] ,np.int32)
                points = points.reshape(4 , 2)
                points = box_finder.rearange_points(points)

                if draw:

                    cv2.circle(image , points[0] , 10 , red , -1)
                    cv2.circle(image , points[1] , 10 , blue , -1)
                    cv2.circle(image , points[2] , 10 , green , -1)
                    cv2.circle(image , points[3] , 10 , magenta , -1)
                    cv2.polylines(image , [points] , True , (0 , 0,255) , 5)
                

    return points , found , bar , image 




# [[[ 79 254]] [[ 83 340]] [[171 335]] [[167 250]]]

# arr[i][0][0 , 1]