import cv2
import os
import configparser
import time
import msvcrt

import video_to_images
import binarization
import noise_reduction
import data_export


def config_exists(config_file): # 如果配置文件不存在，创建默认配置

    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print(f"Configuration file {config_file} does not exist! \nCreating new configuration file...")

        config["video_to_images"] = {
            "input_path": "./input_videos",
            "output_path": "./video_to_images",
            "target_fps": "1",
            "image_format": "jpg",
            "output_width" : "640",
            "output_height" : "480",
            "scale_factor": "1.0",
            "jpeg_quality": "95"
        }

        config["binarization"] = {
            "input_path": "./input_images",
            "output_path": "./binary_images",
            "input_extension": '[".jpg", ".png", ".jepg"]',
            "output_extension": ".jpg",
            "overwrite_existing": "False",
            "threshold": "128"
        }

        config["noise_reduction"] = {
            "input_path" : "./binary_images",
            "output_path" : "./noise_reduction",
            "input_extension" : '[".jpg", ".png", ".jepg"]',
            "output_extension" : ".jpg",
            "overwrite_existing" : "True",
            "threshold" : "63",
            "sample_noise_reduction" : "True",
            "type" : "5, 3, 5, 3",
            "k1" : "5, 4, 2, 2",
            "k2" : "0, 4, 0, 5",
            "i" : "0, 2, 0, 2"
            "#(1ERODE腐蚀, 2DILATE膨胀, 3CLOSE先膨胀后腐蚀, 4OPEN先腐蚀后膨胀, 5CONTOUR绘制轮廓)"
            "#k结构元素，先宽后高，在轮廓绘制只取k1"
            "#i迭代次数，在轮廓绘制不可用"
        }

        config["data_export"] = {
            "input_path" : "./binary_images",
            "output_path" : "./noise_reduction",
            "input_extension" : '[".jpg", ".png", ".jepg"]',
            "CAMERA_FOCAL_LENGTH" : "45",
            "SENSOR_WIDTH" : "22.3",
            "SENSOR_HEIGHT" : "14.9",
            "IMAGE_WIDTH" : "1920",
            "IMAGE_HEIGHT" : "1080",
            "OBJECT_DISTANCE" : "2000",
            "X_FACTOR" : "1",
            "Y_FACTOR" : "1"
            
        }


        try:
            with open(config_file, "w") as f:
                config.write(f)
            print("配置文件已创建！")
        except FileNotFoundError:
            print(f"错误：路径 {config_file} 的目录不存在！")
        except PermissionError:
            print("错误：无写入权限！")
        except Exception as e:
            print(f"未知错误：{str(e)}")
        input("按 Enter 键继续...")
        return False

    else:
        return True


def main_load_config(config_file):

    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config

def handle_help():
    help_text = """
Available command:
  help           - Show this help
  function <number>    - Call function
  config <number>    - Show configuration of the function
  exit/quit/end      - Close this programe
  
    """
    print(help_text.strip())

def main():

    config_file = "./config.ini"
    configexists = None

    if config_exists(config_file) == False:
        configexists = True
    else:
        print(f"Loading config: {config_file} \n")

    config = main_load_config(config_file)
    config.read(config)
    config_1 = config["video_to_images"]
    config_2 = config["binarization"]
    config_3 = config["noise_reduction"]
    config_4 = config["data_export"]


    print("=== Command Window ===")
    print("Input 'help' to show help information.\n")

    while True:

        print(f"\nRefreshed config: {config_file}")
        config = main_load_config(config_file)
        config.read(config)
        config_1 = config["video_to_images"]
        config_2 = config["binarization"]
        config_3 = config["noise_reduction"]
        config_4 = config["data_export"]

        current_time = time.localtime()
        current_time = time.strftime("%H:%M:%S_%m.%d.%Y", current_time) # 获取当前时间,格式化时间
        print(current_time)

        try:
            
            raw_input = input(">>> ").strip()
            if not raw_input:
                continue

            
            parts = raw_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            
            if command in ("exit", "quit", "end"):
                print("Closing...")
                break

            elif command == "help":
                handle_help()
                
            elif command == "function":
                match args:
                    case "1":
                        print("Running function 1: Video to image...")
                        video_to_images.video_to_images(config_1)

                    case "2":
                        print("Running function 2: Binarization...")
                        binarization.binarization(config_2)

                    case "3":
                        print("Running function 3: Noise reduction...")
                        noise_reduction.noise_reduction(config_3)

                    case "4":
                        print("Running function 4: Data export...")
                        data_export.data_export(config_4)

                    case _:
                        print("Code is unavailable.")
                
            elif command == "config":
                match args:
                    case "1" | "video_to_images":
                        print("Printing config of function 1: Video to image...\n")
                        print(config["video_to_images"])
                        for key, val in config.items("video_to_images"):
                            print(f"{key} = {val}")
                        

                    case "2":
                        print("Printing config of function 2: Binarization...\n")
                        print(config["binarization"])
                        for key, val in config.items("binarization"):
                            print(f"{key} = {val}")

                    case "3":
                        print("Printing config of function 3: Noise reduction...\n")
                        print(config["noise_reduction"])
                        for key, val in config.items("noise_reduction"):
                            print(f"{key} = {val}")

                    case "4":
                        print("Printing config of function 4: Data export...\n")
                        print(config["data_export"])
                        for key, val in config.items("data_export"):
                            print(f"{key} = {val}")

                    case _:
                        print("Code is unavailable.")
                
                
            else:
                print(f"Error: Unkonwn command '{command}', Input 'help' to show help information.")

        except KeyboardInterrupt:
            print("\nCompulsory withdrawal, being terminated...")
            break
        except Exception as e:
            print(f"System error: {str(e)}")








if __name__ == "__main__":

    main()

#input_path = config_1["input_path"]
#print(input_path)

#video_to_images.video_to_images(config_1)  #转图片函数
#input()
