'''
This helps to generate CharucoBoard, will save in ```CharucoBoard``` directory
'''

import cv2 
import argparse
import os 
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width',dest='width',help="the scale of square in one side", type=int, default=7)
    parser.add_argument('--height',dest='height',help="the scale of square in another side",type=int, default=9)
    parser.add_argument('--pixel_width',dest='pixel_width',help="the pixel of the board in another side", type=int, default=200)   
    parser.add_argument('--pixel_height',dest='pixel_height',help="the pixel of the board in one side", type=int, default=200)   
    parser.add_argument('--output_name',dest='output_name',help="the output file name", type=str, default='Board.png')  
    args = parser.parse_args()
    Calibration_board = cv2.aruco.CharucoBoard_create(args.width, args.height, \
                                                    .0125, .01, dictionary) # create the calibration board
    Cal_img = Calibration_board.draw((args.pixel_width*3, args.pixel_height*3))

    cv2.imwrite(os.path.join("CharucoBoard",args.output_name), Cal_img)