import cv2
import os
import configparser
import time
from pathlib import Path
import numpy as np


def processing(img, type, k1, k2, i):
    img_1 = img
    type = type.upper()
    match type:
        case "1" | "ERODE":
            img_2 = cv2.morphologyEx(img_1, cv2.MORPH_ERODE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k1, k2)), iterations = i)

        case "2" | "DILATE":
            img_2 = cv2.morphologyEx(img_1, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k1, k2)), iterations = i)

        case "3" | "CLOSE":
            img_2 = cv2.morphologyEx(img_1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k1, k2)), iterations = i)

        case "4" | "OPEN":
            img_2 = cv2.morphologyEx(img_1, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k1, k2)), iterations = i)

        case "5" | "CONTOUR":
            img_2 = img_1
            contours, hierarchy = cv2.findContours(img_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img_2, contours, -1, (255, 255, 255), int(k1))
        case _:
            img_2 = img_1

    return img_2


def sample_noise_reduiction(img, sample):  

    for n in range(len(sample)):
        sample_contours, hierarchy = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(sample, sample_contours, -1, (255, 255, 255), 3)




def noise_reduction(config_section):

    config = config_section
    
    
    input_path = config["input_path"]
    output_path = config["output_path"]
    input_extension = config["input_extension"]
    output_extension = config["output_extension"]
    overwrite = config.getboolean("overwrite_existing")
    threshold = int(config["threshold"])
    snr = bool(config["sample_noise_reduction"])
    contours_num = int(config["contours_num"])
    type = [item.strip() for item in config.get("type").split(",")]
    k1 = [item.strip() for item in config.get("k1").split(",")]
    k2 = [item.strip() for item in config.get("k2").split(",")]
    i = [item.strip() for item in config.get("i").split(",")]

    
    image_files_out = []
    image_files_in = []
    image_files = []

    image_files_out = os.listdir(input_path)
    #print(f"文件列表为{image_files_out}")



    for f_out in image_files_out:   
        path_out = os.path.join(input_path, f_out)
        #print(path_out)
        print(f"Processing: {path_out}")
        if Path(path_out).is_dir():    
            image_files_in = os.listdir(Path(path_out))
            #print(f"内层文件列表：{image_files_in}")
            output_dir = os.path.join(output_path, f_out)
            os.makedirs(Path(output_dir), exist_ok=True)

            if snr == True: 
                snr_path = os.path.join(path_out, "sample")
                snr_files = os.listdir(snr_path)
                sample = []
                first = True
                for f_s_1 in snr_files:

                    img_s = cv2.imread(os.path.join(snr_path,f_s_1), cv2.IMREAD_GRAYSCALE)
                    ret, b_img_s = cv2.threshold(img_s, threshold, 255, cv2.THRESH_BINARY)
                    #cv2.imshow("img",b_img_s)
                    #cv2.waitKey()
                    if first == True:
                        f_s_2 = np.zeros_like(img_s)
                        first = False
                    #cv2.imshow("img",img_s)
                    #cv2.waitKey()
                    #cv2.imshow("img",f_s_2)
                    #cv2.waitKey()
                    f_s_2 = cv2.add(f_s_2,img_s)
                #cv2.imshow("img",f_s_2)
                #cv2.waitKey()

                sample_contours, hierarchy = cv2.findContours(f_s_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(f_s_2, sample_contours, -1, (255, 255, 255), 3)
                f_s_2 = cv2.morphologyEx(f_s_2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations = 10)
                #cv2.imshow("img!",f_s_2)
                #cv2.waitKey()
                #sample_contours, hierarchy = cv2.findContours(f_s_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                #cv2.drawContours(f_s_2, sample_contours, -1, (255, 255, 255), 1)
                #cv2.imshow("img!",f_s_2)
                #cv2.waitKey()

                    
            #print(f"f_out={f_out}")
            #print(f"path_out={path_out}")
            #print(f"snr_path={snr_path}")

            for f_in in image_files_in: 
                path_in = os.path.join(path_out, f_in)
                #print(path_in)
                f_ext = Path(path_in).suffix.lower()
                if f_ext in input_extension:
                    #print(f"找到文件{path_in}")
                    if os.path.isdir(path_in):
                        continue
                    else:

                        try:    
                            
                            img = cv2.imread(path_in, cv2.IMREAD_GRAYSCALE)
                            ret, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
                            img_1 = binary_img

                            if snr == True:
                                
                                assert f_s_2.shape == binary_img.shape, "Differences in image and sample resolution!"
                                img_1 = cv2.subtract(img_1, f_s_2)
                                #cv2.imshow("img",img_1)
                                #cv2.waitKey()


                            img_n = []
                            for n in range(len(type)):
                                try:
                                    img_n += [processing(img_1, type[n], int(k1[n]), int(k2[n]), int(i[n]))]

                                except:
                                    print(f"Error with processing {Path(output_file)} !")
                                    

                            
                            img_2 = img_n[len(type)-1]


                            contours, hierarchy = cv2.findContours(img_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            cv2.drawContours(img_2, contours, -1, (255, 255, 255), 1)
                            #cv2.imshow("img",img_2)
                            #cv2.waitKey()

                            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                            keep_contours = sorted_contours[:contours_num] if contours_num <= len(sorted_contours) else sorted_contours   

                            gray = img_2.copy()
                            mask = np.zeros_like(gray)  
                            cv2.drawContours(mask, keep_contours, -1, 255, cv2.FILLED)  
                            original = img_2.copy()
                            #print("输入图像:", img_iteration.shape)  
                            #print("掩膜:", mask.shape)        
                            img_3 = cv2.bitwise_and(original, original, mask=mask)  
                            #cv2.imshow("img",img_3)
                            #cv2.waitKey()

                            img_4 = cv2.morphologyEx(img_3, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations = 1)
                            #cv2.imshow("img",img_4)
                            #cv2.waitKey()


                            output_file = os.path.join(output_dir, Path(f_in).stem + output_extension)
                            cv2.imwrite(Path(output_file), img_3)

                        except:
                            if output_file == None:
                                output_file = '1'
                            print(f"Error with processing {Path(output_file)} !")
                            
            print(f"Saved {len(image_files_in)-1} images in: {output_dir}\n")




if __name__ == "__main__":
    config_file = "./config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    noise_reduction(config["noise_reduction"])
    