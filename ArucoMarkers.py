'''
This is the python to generate the aruco marker
```
python ArucoMarkers --number 2 # 2 is the number to generate 
```
'''

import cv2 
import argparse
import os

aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)

def GenerateMarker(id_):
    '''
    input: 
        id_: int, the aruco id
    output:
        aruco_marker: img, aruco marker 
    '''
    if(id_>=250):
        print('The ID is between 0~249')
        return None
    else:
        aruco_marker = cv2.aruco.drawMarker(dictionary=aruco_dictionary, \
                                            id=id_, sidePixels=600, borderBits=1)
        return aruco_marker

def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", dest="num", \
                        help="Number of ArucoMarker pictures to generate", type=int, default=1)
    return parser

if __name__ == '__main__':
    args = Parser().parse_args()
    num = args.num
    os.makedirs('ArucoMarkers',exist_ok=True)
    for i in range(0,num):
        img = GenerateMarker(i)
        cv2.imwrite(os.path.join('ArucoMarkers',"output_"+str(i)+".png"), img)



