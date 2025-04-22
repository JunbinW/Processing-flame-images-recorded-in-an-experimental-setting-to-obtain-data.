import cv2
import os
import configparser
import csv
import numpy as np
from pathlib import Path
import time

def data_export(config_section):
    config = config_section
    
    input_path = config["input_path"]
    output_path = config["output_path"]
    input_extension = config["input_extension"]
    step = int(config["step"])
    
    CAMERA_FOCAL_LENGTH = int(config["CAMERA_FOCAL_LENGTH"])
    SENSOR_WIDTH = float(config["SENSOR_WIDTH"])
    SENSOR_HEIGHT = float(config["SENSOR_HEIGHT"]) 
    IMAGE_WIDTH = int(config["IMAGE_WIDTH"]) 
    IMAGE_HEIGHT = int(config["IMAGE_HEIGHT"]) 
    OBJECT_DISTANCE = int(config["OBJECT_DISTANCE"]) 
    X_FACTOR = float(config["X_FACTOR"])
    Y_FACTOR = float(config["Y_FACTOR"])



    
    pixel_width = (SENSOR_WIDTH / IMAGE_WIDTH) * (OBJECT_DISTANCE / CAMERA_FOCAL_LENGTH) * X_FACTOR
    pixel_height = (SENSOR_HEIGHT / IMAGE_HEIGHT) * (OBJECT_DISTANCE / CAMERA_FOCAL_LENGTH) * Y_FACTOR
    pixel_area = pixel_width * pixel_height

    
    os.makedirs(output_path, exist_ok=True)
    current_time = time.localtime()
    current_time = time.strftime("%H%M%S_%m%d%Y", current_time) 

    files_out = os.listdir(input_path)
    

    for f_out in files_out:
        results = []
        path_out = os.path.join(input_path, f_out)
        #print(f"{files_out}")
        #print(f"{f_out}")
        print(f"Processing: {path_out}")
        if Path(path_out).is_dir():
            files_in = os.listdir(Path(path_out))
            #print(f"内层文件列表：{files_in}")
            output_dir = os.path.join(output_path, f_out)

            sum_pixel_height_val = 0
            sum_actual_height = 0
            sum_area_pixel = 0
            sum_actual_area = 0

            p_pixel_height_val = 0
            p_area_pixel = 0
            p_actual_height = 0
            p_actual_area = 0


            step_count = 0

            for f_in in files_in:
                path_in = os.path.join(path_out, f_in)
                #print(path_in)
                f_ext = Path(path_in).suffix.lower()
                if f_ext in input_extension:
                    #print(f"找到文件{path_in}")
                    
                    
                    img = cv2.imread(path_in, cv2.IMREAD_GRAYSCALE)

                    if img is None:
                        print(f"Error with loading: {path_in}")
                        continue
                        
                    

                    
                    y_coords, x_coords = np.where(img == 255)
                    
                    """if len(y_coords) == 0:
                        results.append((f_in, 0, 0, 0, 0, sum_pixel_height_val, sum_area_pixel, round(sum_actual_height, 0), round(sum_actual_area, 0)))
                        continue"""

                    
                    contours, img = cv2.findContours(img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                    if y_coords.size == 0:
                        print(f"None data in: {path_in}")
                        
                        min_y, max_y = 0, 0 
                    else:
                        min_y, max_y = np.min(y_coords), np.max(y_coords)
                    
                    if len(contours) > 0:
                        
                        pixel_height_val = max([cv2.boundingRect(contour)[3] for contour in contours])
                        
                    else:
                        pixel_height_val = 0
                    actual_height = round(pixel_height_val * pixel_height, 1)

                    
                    area_pixel = len(y_coords)
                    actual_area = round(area_pixel * pixel_area, 1)

                    
                    sum_pixel_height_val += pixel_height_val
                    sum_actual_height += actual_height
                    sum_area_pixel += area_pixel
                    sum_actual_area += actual_area

                    
                    p_pixel_height_val += pixel_height_val
                    p_area_pixel += area_pixel
                    p_actual_height += actual_height
                    p_actual_area += actual_area


                    if step_count == 0:
                        results.append((f_in, step_count, 
                            round(p_pixel_height_val,0), 
                            round(p_area_pixel,0), 
                            round(p_actual_height,0), 
                            round(p_actual_area,0), 
                            sum_pixel_height_val, 
                            sum_area_pixel, 
                            round(sum_actual_height, 0), 
                            round(sum_actual_area, 0)))
                        p_pixel_height_val = 0
                        p_area_pixel = 0
                        p_actual_height = 0
                        p_actual_area = 0
                        #print("Saved")
                        step_count += 1
                        continue

                    if (step_count % step) == 0:
                        results.append((f_in, step_count/step, 
                            round(p_pixel_height_val/step,0), 
                            round(p_area_pixel/step,0), 
                            round(p_actual_height/step,0), 
                            round(p_actual_area/step,0), 
                            sum_pixel_height_val, 
                            sum_area_pixel, 
                            round(sum_actual_height, 0), 
                            round(sum_actual_area, 0)))
                        p_pixel_height_val = 0
                        p_area_pixel = 0
                        p_actual_height = 0
                        p_actual_area = 0
                        #print("Saved")
                    step_count += 1
                    continue

        #print(f"results: {results}")

        
        csv_path = os.path.join(output_path, f_out + ".csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([f_out, "period", "height_pixel", "area_pixel", "height_mm", "area_mm2", "sum_height_pixel", "sum_area_pixel", "sum_height_mm", "sum_area_mm2"])
            writer.writerows(results)
    
        print(f"Scaned {step_count} images, savd {int(step_count/step)+1} data in: {csv_path}\n")
            

if __name__ == "__main__":
    config_file = "./config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    data_export(config["data_export"])