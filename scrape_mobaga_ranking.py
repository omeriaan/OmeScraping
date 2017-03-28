# coding=utf-8

"""
■ selenium + phantomJS + beautifulSoupでMobagaランキングをスクレイピング

"""

import sys
import time
import scrape_const as Const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def main():

    html = Fetch()

    rankList = html.find_all('li', class_='line0')

    # print(rankList)  # htmlソースを表示する

    for rankElement in rankList:
        rankNum = rankElement.find('div', class_='rankRibbon').text.replace('位', '')
        gameTitle  = rankElement.find('span', class_='rankContentTitle caption_l').text
        print(rankNum, gameTitle)


def Fetch():
    """
    PhantomJSで仮想ブラウザを生成し、BeautifulSoupでパース
    :return: str型HTML
    """

    # options = webdriver.ChromeOptions()
    # options.add_argument('--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 " \
    #          "(KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"')
    # driver = webdriver.Chrome(executable_path = '/Users/tennessee-rose/Documents/chromedriver'
    #                              , chrome_options=options)
    driver = webdriver.PhantomJS(executable_path=GetPhantomjsPath()
                                , desired_capabilities={'phantomjs.page.settings.userAgent': Const.USER_AGENT})
    wait = WebDriverWait(driver, 30)
    url = 'http://sp.mbga.jp/_game_ranking?genre=2000&sex_type=A&p=1&from_func=game_ranking&from_sex_type=A&from_genre=1000'
    driver.get(url)

    print('ページ取得中')
    # ページが読み込まれるまで待機
    wait.until(EC.presence_of_all_elements_located)
    print('ページ取得完了')

    # 30位まで取得するため、「もっと見る」ボタンを押下する
    driver.find_element_by_class_name('sp-more-load').click()

    time.sleep(5)

    # wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'sp-more-load')))

    pageData = driver.page_source.encode('utf-8')

    html = BeautifulSoup(pageData, 'html.parser')
    print(html)

    driver.save_screenshot('ss.png')

    driver.quit()
    return html

def Scrape():
    return

def GetPhantomjsPath():
    phantomjsPath = ''

    # Macの場合
    if sys.platform == 'darwin':
        phantomjsPath = Const.PhantomJSPath_Mac
    # Windowsの
    elif sys.platform == 'win32':
        phantomjsPath = Const.PhantomJSPath_Windows

    if phantomjsPath == '':
        print("そのOSは対応してないっす〜")
        sys.exit()

    return phantomjsPath

if __name__ == '__main__':
    main()