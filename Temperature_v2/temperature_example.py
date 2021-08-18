# Temperature
from selenium import webdriver                                  
from selenium.webdriver.chrome.options import Options                                                              
from selenium.webdriver.common.by import By                     
from selenium.webdriver.support.ui import WebDriverWait                                                            
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

apply_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span'
temperature_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
employID_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
name_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

import datetime
datetime_dt = datetime.datetime.today()
today = datetime_dt.strftime("%Y/%m/%d %H:%M")
url = "example"

retry_count = 0

def autofill(id):
    
    try:    
        options = Options()
        options.add_argument("--no-sandbox")                                                                               
        options.add_argument("--headless") 
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,apply_xpath)))

        #temperature
        generate_temp = str (random.randint(359, 362) / 10)
        driver.find_element_by_xpath(temperature_xpath).send_keys(generate_temp)
        time.sleep(1)

        #employID
        driver.find_element_by_xpath(employID_xpath).send_keys(id[0])
        time.sleep(1)

        #name
        driver.find_element_by_xpath(name_xpath).send_keys(id[1])
        time.sleep(1)
        
        #submit
        driver.find_element_by_xpath(apply_xpath).click()
        time.sleep(3)
        
        driver.quit()
        write_result(message="%s , Uploaded , temperature=%s" %(today,generate_temp))

    except TimeoutException:
        driver.quit()
        global retry_count
        retry_count += 1
        if retry_count > 1:
            print ("Write error log")
            write_result(message="%s , Failed , Unable to open the page" %today)
        else:
            print ("retry again")
            autofill(id=IdList)

def readID():
    with open("id_example.txt",'r',encoding='utf-8') as f:
        IDList = f.read().splitlines()
    return IDList

def write_result(message):
    print (message)
    with open("log.txt",'a+' , encoding='utf-8') as f:
        f.write('%s\n' %message)
        f.write('==============================================\n')

if __name__ == '__main__':
    IdList = readID()
    autofill(id=IdList)

    
    