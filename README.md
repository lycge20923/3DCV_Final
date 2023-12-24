# 3DCV Final Project Team 18
## Virtual Museam: Infuse Life into Art

### Content
1. **Code & Model:** All in this project
2. **Data:**
    * Image of artworks and its obj files: All stored in the ```Artwork_Images``` folder
    * The video for plane detection and its output(result): Stored in ```Sample.mp4``` and ```Det_output.mp4```
    * The resultant video: ```final.mov``` 
    * (Optional)Calibration Board and its relative video for camera calibration: stored in the ```CharucoBoard``` folder, and the result of Camera Calibration, Camera Matrix and Distotion Coefficient, are stored in the ```PickleFile/defined_calibration.pckl```
    * (Optional)Examples of Aruco Markers: Stored in ```ArucoMarkers``` folder.
3. **Report:** ```3DCV_Team18_Report.pdf```
4. **PowerPoint for Presentation:** ```3dcv2023_final_group_18.pdf```
5. **How to Implement:** Describe bellow

### Code Implementation
#### Image-to-3D
* Follow the ```readme.md``` in the ```image-to-3d``` folder to set and implement
* The Image of artworks we implemented are stored in the ```Artwork_Images```, and the output ```obj file``` are stored in the ```obj_files``` directory.

#### Aruco-Marker
* First, download the required packages
    ```
    pip install opencv-python opencv-contrib-python==4.6.0.66
    ```
* Then run the following code, the output would be stored in the ```Det_output.mp4```

    ```
    python PlaneDetection.py --video_path Sample.mp4 
    ```

* Appendix
    1. You could generate the Aruco Marker by yourself by conducting the following code. The result would stored in the ```ArucoMarkers``` directory.

    ```
    python ArucoMarkers.py --number num_you_want_generate
    ```

    2. You could also generate Calibration Board by yourself. Try to check the ```CharucoBoard.py``` and conduct the following code with adding some parameters.
    ```
    python CharucoBoard.py 
    ```

#### OpenGL
* Config.

    ```
    pip install pyopengl
    ```

* Try to implement the following codes
    ```
    python3 opengl_implement/opengl_.py
    ```

