import cv2
import os
import configparser
import time
from pathlib import Path


def binarization(config_section):

    config = config_section
    
    
    input_path = config["input_path"]
    output_path = config["output_path"]
    input_extension = config["input_extension"]
    output_extension = config["output_extension"]
    overwrite = config.getboolean("overwrite_existing")
    binary_threshold = int(config["threshold"])

    
    image_files_out = []
    image_files_in = []
    image_files = []

    image_files_out = os.listdir(input_path)
    #print(f"文件列表为{image_files_out}")

    if binary_threshold == -2:
        print("Applied Triangle Algorithm.")
        for f_out in image_files_out:
            path_out = os.path.join(input_path, f_out)
            #print(path_out)
            if Path(path_out).is_dir():
                image_files_in = os.listdir(Path(path_out))
                #print(f"内层文件列表：{image_files_in}")

                n=0
                for f_in in image_files_in:
                    path_in = os.path.join(path_out, f_in)
                    #print(path_in)
                    f_ext = Path(path_in).suffix.lower()
                    if f_ext in input_extension:
                        #print(f"找到文件{path_in}")
                        try:

                            img = cv2.imread(path_in, cv2.IMREAD_GRAYSCALE)
                            ret, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
                            output_dir = os.path.join(output_path, f_out + "_TRIANGLE")
                            os.makedirs(Path(output_dir), exist_ok=True)
                            output_file = os.path.join(output_dir, Path(f_in).stem + output_extension)
                            cv2.imwrite(Path(output_file), binary_img)
                            n+=1
                           
                        except:
                            print(f"Error with processing {Path(output_file)} !")
                            
                print(f"Saved {n} images in: {output_dir} ; Triangle Algorithm.")
            os.makedirs(os.path.join(Path(output_dir),"sample"), exist_ok=True)



    elif binary_threshold == -1:
        print("Applied OSTU Algorithm.")
        for f_out in image_files_out:
            path_out = os.path.join(input_path, f_out)
            #print(path_out)
            if Path(path_out).is_dir():
                image_files_in = os.listdir(Path(path_out))
                #print(f"内层文件列表：{image_files_in}")

                n=0
                for f_in in image_files_in:
                    path_in = os.path.join(path_out, f_in)
                    #print(path_in)
                    f_ext = Path(path_in).suffix.lower()
                    if f_ext in input_extension:
                        #print(f"找到文件{path_in}")
                        try:

                            img = cv2.imread(path_in, cv2.IMREAD_GRAYSCALE)
                            ret, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            output_dir = os.path.join(output_path, f_out + "_OTSU")
                            os.makedirs(Path(output_dir), exist_ok=True)
                            output_file = os.path.join(output_dir, Path(f_in).stem + output_extension)
                            cv2.imwrite(Path(output_file), binary_img)
                            n+=1
                           
                        except:
                            print(f"Error with processing {Path(output_file)} !")
                            
                print(f"Saved {n} images in: {output_dir} ; OSTU Algorithm.")
            os.makedirs(os.path.join(Path(output_dir),"sample"), exist_ok=True)


    else:
        print(f"Applied Customized global fixed threshold: {binary_threshold}.")
        for f_out in image_files_out:
            path_out = os.path.join(input_path, f_out)
            #print(path_out)
            if Path(path_out).is_dir():
                image_files_in = os.listdir(Path(path_out))
                #print(f"内层文件列表：{image_files_in}")
                
                n=0
                for f_in in image_files_in:
                    path_in = os.path.join(path_out, f_in)
                    #print(path_in)
                    f_ext = Path(path_in).suffix.lower()
                    if f_ext in input_extension:
                        #print(f"找到文件{path_in}")
                        try:

                            img = cv2.imread(path_in, cv2.IMREAD_GRAYSCALE)
                            ret, binary_img = cv2.threshold(img, binary_threshold, 255, cv2.THRESH_BINARY)
                            output_dir = os.path.join(output_path, f_out + "_" + str(binary_threshold))
                            os.makedirs(Path(output_dir), exist_ok=True)
                            output_file = os.path.join(output_dir, Path(f_in).stem + output_extension)
                            cv2.imwrite(Path(output_file), binary_img)
                            n+=1
                           
                        except:
                            print(f"Error with processing {Path(output_file)} !")
                            
                print(f"Saved {n} images in: {output_dir} ;Customized threshold: {binary_threshold}.")             
            os.makedirs(os.path.join(Path(output_dir),"sample"), exist_ok=True)
            

            #else:  #对于非文件夹进行操作

        """with open Path(os.path.join(output_dir, config.txt)) as config:
                                    write(f"")"""
  

if __name__ == "__main__":
    config_file = "./config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    binarization(config["binarization"])