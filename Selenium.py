from selenium import webdriver
driver = webdriver.Chrome(executable_path='path/to/chromedriver')

driver.get('https://www.google.com')
search_box = driver.find_element_by_name('q')
search_box.send_keys('python')
search_box.submit()