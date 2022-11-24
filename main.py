import requests
from bs4 import BeautifulSoup
import re
import random
import time
from urllib.parse import quote
from tqdm import tqdm, trange
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
import sys
import pandas as pd
import re

import os,os.path

chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

def get_todate():
    return date.today()

def selenium_get_detail_twinc(url):
    print('目前爬取頁面是：' + url)
    driver.get(url)
    save = driver.page_source

    soup = BeautifulSoup(save, "html.parser")

    return soup

def selenium_get_content_twinc(url):
    print('目前爬取頁面是：' + url)
    driver.get(url)
    save = driver.page_source

    soup = BeautifulSoup(save, "html.parser")
    url = soup.select('table', {'class': 'table table-striped'})[1]
    return url

def selenium_get_Code_twinc(url):
    print('目前爬取頁面是：' + url)
    driver.get(url)
    save = driver.page_source
    
    soup = BeautifulSoup(save, "html.parser")
    url = soup.select('table', {'class': 'table table-striped'})[1]
    return url


def selenium_get_Code_104(url):
    print('目前爬取頁面是：' + url)
    driver.get(url)
    save = driver.page_source

    soup = BeautifulSoup(save, "html.parser")
    page = soup.select('.pagination__count')[0].text
    page = page.lstrip(' 共 ').rstrip(' 頁 ')
    return page

def read_url(url):
    USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]
    USER_AGENT = random.choice(USER_AGENT_LIST)
    headers = {'user-agent': USER_AGENT}
    #s = requests.Session()
    #req = s.get(url, headers = headers)
    driver.get(url)
    save = driver.page_source
    soup = BeautifulSoup(save, "html.parser")
    return soup

def is_address(address):
    regex = re.compile(r'(?P<縣市>\D+?[縣市])?(?P<號>\d+號)')
    match = regex.search(address)

    if match:
        return match.groupdict()
    else:
        return ""

def find_title_104(key_txt, start, end):
    #路徑組合
    today = get_todate()
    path_csv = "%s" % os.getcwd() + '/' + 'companies/'
    if not os.path.isdir('companies'): # 確認是否有companies資料夾  沒有則返回Ture
        os.mkdir('companies') # 建立companies資料夾

    key = quote(key_txt)
    #
    find_page_url = 'https://www.104.com.tw/company/search/?keyword={0}&jobsource=cs_custlist&mode=s&page=1'.format(key)
    get_sum_page = int(selenium_get_Code_104(find_page_url))
    print('共有：' + str(get_sum_page) + ' 頁')

    companies = []


    for i in tqdm(range(1, get_sum_page+1)):  #set page 1 to find all max page ,tqdm讀取進度條
        if start != 0 and i < start:
            continue
        if end != 0 and i > end:
            continue
        url = 'https://www.104.com.tw/company/search/?keyword={0}&jobsource=cs_custlist&mode=s&page={1}'.format(key, i) 
        #time.sleep(random.randint(2,10)) #隨機等待
        soup = read_url(url) #讀取網頁
        print('目前爬取頁面是：' + url)
        for title_1 in soup.select('.info-job__text'):
            #公司名
            company_name = title_1.text

            tw_url = 'https://www.twincn.com/Lq.aspx?q={0}'.format(quote(company_name))
            content = selenium_get_Code_twinc(tw_url) #讀取網頁

            for cont in content.find_all('a'):

                if cont.text != company_name:
                    continue

                # 用統編查詢
                detail_url = 'https://www.twincn.com{0}'.format(cont['href'])

                # cont['href'] in companies['統一編號（統編）']
                if len(companies) > 0:
                    if any(obj['url'] == detail_url for obj in companies):
                        continue

                details = selenium_get_detail_twinc(detail_url)

                details_header = details.findAll('p', {'class': 'lead'})
                details_table = details.findAll('table', {'id': 'basic-data'})[0]

                detail_p = details_header[0]
                # split values inside <p> with <br/> tag
                detail_p = detail_p.findAll('br')
                # get previous sibling of <br/> tag
                detail_texts = [x.previous_sibling for x in detail_p]

                # remove all \n and \t in list detail_texts
                detail_texts = [x.replace('\n', '').strip() for x in detail_texts]

                company = {}

                detail_data = '|'.join(detail_texts)
                basic = detail_data

                #公司地址
                table_MN = pd.read_html(str(details_table))
                df = table_MN[0]

                # 統一編號（統編）
                invoicd_id = ""
                # 公司地址
                company_address = ""
                # 股票代號
                stock_code = ""
                # 代表人姓名
                representative_name = ""
                # 網址
                company_url = ""
                # mail
                company_mail = ""
                # 公司狀況
                company_status = ""
                # 資本總額(元)
                capital_total = ""
                # 實收資本額(元)
                real_capital_total = ""
                mail = ""
                # email
                tel = ""
                fax = ""
                tax = ""
    
                

                for text in detail_texts:
                    if is_address(text):
                        company_address = text
                    if text.startswith('電話'):
                        tel = text.split(':')[1]
                    if text.startswith('傳真'):
                        fax = text.split(':')[1]
                    if text.startswith('股票代號'):
                        stock_code = text.split(' ')[1]
                    if text.startswith('(稅籍狀態:'):
                        tax = text.split(':')[1].rstrip(')')
                    if text.startswith('統編'):
                        invoicd_id = text.split(' ')[1]


                for i in df.index:
                    if df[0][i] == '統一編號（統編）':
                        invoicd_id = df[1][i]

                    if df[0][i] == '公司地址':
                        company_address = df[1][i]

                    if df[0][i] == '股票代號':
                        stock_code = df[1][i]
                    
                    if df[0][i] == '代表人姓名':
                        representative_name = df[1][i]

                    if df[0][i] == '網址':
                        company_url = df[1][i]
                    
                    if df[0][i] == 'mail':
                        company_mail = df[1][i]

                    if df[0][i] == '公司狀況':
                        company_status = df[1][i]

                    if df[0][i] == '資本總額(元)':
                        capital_total = df[1][i].split(' ')[0]

                    if df[0][i] == '實收資本額(元)':
                        real_capital_total = df[1][i].split(' ')[0]

                    if df[0][i] == 'Mail':
                        mail = df[1][i]

                company['公司名稱'] = company_name
                company['電話'] = tel
                company['傳真'] = fax
                company['公司地址'] = company_address
                company['稅籍狀況'] = tax
                company['統一編號（統編）'] = invoicd_id
                company['股票代號'] = stock_code
                company['代表人姓名'] = representative_name
                company['網址'] = company_url   
                company['mail'] = company_mail
                company['公司狀況'] = company_status
                company['資本總額(元)'] = capital_total
                company['實收資本額(元)'] = real_capital_total
                company['url'] = detail_url
                company['mail'] = mail
                company['基本資料'] = basic


                companies.append(company)

    pages = ""
    if start != 0 and end != 0:
        pages = str(start) + '-' + str(end)
    save_datas_to_csv(path_csv, key_txt, companies, pages)
    return 

def save_datas_to_csv(path_csv, key_txt, companies, pages):
    # 建立資料夾
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)

    # 建立檔案
    if not os.path.exists(path_csv + key_txt + pages + '.csv'):
        with open(path_csv + key_txt + pages + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['公司名稱', '公司地址', '電話', '傳真', '稅籍狀況', 'Email', '資本總額(元)', '實收資本額(元)', '統一編號（統編）', '股票代號', '代表人姓名', '網址', '公司狀況', 'url', '基本資料'])
    # 寫入資料
    with open(path_csv + key_txt + pages + '.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for company in companies:
            writer.writerow([company['公司名稱'], company['公司地址'], company['電話'], company['傳真'], company['稅籍狀況'], company['mail'], company['資本總額(元)'], company['實收資本額(元)'], company['統一編號（統編）'], company['股票代號'], company['代表人姓名'], company['網址'], company['公司狀況'], company['url'], company['基本資料']])
    return


if __name__ == '__main__':
    start = 0
    end = 0
    input_go = args = sys.argv[1:]
    if len(input_go) == 0:
        print('請輸入關鍵字')
    else:
        if len(input_go) == 3:
            start = int(input_go[1])
            end = int(input_go[2])
        save_title_data = find_title_104(input_go[0], start, end)

    driver.quit()#關閉瀏覽器
