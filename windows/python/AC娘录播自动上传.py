import re
import tkinter as tk
from tkinter import filedialog
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
#用于使用pywin32操作上传
import win32gui
import win32con
import cv2
import random
#必须安装的包：selenium pywin32 cv2


#定义函数使用对话框导入文件同时获取文件名
def get_filename():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename()  # 打开文件选择对话框
    return file_path

#调用pywin32定义upload函数，此步经测试成功实现。
def upload(filePath, browser_type="chrome"):
    '''
    通过pywin32模块实现文件上传的操作
    :param filePath: 文件的绝对路径
    :param browser_type: 浏览器类型（默认值为chrome）
    :return:
    '''
    if browser_type.lower() == "chrome":
        title = "打开"
    elif browser_type.lower() == "firefox":
        title = "文件上传"
    elif browser_type.lower() == "ie":
        title = "选择要加载的文件"
    elif browser_type.lower() == "edge":
        title = "打开"
    else:
        title = "打开"  # 这里根据其它不同浏览器类型来修改

    # 找元素
    # 一级窗口"#32770","打开"；找到窗口，在根据不同浏览器传入 title
    dialog = win32gui.FindWindow("#32770", title)
    # 向下传递
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)   # 三级
    # 编辑按钮
    edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
    # 打开按钮
    button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级

    # 输入文件的绝对路径，点击“打开”按钮
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮

#基础信息定义
origin_file_path = get_filename()
file_name_without_extension = os.path.splitext(os.path.basename(origin_file_path))[0] #获取不带后缀的文件名
#print("输入的文件名是:\n",file_name_without_extension)
new_file_name_without_extension = file_name_without_extension.replace(" ", "-") #替换空格，避免处理出错

s_text_origin = new_file_name_without_extension[:19] #提取开头到第十个字符（固定部分）
title = re.search(r'-([^-]+)$', new_file_name_without_extension).group(1)  
formatted_date = s_text_origin.replace("-", "")
output = f"[AC娘录播] {title} {formatted_date[:8]}直播录播"
simpletext=f"开播时间:{s_text_origin}"

print("输入的文件绝对路径是：\n",origin_file_path)
print("输出的标题是:\n",output)
print("简介内容是:\n",simpletext)
print("即将调用edge dev进行网页调试\n")

service = Service(executable_path='C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe')
option = webdriver.EdgeOptions()
driver = webdriver.Edge(options = option)
#option = webdriver.ChromeOptions()
#driver = webdriver.Chrome(options = option)

#打开登录界面
driver.get('https://www.acfun.cn/login/')
switch_login = driver.find_element(By.ID, "login-switch")
switch_login.click()
username_input = driver.find_element(By.ID, 'ipt-account-login')
password_input = driver.find_element(By.ID, 'ipt-pwd-login')
username_input.send_keys('用户名')
sleep(2)
password_input.send_keys('密码')
login_button = driver.find_element(By.XPATH, '//*[@id="form-login"]/div[4]/div')
login_button.click()
sleep(10)
print("\n登陆成功！准备跳转到上传页面...")

#跳转上传页面
driver.get('https://member.acfun.cn/upload-video')
upload_title = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[2]/div[2]/div/div/div[1]/textarea')
upload_title.send_keys(output)


#导入处理好的信息到页面指定xpath
type_radio = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[3]/div[2]/div[1]/div/div/label[1]/span[1]/input')
type_radio.click()
#select_info = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[4]/div[2]/div')
#select_info.send_keys('207')
tag_info = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[5]/div/div/div[2]/div[1]/div[2]/input')
tag_info.send_keys('AC娘录播')
tag_info.send_keys(Keys.ENTER)
upload_info = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[6]/div[2]/div/div/div/textarea')
upload_info.send_keys(simpletext)
#分区选择
area_select_1 = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[4]/div[2]/div/div')
area_select_1.click()
sleep(2)
area_select_2 = driver.find_element(By.XPATH,'/html/body/div[12]/div[1]/div[1]/div[1]/ul/li[1]')
area_select_2.click()
sleep(2)
area_select_3 = driver.find_element(By.XPATH,'/html/body/div[12]/div[1]/div[2]/div[1]/ul/li[5]')
area_select_3.click()

#处理截图
temp_dir = os.environ['TEMP']
random_integer = random.randint(1, 100000000)
screenshot_output = temp_dir + '\\' + str(random_integer) + '.jpg'
#screenshot_output = os.path.join(temp_dir, new_file_name_without_extension, '.jpg')
frame_number = 100 #指定帧
cap = cv2.VideoCapture(origin_file_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
if ret:
    # 保存图片
    cv2.imwrite(screenshot_output, frame)
    print(f'Screenshot saved to {screenshot_output}')
else:
    print('Failed to read the frame')
 
# 释放视频捕获对象
cap.release()
sleep(5)

#上传截图
photo_upload_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[1]/div[1]/div[1]/div/div') #此处可以定位到文件上传按钮，下一步执行点击。但需要调用系统文件选择器，所以无法直接使用。
photo_upload_button.click()
sleep(2)
upload(os.path.normpath(screenshot_output)) #调用前面的绝对路径，使用normpath方法自动替换为python可识别的路径
sleep(5)
photo_upload_button_conf = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[3]/div/button') #此处可以定位到文件上传按钮，下一步执行点击。但需要调用系统文件选择器，所以无法直接使用。
photo_upload_button_conf.click()
sleep(2)

#文件上传
upload_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/button') #此处可以定位到文件上传按钮，下一步执行点击。但需要调用系统文件选择器，所以无法直接使用。
upload_button.click()
sleep(2)
upload(os.path.normpath(origin_file_path)) #调用前面的绝对路径，使用normpath方法自动替换为python可识别的路径
sleep(5)
#upload_button.send_keys(origin_file_path)

#发布内容
release_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/form/div/div[14]')
release_button.click()


#print("\n按下任意键退出程序")
#msvcrt.getch()  # 等待任意键被按下
#print("\n程序已退出")
#os.system('pause') #调用cmd的按键退出
#os.system('read') #linux实现按键退出
