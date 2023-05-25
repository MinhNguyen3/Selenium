from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import sys
try:
    import pandas as pd
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    import pandas as pd
import os

userID = 'mnguyen3'
password =  'D@talogic1'

global_configuration = "Tyson GFS4500 - GFE4500"
# global_configuration = "Michelangelo Desk GD45xx"

# iteration = "Tyson|HH12"
# iteration = "PXA_B|B02"


## GET INFORMATION FROM EXCEL
file_content = pd.read_excel(os.getcwd() + "\\Result.xlsx")
# Get Iteration
excel_iteration = []
for x in file_content['Iteration']:
    if x not in excel_iteration:
        excel_iteration.append(x)
iteration = excel_iteration[0]
print(iteration)

# Get Test Plan ID
# excel_planID = []
# for x in file_content['Test Plan ID']:
#     if x not in excel_planID:
#         excel_planID.append(x)
# planID = int(excel_planID[0])
# print(planID)

# Get Owner
# excel_owner = []
# for x in file_content['Owner']:
#     if x not in excel_owner:
#         excel_owner.append(x)
# owner = excel_owner[0]
# print(owner)

# Get TC Name and Result of that TC
result_dict = {}
for x in file_content["Name"]:
    pandas_index = file_content[file_content["Name"] == x].index.to_numpy()
    result_dict[x] = file_content["Last Result"][int(pandas_index)]


## OPEN JAZZ
chrome_options =  webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://rationalcld.dl.net/qm/web/console/HHS%20(Test)')
driver.maximize_window()

## LOG IN TO JAZZ
try:
    # Wait until log in dialog is displayed
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#jazz_ui_Dialog_0")))
    # User ID
    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_userId").send_keys(userID)
    time.sleep(1)
    # Password
    driver.find_element(By.CSS_SELECTOR,"#jazz_app_internal_LoginWidget_0_password").send_keys(password)
    time.sleep(1)
    # Submit
    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
    time.sleep(1)

    print("Log In")

except NoSuchElementException:
    print("Already Logged In")
    


## CHECK GLOBAL CONFIGURATION
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.configurationUiNode.hideLink')))
time.sleep(5)
current_gc = driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').text
# Change Global Configuration if not correct
if global_configuration not in current_gc :
    print("Incorrect Global Configuration")
    driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').click()
    driver.find_element(By.CSS_SELECTOR,'.switchButton.fauxButton').click()

    WebDriverWait(driver,30).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Configuration Picker']"))) 
    driver.find_element(By.XPATH,"//input[@placeholder='Type to search names or tags (enter * to show all)']").send_keys(global_configuration)
    time.sleep(2)
    driver.find_element(By.XPATH,"//span[contains(text(),'" + global_configuration + "')]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
    time.sleep(30)

    # Check Global Configuration again
    current_gc = driver.find_element(By.CSS_SELECTOR,'.configurationUiNode.hideLink').text
    if global_configuration not in current_gc:
        print("Change Global Configuration Failed")
    else:
        print("Change Global Configuration Successful")

else:
    print("Correct Global Configuration")



## MOVE TO TCER AND CLEAR ALL FILTERS
# Move to TCER
driver.find_element(By.XPATH,"(//a[normalize-space()='Execution'])[1]").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR,"#jazz_ui_menu_MenuItem_0_text").click()

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//div[@aria-label='Show/Hide Table Inline Filters']"))) 
try:
    driver.find_element(By.XPATH,"//div[@title='Show Inline Filters']").click()
except NoSuchElementException:
    pass

# Clear all filters
time.sleep(30)
driver.find_element(By.XPATH,"//a[@title='Clear all filters']").click()
time.sleep(5)



## GET COLUMN NAME AND ITS INDEX
columns = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']/thead/tr[2]/th")
columns_index= {}
for x in range(len(columns)):
    if columns[x].text == "":
        pass
    else:
        columns_index[columns[x].text] = x



## CHANGE ITERATION
list1 = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']//thead//tr[@role='search']//th")

if iteration not in list1[columns_index["Iteration"]].text :
    list1[columns_index["Iteration"]].click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//td[normalize-space()='More...']").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,"input[dojoattachpoint='searchText']").send_keys(iteration)
    time.sleep(2)
    driver.find_element(By.XPATH,"//option[contains(text(),'" + iteration +"')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//button[contains(@class,'j-button-primary')]").click()
    time.sleep(1)


# CHANGE OWNER TO CURRENT USER
# Open Owner Dialog
list1[columns_index["Owner"]].click()
time.sleep(5)

# Uncheck all
owner_list = driver.find_elements(By.XPATH,"//tr[@aria-checked='true']")
for x in owner_list:
    driver.execute_script("arguments[0].click();", x)
time.sleep(5)

# Select Current User
driver.find_element(By.XPATH,"//td[normalize-space()='Current User']").click()

# #==========================Change Test Plan==========================
# list1[columns_index["Test Plan"]].click()
# time.sleep(5)
# test_plan_list = driver.find_elements(By.XPATH,"//table[@summary='This is Test Plans table']/tbody//input[@aria-checked='true']")
# for x in test_plan_list:
#     driver.execute_script("arguments[0].click();", x)
# driver.find_element(By.XPATH,"//input[@title='Type filter text or ID']").send_keys(planID)
# time.sleep(1)
# driver.find_element(By.XPATH,"//span[@class='filter-area filter-area-inline-selector']//button[@title='Filter']").click()
# time.sleep(5)
# driver.find_element(By.XPATH,"//input[contains(@aria-label,'" + str(planID) + "')]").click()
# time.sleep(1)

# Filter TCER
driver.find_element(By.CSS_SELECTOR,"button[title='Apply all filters']").click()
time.sleep(30)

## SELECT TEST CASES
rows = driver.find_elements(By.XPATH,"//table[@class='content-table font-setting-default']/tbody/tr")

time.sleep(10)
for x in range(len(rows)):
    TC_Jazz = rows[x].find_element(By.XPATH,"./td[" + str(columns_index["Name"] + 1) + "]").text
    try:
        if result_dict[TC_Jazz] == "Passed":
            checkbox = rows[x].find_element(By.XPATH,"./td[1]//input")

            actionChains = ActionChains(driver)
            actionChains.move_to_element(checkbox).scroll_by_amount(0,50).perform()

            time.sleep(0.25)
            checkbox.click()
    except:
        pass


print("FINISHED")
