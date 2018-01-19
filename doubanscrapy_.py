from bs4 import BeautifulSoup
import re
import requests
import xlwt

def askUrl(url):
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'
    request = requests.get(url = url, headers = head)
    request.encoding ="utf-8"
    html = request.text
    return html

def get_msg():
    total_list = []
    name_list = []
    user_list = []
    tuijian_list = []
    title_list = []
    positive_list = []
    url_list = []
    comment_list = []
    page = input("请输入你要抓取的页数")
    page = int(page)
    for i in range(1,page+1):
        html = askUrl('https://movie.douban.com/review/best/?start='+str((i-1)*20))

        soup = BeautifulSoup(html,"lxml")
        #电影名字
        movie_name = soup.find_all('a',class_ = "subject-img")
        for each in movie_name:
        
            name_list.append(each.img.get("title"))
        #用户名名字
        reg = re.compile(r'<a href=.*?property="v:reviewer" class="name">(.*?)</a>',re.S)
        items = re.findall(reg, html)
        user_list.extend(items)
        #推荐名字
        tuijian = soup.find_all("header",class_ = "main-hd")
        for each in tuijian:
            tuijian_list.append(each.span.get("title"))
        #标题
        reg = re.compile(r'<div class="main-bd">.*?<a href=.*?>(.*?)</a>',re.S)
        items = re.findall(reg,html)
        title_list.extend(items)
        #积极
        reg = re.compile(r'<a href="javascript:;;".*?title="有用">.*?<span id=.*?>(.*?)</span>',re.S)
        items = re.findall(reg,html)
        for item in items:

            pattern = r'\d+'
            m = re.findall(pattern,item,re.S)
            positive_list.extend(m)
        #评论网址
        movie_comment = soup.find_all('div',class_= "main-bd")
        for each in movie_comment:
            url_list.append(each.a.get("href"))
        #评论内容
        for i in url_list:
            head = {}
            head['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'
            request = requests.get(url = i, headers = head)
            request.encoding = "utf-8"
            html = request.text
            soup = BeautifulSoup(html,"lxml")
            c = soup.find_all("div",id = "link-report")
            pattern = r"[\u4e00-\u9fa5]"
            items = re.findall(pattern,str(c))
            a = ""
            comment = a.join(items)
            comment_list.append(comment)
    total_list.extend([name_list,user_list,tuijian_list,title_list,positive_list,url_list,comment_list])
    return total_list,page

def saveData(savepath,total_list,page):
    book = xlwt.Workbook(encoding = "utf-8,style_compression = 0")
    sheet = book.add_sheet("豆瓣最受欢迎的影评",cell_overwrite_ok = True)
    col = ["电影名","用户名","推荐指数","评论标题","称赞数","评论网址","评论"]
    for i in range(0,7):
        sheet.write(0,i,col[i])
    for i in range(0,7):
        b = total_list[i]
        for j in range(0,page*10):
            sheet.write(j+1,i,b[j])
    book.save(savepath)
    print("finished")


if __name__ == "__main__":

    total_list,page = get_msg()
    
    savapath='/users/wangkaixi/desktop/doubanscrapy.xls'
    saveData(savapath,total_list,page)    