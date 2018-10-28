from bs4 import BeautifulSoup
import requests as req
import urllib.request
import os

print('Hello!')
print(('My name is youngho'))
url = "https://www.naver.com"
html = req.get(url).text
print(html)
soup = BeautifulSoup(html, "html.parser")
a = soup.find_all('img')

filePath = 'e:/imagedown/'

for i,e in enumerate(a,1):
    print(i, e['src'])
    #urllib.request.urlretrieve(e['src'], os.path.join(filePath + str(i) + '.jpg'))
