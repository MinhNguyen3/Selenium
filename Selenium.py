from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time

global_configuration = "Tyson GFS4500 - GFE4500"
# global_configuration = "Michelangelo Desk GD45xx"


chrome_options =  webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://rationalcld.dl.net/qm/web/console/HHS%20(Test)')


try:
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#jazz_ui_Dialog_0")))

    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_userId").send_keys('mnguyen3')

    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_password").send_keys('D@talogic1')

    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

    print("Log In")

except NoSuchElementException:
    print("Already Logged In")
    

time.sleep(30)
driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').click()

# WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#jazz_ui_ResourceLink_0')))
time.sleep(10)
current_gc = driver.find_element(By.CSS_SELECTOR,'#jazz_ui_ResourceLink_0').text

if global_configuration not in current_gc :
    driver.find_element(By.CSS_SELECTOR,'.switchButton.fauxButton').click()
    
    WebDriverWait(driver,30).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Configuration Picker']"))) 

    driver.find_element(By.XPATH,"//input[@placeholder='Type to search names or tags (enter * to show all)']").send_keys(global_configuration)
    time.sleep(2)

    driver.find_element(By.XPATH,"//span[contains(text(),'" + global_configuration + "')]").click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
    time.sleep(2)

print("FINISHED")
