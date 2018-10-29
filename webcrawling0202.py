import requests, operator, pandas, glob2
from bs4 import BeautifulSoup
from datetime import datetime

#크롤링 함수(단어와 페이지 수를 받아와 그 단어를 크롤링 해오는 함수)
def Crawling(srcWord, pageCount):

    #현재 시간을 now라는 변수에 저장
    now = datetime.now()
    l = []

    #페이지 수는 1부터 사용자가 입력한 페이지 수까지가 됨
    for page in range(1, int(pageCount)+1):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

        param = {
            'query':srcWord,
            'where':'news',
            'start':(page-1)*10+1
        }

        #동적으로 입력한 단어의 뉴스 페이지에 접속
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

            l.append(d) #리스트에 사전 추가 / 한 행마다 사전에 추가

    df = pandas.DataFrame(l) #pandas의 데이터프레임에 리스트(l)를 추가함

    # 타이틀 값이 None인 행들을 삭제
    df = df[df.title != 'None']

    df.to_csv("%s-%s-%s-%s-%s-%s.csv" % (now.year, now.month, now.day, now.hour, now.minute, now.second))
    print("Data saved successfully!")


def loadFile(fileName):
    #checkFileName이라는 함수를 호출, 파일이 존재하는지의 여부를 확인
    oupputFileName = checkFileName(fileName)
    if oupputFileName != -1:
        df = pandas.read_csv(oupputFileName)
        title = df['title']
        desk = df['desk']
        links = df['links']
        print(title)

# checkFileName 함수
# 사용자가 입력한 파일이 존재하지 않을 시 -1을 리턴, 존재 시 파일명 리턴
# 사용자가 입력한 값이 all이면 같은 경로의 모든 csv 파일을 하나로 합치고, csv 파일을 만듬.
# 그리고 만들어진 csv 파일명을 리턴
def checkFileName(fileName):

    now =datetime.now()
    if len(glob2.glob("*.csv")) == 0:
        print("No file found in this directory!")
        return -1
    else:
        if fileName == "all":
            result = []

            for i in glob2.glob("*.csv"):
                result.append(pandas.read_csv(i))

            outputFileName = "%s-%s-%s-%s-%s-%s- merge.csv" \
                             % (now.year, now.month, now.day, now.hour, now.minute, now.second)

            #list에 저장한 csv파일들을 resultDf에 저장
            resultDf = pandas.concat(result, ignore_index= True)
            resultDf.to_csv(outputFileName, encoding= 'utf-8')
            return outputFileName
        else:
            return fileName



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
            fileName = input("Enter CSV FileName : ")
            loadFile(fileName)
        else:
            print("Error Command!")

mainSetting()
