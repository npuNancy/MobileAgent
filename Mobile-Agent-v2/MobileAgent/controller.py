import os, re
import time
import subprocess
from PIL import Image


def get_location(adb_path):

    return "Home"
    # 返回经纬度
    command = adb_path + " shell dumpsys location"
    result = subprocess.run(command, capture_output=True, text=True, shell=True).stdout

    # 使用正则，查找经纬度
    # last location=Location[network 40.003831,116.329476 hAcc=15.0 et=+1d1h11m29s41ms {Bundle[{indoor=0, provider=wifi, source=2}]}]
    pattern = r"last location=Location\[network(.*?)hAcc="
    match = re.search(pattern, result)
    if match:
        location = match.group(1).strip()
        return location

    return ""


def get_phone_time(adb_path):
    command = adb_path + " shell date +%Y-%m-%d_%H:%M:%S"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def set_default_input_method(adb_path):
    # 设置默认输入法为 ADB Keyboard
    command = adb_path + " shell ime set com.android.adbkeyboard/.AdbIME"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    if process.returncode != 0:
        print("Error: 设置默认输入法失败")
        print(process.stderr)
    else:
        print("默认输入法已设置为 ADB Keyboard")


def get_screenshot(adb_path, print_flag=True):
    if print_flag:
        print("正在获取截图....")
    # 删除旧的截图
    command = adb_path + " shell rm /sdcard/screenshot.png"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    if process.returncode != 0:
        print("Error: 删除截图失败")
        print(process.stderr)
    time.sleep(0.5)
    # 获取新的截图
    command = adb_path + " shell screencap -p /sdcard/screenshot.png"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    if process.returncode != 0:
        print("Error: 截图失败")
        print(process.stderr)
    time.sleep(0.5)
    # 下载截图
    command = adb_path + " pull /sdcard/screenshot.png ./screenshot"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    if process.returncode != 0:
        print("Error: 拉取截图失败")
        print(process.stderr)
    time.sleep(0.5)
    image_path = "./screenshot/screenshot.png"
    save_path = "./screenshot/screenshot.jpg"
    image = Image.open(image_path)
    image.convert("RGB").save(save_path, "JPEG")
    os.remove(image_path)


def tap(adb_path, x, y):
    command = adb_path + f" shell input tap {x} {y}"
    subprocess.run(command, capture_output=True, text=True, shell=True)


def type(adb_path, text):
    text = text.replace("\\n", "_").replace("\n", "_")
    for char in text:
        if char == " ":
            command = adb_path + f" shell input text %s"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif char == "_":
            command = adb_path + f" shell input keyevent 66"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif "a" <= char <= "z" or "A" <= char <= "Z" or char.isdigit():
            command = adb_path + f" shell input text {char}"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif char in "-.,!?@'°/:;()":
            command = adb_path + f' shell input text "{char}"'
            subprocess.run(command, capture_output=True, text=True, shell=True)
        else:
            command = adb_path + f' shell am broadcast -a ADB_INPUT_TEXT --es msg "{char}"'
            subprocess.run(command, capture_output=True, text=True, shell=True)


def slide(adb_path, x1, y1, x2, y2):
    command = adb_path + f" shell input swipe {x1} {y1} {x2} {y2} 500"
    subprocess.run(command, capture_output=True, text=True, shell=True)


def back(adb_path):
    command = adb_path + f" shell input keyevent 4"
    subprocess.run(command, capture_output=True, text=True, shell=True)


def home(adb_path):
    command = adb_path + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    subprocess.run(command, capture_output=True, text=True, shell=True)


def open_douyin(adb_path):
    command = adb_path + f" shell am start com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.splash.SplashActivity"
    subprocess.run(command, capture_output=True, text=True, shell=True)


if __name__ == "__main__":
    import time

    adb_path = "adb -s hyiz5hjvz975mrdq"
    open_douyin(adb_path)
