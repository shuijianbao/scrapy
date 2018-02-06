from selenium import webdriver
from bs4 import BeautifulSoup


def get_text():
    """
    获得基本网页报文
    """
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
    driver = webdriver.Chrome(chrome_options = options)
    driver.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html')
    nextpage1 = driver.find_element_by_css_selector("body > div.sf-edu-wenku-vw-container > div.sfa-body.day > div.sf-edu-wenku-id-container.wrap.xreader-container.reader-xreader > div.sf-edu-wenku-id-content.font-size-setting.fsz1 > div.content.singlePage.flodpage-clear-after > div.flod-wrap > div")
    nextpage1.click()
    html1 = driver.page_source
    nextpage2 = driver.find_element_by_css_selector("body > div > div.sfa-body.day > div.sf-edu-wenku-id-container.wrap.xreader-container.reader-xreader > div.sf-edu-wenku-id-pageNext.flod-pager")
    nextpage2.click()
    html2 = driver.page_source
    nextpage3 = driver.find_element_by_css_selector("body > div > div.sfa-body.day > div.sf-edu-wenku-id-container.wrap.xreader-container.reader-xreader > div.sf-edu-wenku-id-pageNext.flod-pager")
    nextpage3.click()
    html3 = driver.page_source
    driver.close()
    return html1,html2,html3

def text_fomation(html1,html2,html3):
     """
     返回具体文件内容
     """

    result_list = list()
    for item in [html1,html2,html3]:
        result = BeautifulSoup(item, 'lxml').find_all(class_ = 'sf-edu-wenku-id-content font-size-setting fsz1')
        bs = BeautifulSoup(str(result),'lxml')
        result_list.append(bs.text)

    return result_list


def conserve_file(result_list):
    """
    保存文件
    """
    with open("/users/wangkaixi/desktop/wenku2.txt",'w') as f:
        for i in result_list:
            f.write(i)


if __name__ == "__main__":
    html1,html2,html3 = get_text()
    result_list = text_fomation(html1,html2,html3)
    conserve_file(result_list)



