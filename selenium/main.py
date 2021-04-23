import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

driver = webdriver.Chrome("/Users/mr.stark/Downloads/chromedriver")

driver.get("https://www.suning.com/")
# input = driver.find_element_by_id("searchKeywords")
# input.clear()
# input.send_keys("iphone")       # 输入文字
# input.send_keys(Keys.ENTER)     # 按下回车
# wait = WebDriverWait(driver, 10)
# # 设置显示等待时间为10秒直到某个ID、标签被加载
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'root990')))
# # 获取源代码
# print(driver.page_source)

time.sleep(10)       # 等待5秒
# 将进度条拉到最下面
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')