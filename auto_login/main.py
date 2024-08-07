from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time 
import pyautogui
import pyperclip

import auth 
# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

iris_driver = webdriver.Chrome(options=chrome_options)
iris_driver.get("https://iris.dongkuk.com/")

id = iris_driver.find_element(By.CSS_SELECTOR, "#idtemp")
id.click()
pyperclip.copy("kyungbong.lee")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

pw = iris_driver.find_element(By.CSS_SELECTOR, "#passwordtemp")
pw.click()
pyperclip.copy("Dlrudqhd00@")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

login_bt = iris_driver.find_element(By.CSS_SELECTOR, "#frm > section > section > article.loginBox > div > div:nth-child(4) > a")
login_bt.click()
time.sleep(10)


# 2차인증 
auth_bt = iris_driver.find_element(By.CSS_SELECTOR, "#privateEmailButton")
auth_bt.click()
time.sleep(5)

# 이메일 내용 크롤링
auth_num = auth.getAuthNumber("rudqhd05193@gmail.com", "qncl mviv vieh ionv", "no_reply@worksmobile.com")
# 인증번호 입력 
pw2 = iris_driver.find_element(By.CSS_SELECTOR, "#number1")
pw2.click()
pyperclip.copy(auth_num)
pyautogui.hotkey("ctrl", "v")
time.sleep(2)
