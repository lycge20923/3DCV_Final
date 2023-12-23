'''
This is to 
1. (could neglect)Camera Calibration(with defined board, in ```CalibrationBoard.png```)
2. add the axis to the video having maruco marker 
'''

import argparse
import cv2 
import pickle
import os

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250) #Aruco有多種Dictionay，就當作是有不同的編碼方式
parameters = cv2.aruco.DetectorParameters_create()

# To do Camera Calibration
def CameraCalibration(CalVideo_pth):
    '''
    input:
        CalVideo_pth: The video of Camera Calibration
    output: 
        the pickle file with the 
    '''
    Calibration_board = cv2.aruco.CharucoBoard_create(7, 9, \
                                                  .0125, .01, dictionary) # create the calibration board
    
    Cap = cv2.VideoCapture(CalVideo_pth) #抓影片
    frameCount = int(Cap.get(cv2.CAP_PROP_FRAME_COUNT))
    all_corners, all_ids, counter = [], [], 0
    for i in range(frameCount):
        ret, frame = Cap.read() 
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # turn to gray-scale image
        res = cv2.aruco.detectMarkers(grayframe, dictionary) # check marker
        if len(res[0]) > 0:
            res2 = cv2.aruco.interpolateCornersCharuco(res[0], res[1], grayframe, Calibration_board)
            if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3 and counter % 3 == 0:
                all_corners.append(res2[1])
                all_ids.append(res2[2])
            cv2.aruco.drawDetectedMarkers(grayframe, res[0], res[1])
        cv2.imshow('frame', grayframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        counter += 1
    try:
        cal = cv2.aruco.calibrateCameraCharuco(all_corners, all_ids, Calibration_board, grayframe.shape, None, None)
    except:
        Cap.release()
        print("Calibration could not be done ...")
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cal
    with open(os.path.join('PickleFile','calibration.pckl'), 'wb') as f:
        pickle.dump((cameraMatrix, distCoeffs), f)
    f.close()

def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", dest="video_pth", \
                        help="Input Video path", type=str)
    parser.add_argument('--calvideo_path', dest='calvideo_path', \
                        help="Input Calibration path", type=str, default='')
    parser.add_argument('--output_path', dest='output_path',\
                        help="Output path", type=str, default='output.mp4')
    return parser

if __name__ == '__main__':
    args = Parser().parse_args()
    
    # get parameters 
    video_pth = args.video_pth
    calvideo_path = args.calvideo_path
    output_path = args.output_path

    # Get the Camera Matrix and distortion coefficients if necessary
    if (calvideo_path != ''):
        CameraCalibration(calvideo_path)
        with open(os.path.join('PickleFile','calibration.pckl'), 'rb') as f:
            cameraMatrix, distCoeffs = pickle.load(f)
    else:
        with open(os.path.join('PickleFile','defined_calibration.pckl'), 'rb') as f:
            cameraMatrix, distCoeffs = pickle.load(f)
    
    print(cameraMatrix)
    print(distCoeffs)

    capture = cv2.VideoCapture(video_pth)
    
    # prepare for write video
    fps = capture.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    outvideo = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        try:
            ret, frame = capture.read() # Capture each frame
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # turn to gray
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray_frame, dictionary, parameters=parameters) # detect markers
            frame = cv2.aruco.drawDetectedMarkers(image=frame, corners=corners, ids=ids, borderColor=(0, 255, 0)) # draw markers
            frame = cv2.aruco.drawDetectedMarkers(image=frame, corners=rejectedImgPoints, borderColor=(0, 0, 255)) # draw ban markers 
            if ids is not None:
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs) # rvecs, tvecs are the rotation and transition vectors, speratively 
                #########  draw the axis  ##########
                #for rvec, tvec in zip(rvecs, tvecs): # draw the axis 
                    #cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec, tvec, 1) # show the axises
                ####################################
            cv2.imshow('frame', frame)
            outvideo.write(frame)
        except:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    outvideo.release()