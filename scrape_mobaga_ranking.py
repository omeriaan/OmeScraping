# coding=utf-8

##
# selenium + phantomJS + beautifulSoupでスクレイピング
##

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

phantomjsPath = '/usr/local/bin/phantomjs'
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'

driver = webdriver.PhantomJS(executable_path=phantomjsPath
                             ,desired_capabilities={'phantomjs.page.settings.userAgent':USER_AGENT})
url = 'http://sp.mbga.jp/_game_ranking?genre=2000&sex_type=A&p=1&from_func=game_ranking&from_sex_type=A&from_genre=1000'
driver.get(url)

data = driver.page_source.encode('utf-8')

html = BeautifulSoup(data, 'html.parser')
title_list = html.find_all('span', class_='rankContentTitle caption_l')

print(title_list)  # htmlソースを表示する

# driver.save_screenshot('ss.png')
driver.quit()
