# from django.test import selenium
import selenium
import csv

from django.http import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

# pip install webdriver-manager
# ui_report_writer.writerow(['Criteria', 'Pass'])

#BlackBox Testing of Application
class TestSel:
    with open('UITest_file.csv', mode='w') as ui_report:
        ui_report_writer = csv.writer(ui_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        driver = webdriver.Chrome(ChromeDriverManager().install()) #Automatically Take the Chrome WebDriver
        driver.implicitly_wait(30)
        driver.maximize_window()
        # Navigate to the application home page
        driver.get(" http://127.0.0.1:8000/")
        print("Browser Initiated")
        ui_report_writer.writerow(['Browser Started', 'Pass'])
        ui_report_writer.writerow(['Goto to http://127.0.0.1:8000/ ', 'Pass'])

        ui_report_writer.writerow(['Test For :-  ', 'ADMINISTRATOR'])

        driver.find_element_by_name('username').send_keys('admin')
        driver.implicitly_wait(100)
        driver.find_element_by_name('password').send_keys('admin')
        driver.implicitly_wait(100)
        driver.find_element_by_name('submit').send_keys(Keys.RETURN)
        driver.implicitly_wait(100)
        ui_report_writer.writerow(['Login', 'Pass'])
        print('Logged in as Administrator')

        link = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul[1]/li[3]/a')
        link.click()
        rows_count_int = driver.execute_script("return document.getElementsByTagName('tr').length")
        print (rows_count_int)
        link = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul[1]/li[1]/a')
        link.click()
        ui_report_writer.writerow(['Click on Link - Create Employee', 'Pass'])
        print('pass')
        driver.find_element_by_name('first_name').send_keys('Test1')
        driver.find_element_by_name('last_name').send_keys('Data1')
        driver.find_element_by_name('uname').send_keys('useraccount1')
        driver.find_element_by_name('password').send_keys('1234567890')
        #driver.find_element_by_name('first_name').send_keys('Test')
        select = Select(driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div/div[2]/form/div[2]/div[2]/select'))
        select.select_by_index(2)
        driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/button[1]').send_keys(Keys.RETURN)
        ui_report_writer.writerow(['Create Employee Link', 'Pass'])
        print('pass')
        link = driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div[2]/a[1]')
        link.click()
        ui_report_writer.writerow(['Edit Employee Link Works? ', 'Pass'])
        link = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul[1]/li[3]/a')
        link.click()
        rows_count_later = driver.execute_script("return document.getElementsByTagName('tr').length")
        if(rows_count_int<rows_count_later):
            ui_report_writer.writerow(['Create Employee Function', 'Pass'])
            print(rows_count_later)
            print("New Employee Created")

        link= driver.find_element_by_xpath('/html/body/div/nav/div/div/ul[2]/li[2]/a')
        link.click()

        driver.quit()
        ui_report_writer.writerow(['File Close', 'Pass'])