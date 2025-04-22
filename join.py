import os
import cv2
import numpy as np

def cv_stitch_images(input_dir, output_path, columns):
    """
    使用OpenCV实现的图片拼接工具
    
    :param input_dir: 图片目录路径
    :param output_path: 输出图片路径
    :param columns: 每行图片数量
    """
    # 获取排序后的文件列表（不区分大小写）
    files = sorted(os.listdir(input_dir), key=str.lower)
    if not files:
        raise ValueError("输入目录为空")

    # 校验所有文件扩展名一致
    extensions = {os.path.splitext(f)[1].lower() for f in files}
    if len(extensions) != 1:
        raise ValueError("目录中存在不同扩展名的文件")
    ext = extensions.pop()

    # 过滤非图片文件（通过尝试读取验证）
    images = []
    valid_files = []
    for f in files:
        file_path = os.path.join(input_dir, f)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append(img)
            valid_files.append(f)
        else:
            print(f"警告：忽略非图片文件 {f}")
    
    if not images:
        raise ValueError("目录中未找到有效图片")

    # 校验所有图片尺寸一致
    first_shape = images[0].shape
    for i, img in enumerate(images[1:]):
        if img.shape != first_shape:
            err_msg = f"图片尺寸不一致：\n{valid_files[0]} {first_shape}\n{valid_files[i+1]} {img.shape}"
            raise ValueError(err_msg)

    # 计算拼接布局
    img_h, img_w = first_shape[:2]
    img_count = len(images)
    rows = (img_count + columns - 1) // columns

    # 创建画布（自动处理灰度/彩色图）
    if len(first_shape) == 3:
        canvas = np.zeros((img_h*rows, img_w*columns, first_shape[2]), dtype=np.uint8)
    else:
        canvas = np.zeros((img_h*rows, img_w*columns), dtype=np.uint8)

    # 填充图片到画布
    for index, img in enumerate(images):
        row = index // columns
        col = index % columns
        y = row * img_h
        x = col * img_w
        canvas[y:y+img_h, x:x+img_w] = img

    # 保存结果（自动根据扩展名选择格式）
    if not cv2.imwrite(output_path, canvas):
        raise ValueError("保存失败，请检查输出路径和文件权限")

    print(f"成功拼接 {len(images)} 张图片 → {output_path}")


# 使用示例
if __name__ == "__main__":
    cv_stitch_images(
        input_dir="F:\college/FPST4994/fireload1_exp/en_version/noise_reduction/ny_random1_1_102257_04192025_128_1",    # 图片目录
        output_path="./join/cv_output.jpg",  # 输出路径
        columns = 5               # 每行n张图片
    )