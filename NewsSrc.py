from bs4 import BeautifulSoup
import requests
import sys
import io
from collections import OrderedDict
from itertools import count

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def naverNewsSrc_cralwler(src_word, max_page):
    url = "https://search.naver.com/search.naver"
    post_dict = OrderedDict() #OrderedDict를 사용하며, key에 url을 넣겠습니다.
                              #url은 유일성이기 때문에!
    f = open('e:/imagedown/뉴스검색결과.txt', 'wt', encoding='utf-8')
    i = 1
    for page in count(1): #1부터 무한대로 시작(break or return이 나올때까지)
        param = {
            'query':src_word,
            'where':'news',
            'start':(page-1)*10+1
        }
        response = requests.get(url, params = param)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        titleList = soup.select("._sp_each_title")
        #print(titleList)

        for srcList in titleList:
            if max_page and (page > max_page):
                return post_dict
            if srcList['href'] in post_dict: #지금 저장할 링크(key)가 이미 post_dict에 있다면
                return post_dict #리턴해서 끝내버린다.
            print(i, srcList.text, srcList['href'])
            f.write(str(i) + ' ' + srcList.text + ' - ' + srcList['href'] + '\n')
            post_dict[srcList['href']] = srcList.Text
            i += 1

    return post_dict
    f.close()

#실행
if __name__ == '__main__':
    naverNewsSrc_cralwler('류현진', 5)
