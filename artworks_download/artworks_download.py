# -*- coding: cp949 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os
import urllib.request
from tkinter import filedialog
from tkinter import *

def scroll_down():
    """
    웹페이지 맨 아래까지 무한 스크롤"""
    prev_height = driver.execute_script("return document.body.scrollHeight")


    while True:
        # 스크롤을 화면 가장 아래로 내린다
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        # 페이지 로딩 대기
        time.sleep(2)
    
        # 현재 문서 높이를 가져와서 저장
        curr_height = driver.execute_script("return document.body.scrollHeight")
    
        if(curr_height == prev_height):
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")




def search(artist):
    """
    아티스트를 검색하고 해당 웹페이지로 이동"""
    search_screen = driver.find_element('xpath', '/html/body/div[4]/div[1]/div[2]/div/div/form/div/input[1]')
    search_screen.clear()
    search_screen.send_keys(artist + Keys.ENTER)
    driver.implicitly_wait(5)

    scroll_down()




def get_drawing_list():
    #drawing_list에 그림이 담긴 tag들을 담는다
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    drawing_list = soup.select('#sd-tab-image > div:nth-child(2) > div > div > div > a')

    return drawing_list

#folder 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")



# ==================================================================
# ============ 실행 ==================
# ==================================================================

#artist 설정
artists = []
print('artist이름을 한명씩 정확한 영문명(full name)으로 입력해줘')
print('없으면 그냥 enter 눌러')
while True:    
    name = input('누구 다운 받아줘?: ')

    if name == '':
        break
    artists.append(name)



#담을 폴더(artists) 생성
main_path = Tk()
main_path.withdraw()
main_path.dirName = filedialog.askdirectory()
createDirectory(main_path.dirName + '\\artists')

for artist in artists:
    #artist의 artwork를 담을 폴더 생성
    createDirectory(main_path.dirName + '\\artists\\' + artist)

    #해당 웹사이트 들어가기
    url = 'https://commons.wikimedia.org/wiki/Main_Page'
    driver = webdriver.Chrome('C:\\Users\\User\\Desktop\\chromedriver_win32\\chromedriver')
    driver.get(url)
    driver.implicitly_wait(5)
    
    #url artist작품 검색하기, 그리고 그림 url들 담은 list만들기
    search(artist+ ' artwork')
    drawing_list = get_drawing_list()
    nums = len(drawing_list)

    for drawing in drawing_list:
        try:
            #그림의 설명을 적어놓은 url로 들어간다
            drawing_url = drawing['href']
            driver.get(drawing_url)
            driver.implicitly_wait(5)
            
            #download가능한 img_site로 들어가기
            #간김에 title도
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select('head > title')[0].text   
            title = title.replace('File:', '')
            title = title.replace(' - Wikimedia Commons', '')
            title = title.strip()
            
            img_site_url = soup.select('#file > a')[0]['href']
            driver.get(img_site_url)
            
            #img_site에서 src 따기
            #이유: src에서 urllib 이용해서 그림다운로드
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            img_src = soup.select('img')[0]['src']
            
            urllib.request.urlretrieve(img_src, main_path.dirName + '\\artists\\' + artist + '\\'+ title)

        except:
            pass

    driver.close()

    print(f'{artist}의 작품 총 {nums}개 다운로드 완료했습니다')


  
