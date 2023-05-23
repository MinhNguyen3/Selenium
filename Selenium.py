from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time

global_configuration = "Tyson GFS4500 - GFE4500"
# global_configuration = "Michelangelo Desk GD45xx"

iteration = "Tyson|HH12"
# iteration = "PXA_B|B02"
chrome_options =  webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://rationalcld.dl.net/qm/web/console/HHS%20(Test)')
driver.maximize_window()
# Log in to Jazz
try:
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#jazz_ui_Dialog_0")))

    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_userId").send_keys('mnguyen3')
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_password").send_keys('D@talogic1')
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
    time.sleep(1)

    print("Log In")

except NoSuchElementException:
    print("Already Logged In")
    
time.sleep(20)

# Check Global Configuration and Change Global Configuration if not correct
current_gc = driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').text

if global_configuration not in current_gc :
    print("Incorrect Global Configuration")
    driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').click()
    driver.find_element(By.CSS_SELECTOR,'.switchButton.fauxButton').click()
    WebDriverWait(driver,30).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Configuration Picker']"))) 
    driver.find_element(By.XPATH,"//input[@placeholder='Type to search names or tags (enter * to show all)']").send_keys(global_configuration)
    time.sleep(2)
    # print("//span[contains(text(),'" + global_configuration + "')]")
    driver.find_element(By.XPATH,"//span[contains(text(),'" + global_configuration + "')]").click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
    time.sleep(30)

    current_gc = driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').text
    if global_configuration not in current_gc:
        print("Change Global Configuration Failed")
    else:
        print("Change Global Configuration Successful")

else:
    print("Correct Global Configuration")

# Move to TCER
# driver.switch_to.default_content()
driver.find_element(By.XPATH,"(//a[normalize-space()='Execution'])[1]").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR,"#jazz_ui_menu_MenuItem_0_text").click()

# time.sleep(15)
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//div[@aria-label='Show/Hide Table Inline Filters']"))) 
try:
    driver.find_element(By.XPATH,"//div[@title='Show Inline Filters']").click()
except NoSuchElementException:
    pass

time.sleep(20)

# Get column's text
columns = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']/thead/tr[2]/th")
index_dict1 = {}
for x in range(len(columns)):
    if columns[x].text == "":
        pass
    else:
        index_dict1[columns[x].text] = x


# Change Iteration ...
list1 = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']//thead//tr[@role='search']//th")


# print(index_dict1)

if iteration not in list1[index_dict1["Iteration"]].text :
    list1[index_dict1["Iteration"]].click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//td[normalize-space()='More...']").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,"input[dojoattachpoint='searchText']").send_keys(iteration)
    time.sleep(2)
    driver.find_element(By.XPATH,"//option[contains(text(),'" + iteration +"')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//button[contains(@class,'j-button-primary')]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,"button[title='Apply all filters']").click()
    time.sleep(30)

rows = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']/tbody/tr")
print(len(rows))

time.sleep(10)
for x in range(len(rows)):
    print(rows[x].find_element(By.XPATH,"./td[" + str(index_dict1["Test Case"] + 1) + "]").text)


print("FINISHED")
