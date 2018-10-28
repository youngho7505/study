import requests, operator, pandas, glob2
from bs4 import BeautifulSoup
from datetime import datetime

def Crawling(srcWord, pageCount):

    now = datetime.now()
    l = []

    for page in range(1, int(pageCount)+1):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

        param = {
            'query':srcWord,
            'where':'news',
            'start':(page-1)*10+1
        }

        r = requests.get("https://search.naver.com/search.naver", params= param, headers = headers)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        #print(soup.prettify())
        ul = soup.find("div",{"class":"_prs_nws"}).find("ul",{"class":"type01"})
        li = ul.find_all("li")

        for news in li:
            d = {} #데이터 저장을 위한 딕셔너리 선언

            try:
                title = news.find("dl").find("dt").find("a")['title']
                links = news.find("dl").find("dt").find("a")['href']
                d["title"] = title
                d["links"] = links
            except:
                d["title"] = "None"
                d["links"] = "None"

            try:
                imgSrc = news.find("div",{"class":"thumb"}).find("a").find("img")['src']
                d["imgSrc"] = imgSrc
            except:
                d["imgSrc"] = "None"

            try:
                desk = news.find("dl").find("dd",{"class":"txt_inline"}).find("span",{"class":"_sp_each_source"}).text
                d['desk'] = desk
            except:
                d['desk'] = "None"

            l.append(d)

    df = pandas.DataFrame(l) #pandas의 데이터프레임에 리스트(l)를 추가함
    df.to_csv("%s-%s-%s-%s-%s-%s.csv" % (now.year, now.month, now.day, now.hour, now.minute, now.second))
    print("Data saved successfully!")


def loadFile(fileName):
    pass

#메인 셋팅함수, 사용자로부터 값을 입력받아 함수 호출
def mainSetting():
    while(1):
        kb = input("$ ")
        if kb == "exit":
            break
        elif kb == "crawling":
            srcWord = input("Enter Search Word : ")
            pageCount = input("Enter PageCount : ")
            Crawling(srcWord, pageCount)
        elif kb == "loadAll":
            loadFile("all")
        elif kb == "load":
            fileName = imput("Enter CSV FileName : ")
            loadFile(fileName)
        else:
            print("Error Command!")

mainSetting()
