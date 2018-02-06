#利用selenium搜索淘宝美食并存入mongodb
#1.搜索关键字 输入美食，并点击搜索
#2.分析页码并翻页
#3.分析商品提取内容
#4.存入mongodb
import re
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
#from config import *

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def get_final_number():
    try:
        browser.get("http://www.taobao.com")
        #判断是否加载成功
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        #按钮已经找到
        input.send_keys("美食")
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
        #网速过慢 得不到这个目标 得到错误
    except TimeoutException:
        return get_final_number()

def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_number)))
    except TimeoutException:
        return next_page(page_number)

def get_products():
    connect = pymysql.connect(host='localhost', db='financialdata', user='root', passwd='1234',charset='utf8')  
    #connect()方法用于创建与数据库的连接，里面可以指定参数，这一步只是连接到了数据库，操作数据库还需要下面的游标  
    cursor = connect.cursor()#通过获取到的conn数据库的cursor方法创建游标  
    #products = {}
    wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        price = float(re.compile(r'(\d+)').search(item.find(' .price').text()).group())
        deal = item.find(' .deal-cnt').text()
        title = item.find(' .title').text()
        shop = item.find(' .shop').text()
        location = item.find(' .location').text()
        sql = "INSERT INTO products (price, deal, title, shop, location) VALUES ( '%s', '%s', '%s', '%s', '%s')"
        data = (price, deal, title, shop, location)
        #print(product)
        cursor.execute(sql % data)
        connect.commit()
    #return product



if __name__ == "__main__":
 
    
    total = get_final_number()
    #total = float(re.compile(r'(\d+)').search(item.find(' .price').text()).group())
    for i in range(2, 20):
        next_page(i)
        product = get_products()





