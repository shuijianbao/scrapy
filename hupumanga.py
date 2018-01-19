from bs4 import BeautifulSoup
import requests
import time
from urllib.request import urlretrieve
url_list = []
img_list = []

if __name__ == "__main__":
    url = 'http://photo.hupu.com/nba/tag/%E6%BC%AB%E7%94%BB'
    head = {}
    head['User-Agent'] = "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"
    req = requests.get(url = url, headers = head)
    req.encoding = "utf-8"
    html = req.text
    bf = BeautifulSoup(html,'lxml')
    target_html = bf.find_all(class_ = "ku")
    for each in target_html:
        #print(each)
        url_list.append("http://photo.hupu.com/" + each.get('href'))
    for each in url_list:
        url = each
        head = {}
        head['User-Agent'] = "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"
        req = requests.get(url = url, headers = head)
        req.encoding = "gbk"
        html = req.text
        bf = BeautifulSoup(html,'lxml')
        target_html = bf.find_all("img")
        for each in target_html:
            if each.get("alt") and each.get("alt") != "图片":
                img_list.append(each.get("alt") + ":" + "http:"+str(each.get("src")))
    for each in img_list:

        img_info = each.split(":")
        filename = str(img_info[0]) + '.jpg'
        print("正在下载" + ":" + filename)
        img_url = img_info[1]+":"+img_info[2]
        urlretrieve(url = img_url,filename = 'images/' + filename)
        time.sleep(1)
    
    print("下载完成啦！")