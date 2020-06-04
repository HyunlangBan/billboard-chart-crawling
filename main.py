from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import csv
import math
import time

# 순위, 곡, 아티스트 정보
chrome_path = "/usr/bin/chromedriver"
driver = webdriver.Chrome(chrome_path)
driver.implicitly_wait(3)

api_url = 'https://www.billboard.com/charts/hot-100'

driver.get(api_url)
# 화면 띄우기

# Scroll Down
SCROLL = driver.execute_script("return window.innerHeight")
HEIGHT = driver.execute_script("return document.body.scrollHeight")
num = math.ceil(HEIGHT/SCROLL)
scroll = SCROLL
start = 0
for i in range(num+1):
    driver.execute_script("window.scrollTo("+str(start)+","+str(scroll)+")")
    # 문자끼리 더해야하기 때문에 start, scroll을 str으로 변환해야한다.
    start += SCROLL
    scroll+= SCROLL
    time.sleep(1)

response = driver.page_source
# request.get으로 가져오는게 아니라 스크롤링하면서 띄워놓은 현재의 source를 가져와야하기 때문에 driver.page_source를 가져와야한다.

csv_filename = "billboard.csv"

csv_open = open(csv_filename, 'w+', encoding='UTF-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow(('Rank','Title','Singer', 'Image Link'))

bs = BeautifulSoup(response, 'html.parser')

elements = bs.find_all('li', {'class': 'chart-list__element display--flex'})
#print(elements.prettify())

# 각 row 저장
for element in elements:
    rank_elem = element.find('span', {'class':'chart-element__rank__number'})
    rank = rank_elem.text
    #print(f'rank: {rank}')

    song_elem = element.find('span', {'class':'chart-element__information__song text--truncate color--primary'})
    song = song_elem.text
    #print(f'song: {song}')

    artist_elem = element.find('span', {'class':'chart-element__information__artist text--truncate color--secondary'})
    artist = artist_elem.text
    #print(f'artist: {artist}')

    # 어려웠던 부분: 이미지 크롤링하기
    # 이미지가 스크롤에 따라 동적으로 로딩되서 동일한 방식으로 했더니 실패함(맨 윗 부분만 데이터가 있었음) --> 셀레늄 써야됨
    img_elem = element.find('span', {'class': 'chart-element__image flex--no-shrink'})
    img_elem = str(img_elem)
    # str으로 안바꾸면 find_all 할 수 없다고 오류남!(expected string or bytes-like object)
    # img_elem['style']로 attribute의 value를 가져올수도 있다.

    p=re.compile('http\S+jpg')
    img_link = p.findall(img_elem)
    img_link = img_link[0]
    # indexing을 해주어야 따옴표없이 예쁘게 값이 나온다.

    # print(f'img_link: {img_link}')
    img = img_link

    csv_writer.writerow([rank, song, artist, img])

csv_open.close()
