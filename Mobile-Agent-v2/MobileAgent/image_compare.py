import os
import cv2
import time
import numpy as np

from skimage.metrics import structural_similarity


from MobileAgent.controller import get_screenshot


def wait_screen_loading(adb_path):
    # 每3秒截图，对比前一张截图，如果大致相同则认为加载完成
    screenshot_file = "./screenshot/screenshot.jpg"
    get_screenshot(adb_path, print_flag=False)  # 获取屏幕截图
    last_screenshot_file = "./screenshot/screenshot_last.jpg"
    now_screenshot_file = "./screenshot/screenshot_now.jpg"
    if os.path.exists(last_screenshot_file):
        os.remove(last_screenshot_file)
    os.rename(screenshot_file, last_screenshot_file)
    while True:
        time.sleep(3)
        get_screenshot(adb_path, print_flag=False)  # 获取屏幕截图
        if os.path.exists(now_screenshot_file):
            os.remove(now_screenshot_file)
        os.rename(screenshot_file, now_screenshot_file)
        # 对比 last_screenshot_file 和 now_screenshot_file
        # 如果相同，则认为加载完成，退出循环
        if ssim(last_screenshot_file, now_screenshot_file) > 0.90:
            print("屏幕内容加载完成！")
            break
        else:
            if os.path.exists(last_screenshot_file):
                os.remove(last_screenshot_file)
            os.rename(now_screenshot_file, last_screenshot_file)


def ssim(file1, file2):

    # 加载两张图片
    image1 = cv2.imread(file1)
    image2 = cv2.imread(file2)

    # 图片转换为灰度
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性
    (score, diff) = structural_similarity(gray1, gray2, full=True)
    return score


if __name__ == "__main__":
    path1 = "D:\\Users\\Administrator\\Desktop\\1.jpg"
    path2 = "D:\\Users\\Administrator\\Desktop\\2.jpg"
    path3 = "D:\\Users\\Administrator\\Desktop\\3.jpg"
    path4 = "D:\\Users\\Administrator\\Desktop\\4.jpg"

    print(f"{ssim(path1, path2)=}")
    print(f"{ssim(path2, path3)=}")
    print(f"{ssim(path2, path4)=}")
    print(f"{ssim(path3, path4)=}")
