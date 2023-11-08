from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

search_no=["Modules","Packages","Classes and Interfaces","Members","Search Tags"]
no_num=[]
url='http://docs.oracle.com/en/java/javase/17/docs/api/'
search_text=input("입력창입니다. 입력하세요.")


service=Service(executable_path="./chromedriver")
options=webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])
driver=webdriver.Chrome(options=options, service=service)
driver.get(url)

def cookie(driver):
    time.sleep(5)
    iframe=driver.find_element(By.CLASS_NAME, value="truste_popframe")
    driver.switch_to.frame(iframe)
    cookie_element1=driver.find_element(By.CLASS_NAME, value="required") 
    cookie_element1.send_keys(Keys.ENTER)
    time.sleep(5)
    cookie_element2=driver.find_element(By.ID, value="gwt-debug-close_id") 
    cookie_element2.send_keys(Keys.ENTER)
    time.sleep(2)

def search1st(driver, word):
    input_element=driver.find_element(By.ID, value="search-input")
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys(word)
    time.sleep(3)

cookie(driver)

search1st(driver, search_text)

html=driver.page_source
soup=BeautifulSoup(html, 'lxml')

num=0
abnum=0
for child in soup.find_all('ul',{"id":"ui-id-1"}):
    for child1 in child.find_all('li'):
        num+=1
        abnum+=1
        if child1.get_text()==search_no[0] or child1.get_text()==search_no[1] or child1.get_text()==search_no[2] or child1.get_text()==search_no[3] or child1.get_text()==search_no[4]:
            no_num.append(abnum)
            print("Category : ",child1.get_text())
            num-=1
        else:
            print(num,": " ,child1.get_text())
        
select_word=int(input("원하시는 번호를 입력해주세요."))
for i in range(0,len(no_num)):
    if select_word>=no_num[i]:
        select_word-=1
time.sleep(1)

result=driver.find_elements(By.CLASS_NAME, value="result-item")
result[select_word+1].click()