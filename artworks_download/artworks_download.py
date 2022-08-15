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
    �������� �� �Ʒ����� ���� ��ũ��"""
    prev_height = driver.execute_script("return document.body.scrollHeight")


    while True:
        # ��ũ���� ȭ�� ���� �Ʒ��� ������
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        # ������ �ε� ���
        time.sleep(2)
    
        # ���� ���� ���̸� �����ͼ� ����
        curr_height = driver.execute_script("return document.body.scrollHeight")
    
        if(curr_height == prev_height):
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")




def search(artist):
    """
    ��Ƽ��Ʈ�� �˻��ϰ� �ش� ���������� �̵�"""
    search_screen = driver.find_element('xpath', '/html/body/div[4]/div[1]/div[2]/div/div/form/div/input[1]')
    search_screen.clear()
    search_screen.send_keys(artist + Keys.ENTER)
    driver.implicitly_wait(5)

    scroll_down()




def get_drawing_list():
    #drawing_list�� �׸��� ��� tag���� ��´�
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    drawing_list = soup.select('#sd-tab-image > div:nth-child(2) > div > div > div > a')

    return drawing_list

#folder ����
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")



# ==================================================================
# ============ ���� ==================
# ==================================================================

#artist ����
artists = []
print('artist�̸��� �Ѹ� ��Ȯ�� ������(full name)���� �Է�����')
print('������ �׳� enter ����')
while True:    
    name = input('���� �ٿ� �޾���?: ')

    if name == '':
        break
    artists.append(name)



#���� ����(artists) ����
main_path = Tk()
main_path.withdraw()
main_path.dirName = filedialog.askdirectory()
createDirectory(main_path.dirName + '\\artists')

for artist in artists:
    #artist�� artwork�� ���� ���� ����
    createDirectory(main_path.dirName + '\\artists\\' + artist)

    #�ش� ������Ʈ ����
    url = 'https://commons.wikimedia.org/wiki/Main_Page'
    driver = webdriver.Chrome('C:\\Users\\User\\Desktop\\chromedriver_win32\\chromedriver')
    driver.get(url)
    driver.implicitly_wait(5)
    
    #url artist��ǰ �˻��ϱ�, �׸��� �׸� url�� ���� list�����
    search(artist+ ' artwork')
    drawing_list = get_drawing_list()
    nums = len(drawing_list)

    for drawing in drawing_list:
        try:
            #�׸��� ������ ������� url�� ����
            drawing_url = drawing['href']
            driver.get(drawing_url)
            driver.implicitly_wait(5)
            
            #download������ img_site�� ����
            #���迡 title��
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select('head > title')[0].text   
            title = title.replace('File:', '')
            title = title.replace(' - Wikimedia Commons', '')
            title = title.strip()
            
            img_site_url = soup.select('#file > a')[0]['href']
            driver.get(img_site_url)
            
            #img_site���� src ����
            #����: src���� urllib �̿��ؼ� �׸��ٿ�ε�
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            img_src = soup.select('img')[0]['src']
            
            urllib.request.urlretrieve(img_src, main_path.dirName + '\\artists\\' + artist + '\\'+ title)

        except:
            pass

    driver.close()

    print(f'{artist}�� ��ǰ �� {nums}�� �ٿ�ε� �Ϸ��߽��ϴ�')


  
