# Processing-flame-images-recorded-in-an-experimental-setting-to-obtain-data.
Generall:
This project is a program for processing flame images recorded in an experimental setting to obtain data such as flame height and size in the video over time.

==================================================

File description: 

config.ini: 
Configuration file, stores all parameters such as file path, the configuration file will be explained in detail.

main:
Command Window code, support for unified invocation of each function, easy to record traces of function usage (excluding automatic logging). And support for automatic initialization of configuration files (not tested).

video_to_images: 
Related parameters are edited in the configuration file.

binarization: 
Convert any image to a binary image using a specific algorithm or threshold (gray: 0|255), you can use the Ostu algorithm, Triangle algorithm, Fixed Threshold three modes, the threshold and other parameters are edited in the configuration file.

noise_reduction: 
Import and perform noise reduction on binary images under the path. Has a take sample noise reduction function: manually make a sample image and highlight the non-flame areas. The program will read the sample images from a specific directory and remove the non-flame areas from the image to be noise reduced. The noise reduction uses a sequence of operations, which can be edited in the configuration file.
Tip: The format of binary image to use sould be like:


----binary_images

    ----sample
    
        ----sample_1.jpg
        

    ----frame000001.jpg

    ----frame000002.jpg

    ----frame000003.jpg

    ...


data_export: 
Scan binary images under path and export flame data to .csv file according to set parameters like distance and focus. The correction factor need to be calibrated by yourself, the relevant parameters are modified in the configuration file

==================================================

config.ini description:

[video_to_images]

input_path = ./input_videos

output_path = ./video_to_images

target_fps = 25

#target fps for the images export

image_format = jpg

output_width = 1920

output_height = 1080

scale_factor = 1.0

jpeg_quality = 95

#Available when format is jpg or jepg

[binarization]

input_path = ./video_to_images

output_path = ./binary_images

input_extension = [".jpg", ".png", ".jepg"]

output_extension = .jpg

overwrite_existing = False

threshold = 63

#The threshold of the binarization, use -1 to apply OSTU Algorithm, use -2 to apply Triangle Algorithm.

[noise_reduction]

input_path = ./binary_images

output_path = ./noise_reduction

input_extension = [".jpg", ".png", ".jepg"]

output_extension = .jpg

overwrite_existing = True

threshold = 63

sample_noise_reduction = True

contours_num = 8

type = 5, 3, 5, 3

k1 = 5, 4, 2, 2

k2 = 0, 4, 0, 5

i = 0, 2, 0, 2

#type: Sequence of operations applied to the image to be noise reduced, the following morphological operations can be used:

#Morphological operation: 1 ERODE, 2 DILATE, 3 CLOSE, 4 OPEN, 5 DRAW_CONTOUR)

#k: structure elements, width first, then height, in contour drawing only take k1 

#i: iteration count, not available in contour drawing

[data_export]

input_path = ./noise_reduction

output_path = ./data_output

input_extension = [".jpg", ".png", ".jepg"]

step = 1

CAMERA_FOCAL_LENGTH = 45

SENSOR_WIDTH = 22.3

SENSOR_HEIGHT = 14.9

#For example: Size of the CMOS.

IMAGE_WIDTH = 1920

IMAGE_HEIGHT = 1080

#Images' resolution.

OBJECT_DISTANCE = 2500

#Distance between fire center and sensor of camera.

X_FACTOR = 1.177

Y_FACTOR = 0.85

#Need to be calibrated by yourself.
