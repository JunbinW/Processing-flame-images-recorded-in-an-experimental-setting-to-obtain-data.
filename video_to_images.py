import cv2
import os
import configparser
import time

CONFIG_FILE = "config.ini"
time_unit = 65536


def calculate_frame_time(video_fps, target_fps):
    
    frame_time = time_unit / target_fps

    if video_fps < target_fps:
        print("Target fps is greater than the average frame rate for this video, duplicate frames may occur!")

    return frame_time


def video_to_images(config_section):
    config = config_section
    
    
    input_path = config["input_path"]
    output_path = config["output_path"]
    target_fps = float(config["target_fps"])
    image_format = config["image_format"]
    output_width = int(config["output_width"])
    output_height = int(config["output_height"])
    scale_factor = float(config["scale_factor"])
    jpeg_quality = int(config["jpeg_quality"])

    output_width = int(output_width*scale_factor)
    output_height = int(output_height*scale_factor)

    
    video_files = []
    if os.path.isfile(input_path):
        video_files = [input_path]
    else:
        for f in os.listdir(input_path):
            if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):
                video_files.append(os.path.join(input_path, f))

    for video_path in video_files:
        current_time = time.localtime()
        current_time = time.strftime("%H%M%S_%m%d%Y", current_time)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_output_dir = os.path.join(output_path, video_name+"_"+current_time)
        os.makedirs(video_output_dir, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Failed to read the video: {video_path}")
            continue

        
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        #frame_interval = calculate_frame_interval(video_fps, target_fps)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        video_frame_time = time_unit / video_fps
        frame_time = calculate_frame_time(video_fps, target_fps)

        print(f"\nProcessing video: {os.path.basename(video_path)}")
        print(f"Original frame rate: {video_fps:.2f} FPS, Target frame rate: {target_fps} FPS，Target frame length: {frame_time/65.536 :.2f} ms")
        print(f"Total frames: {total_frames}，Original dimension: {width}x{height}")


        #frame_count = 0
        #frame_pos = 0

        f1 = 0
        f2 = 0

        for f1 in range(total_frames):
            #print(f1,f2)
            ret, frame = cap.read()
            if not ret:
                break

            if ((f1+1)*video_frame_time) <= ((f2+1)*frame_time):

                
                frame = cv2.resize(frame, (output_width, output_height), interpolation=cv2.INTER_AREA)
                
                img_name = f"frame_{f2+1:06d}.{image_format}"
                img_path = os.path.join(video_output_dir, img_name)
                frame
                
                save_params = []
                if image_format.lower() == "jpg":
                    save_params = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
                
                cv2.imwrite(img_path, frame, save_params)
            else:
                f2 += 1

        cap.release()
        print(f"Finished processing: [{os.path.basename(video_path)}], Saved [{f2+1}] images, Actual frame rate: {f2/(f1/video_fps):.2f}-{(f2+1)/(f1/video_fps):.2f} FPS, Output dimension: {output_width}x{output_height}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    video_to_images(config["video_to_images"])
