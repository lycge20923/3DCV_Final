from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np
from objloader import *
from imutils.video import VideoStream
import cv2.aruco as aruco
# import yaml
import pickle
import imutils
import os

"""
This is file loads and displays the 3d model on OpenGL screen.
"""
 
class OpenGLGlyphs:
  
    # constants
    INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])
 
    def __init__(self):
        self.video_pth = 'sample_5.mp4'
        # initialise webcam and start thread
        # self.webcam = VideoStream(src="http://172.20.10.3:8160/").start()
        self.capture = cv2.VideoCapture(self.video_pth)
 
        # initialise shapes
        self.painting = None
        self.file = None
        self.cnt = 1
    
        # initialise texture
        self.texture_background = None

        print("getting data from file")
        with open(os.path.join('PickleFile','defined_calibration.pckl'), 'rb') as f:
            self.cam_matrix,self.dist_coefs = pickle.load(f)
 
    def _init_gl(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(37, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
      
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 300, 200, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
         
        # Load 3d object
        self.model3d_list = {3:OBJ('obj_files/mona_lisa/mona_lisa.obj'),
                             6:OBJ('obj_files/girl/girl.obj'),
                             8:OBJ('obj_files/Chardin_vase/Chardin_vase.obj'),
                             9:OBJ('obj_files/yell/yell.obj')}
        self.painting_list = {3:"obj_files/mona_lisa/mona_lisa.png",
                              6:"obj_files/girl/girl.jpg",
                              8:"obj_files/Chardin_vase/Chardin_vase.png",
                              9:"obj_files/yell/yell.png"}
        self.parameter_list = {3:[[0.0,0.05,0.08], 0.16],
                               6:[[-0.05,0.08,0.1], 0.12],
                               8:[[0.05,0.05,0.0], 0.16],
                               9:[[-0.08,0.29,0.1], 0.2]}
        # assign texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)
        self.painting = glGenTextures(1)
 
    def _draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        # get image from webcam
        # image = self.webcam.read()
        # image = imutils.resize(image,width=640)
        _, image = self.capture.read() 
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
  
        # create background texture
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
         
        # draw background
        # glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10)
        self._draw_background()
        glPopMatrix()
 
        # handle glyphs
        image = self._handle_glyphs(image)
        

        glutSwapBuffers()
    def _handle_painting(self, trans_mat, painting_path, parameter):
        # image = cv2.resize(cv2.imread(painting_path),(343,512))
        image = cv2.imread(painting_path)
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        # print("(ix,iy):",ix,iy)
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
  
        # create background texture
        glBindTexture(GL_TEXTURE_2D, self.painting)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
         
        # draw background
        glBindTexture(GL_TEXTURE_2D, self.painting)

        glPushMatrix()
        glLoadMatrixd(trans_mat)
        glTranslatef(parameter[0][0],parameter[0][1],parameter[0][2])
        glBegin(GL_QUADS)
        scale = parameter[1]
        k1 = 3*scale
        k2 = 5*scale
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0*k1, -1.0*k2, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0*k1, -1.0*k2, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0*k1,  1.0*k2, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0*k1,  1.0*k2, 0.0)
        glEnd()
        glPopMatrix()

    def _handle_glyphs(self, image):


        # aruco data
        # aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        # parameters =  aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)
        parameters = cv2.aruco.DetectorParameters_create()

        # height, width, channels = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        # image = cv2.aruco.drawDetectedMarkers(image=image, corners=corners, ids=ids, borderColor=(0, 255, 0)) # draw markers
        # image = cv2.aruco.drawDetectedMarkers(image=image, corners=rejectedImgPoints, borderColor=(0, 0, 255)) # draw ban markers 
        
        for x in [3,6,8,9]:
            idx = np.where(ids==x)
            if len(idx[0]) == 0:
                continue
            else:
                idx = idx[0][0]
            rvecs, tvecs ,_objpoints = aruco.estimatePoseSingleMarkers(corners,1.5,self.cam_matrix,self.dist_coefs)
            # for rvec, tvec in zip(rvecs, tvecs): # draw the axis 
            #     cv2.drawFrameAxes(image, self.cam_matrix,self.dist_coefs, rvec, tvec, 1) # show the axises

            rmtx = cv2.Rodrigues(rvecs[idx])[0]
            tvec = tvecs[idx]
            view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvec[0][0]],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvec[0][1]],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvec[0][2]],
                                    [0.0       ,0.0       ,0.0       ,1.0    ]])

            view_matrix = view_matrix * self.INVERSE_MATRIX

            view_matrix = np.transpose(view_matrix)
            self._handle_painting(view_matrix,self.painting_list[x],self.parameter_list[x])
            # load view matrix and draw shape
            glPushMatrix()
            glLoadMatrixd(view_matrix)

            glCallList(self.model3d_list[x].gl_list)

            glPopMatrix()
        # cv2.imshow("cv frame",image)
        # cv2.waitKey(1)
        

    def _draw_background(self):
        # draw background
        glBegin(GL_QUADS)
        k = 1
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0*k, -3.0*k, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0*k, -3.0*k, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0*k,  3.0*k, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0*k,  3.0*k, 0.0)
        glEnd( )


 
    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        # glutInitWindowSize(640, 480)
        glutInitWindowSize(960, 540)
        glutInitWindowPosition(500, 400)
        self.window_id = glutCreateWindow(b"OpenGL Glyphs")
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl(640, 480)
        glutMainLoop()
        # glutMainLoopEvent()
  
# run an instance of OpenGL Glyphs 
openGLGlyphs = OpenGLGlyphs()
openGLGlyphs.main()