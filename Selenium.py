from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome(executable_path='path/to/chromedriver')

# driver.get('https://www.google.com')
# search_box = driver.find_element(By.CSS_SELECTOR,".ly0Ckb")
# # search_box.send_keys('python')
# search_box.click()

# time.sleep(5000)


driver.get('https://rationalcld.dl.net/ccm/')
time.sleep(2)

search_box = driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_userId")
search_box.send_keys('mnguyen3')

search_box = driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_password")
search_box.send_keys('D@talogic1')

search_box = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
search_box.click()
time.sleep(30)