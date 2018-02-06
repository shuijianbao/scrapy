from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib

def main():
    html = urlopen("http://tieba.baidu.com/p/5304937633")
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.find_all('img',class_ = 'BDE_Image') 
    x = 0
    for link in imgs:
        url = link.get('src')
        filesavepath  = '/Users/wangkaixi/Desktop/picture/%s.jpg'
        urllib.request.urlretrieve(url,filesavepath % x)
        x+=1

if __name__ == "__main__":
    main()