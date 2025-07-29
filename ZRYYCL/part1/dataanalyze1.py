import json
import re
import requests
import datetime
from bs4 import BeautifulSoup
import os

os.makedirs('work', exist_ok=True)

def crawl_wiki_data():
    """
    爬取百度百科中《乘风破浪的姐姐第二季》中嘉宾的信息,返回html
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3369.99 Safari/537.36'
    }
    url = "https://baike.baidu.com/item/乘风破浪的姐姐第二季"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table', class_='basicInfo')
        #print(tables)
        crawl_table_title = "按姓氏首字母排序"
        for table in tables:
            table_titles = table.find_previous('div')
            #print(table_titles)
            for title in table_titles:
                if (crawl_table_title in title):
                    return table
    except Exception as e:
        print(e)

def parse_wiki_data(table_html):
    """
    解析百度百科中《乘风破浪的姐姐第二季》中嘉宾的信息,保存为json文件,保存到work目录下
    """
    soup = BeautifulSoup(str(table_html), 'lxml')
    all_trs = soup.find_all('tr')

    stars = []
    for tr in all_trs:
        all_trs = tr.find_all('td')
        for td in all_trs:
            star = {}
            if td.find('a'):
                star['name'] = td.find('a').text
                star['link'] = 'https//baike.baidu.com'+ td.find('a').get('href')
                stars.append(star)
    json_data = json.loads(str(stars).replace("\'","\""))
    with open('work/'+'stars.json','w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)

def down_save_pic(name,pic_urls):
    path = 'work/' + 'pics/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(url, timeout = 15)
            pic.raise_for_status()
            string = str(i + 1) + '.jpg'
            with open(path + string, 'wb') as f:
                f.write(pic.content)
                #print('successful download image number %s: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print(e)
            continue

def crawl_everyone_wiki_urls():
    """
    爬取每个选手的百度百科个人信息，并保存
    """
    with open('work/' + 'stars.json', 'r', encoding='utf-8') as file:
        json_array = json.loads(file.read())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3369.99 Safari/537.36'
    }
    star_infos = []

    for star in json_array:
        star_info = {}
        name = star['name']
        link = star['link']
        star_info['name'] = name
        response = requests.get(link, headers=headers, timeout=15)
        #将一段文档传入BeautifulSoup 的构造方法，就可以得到一个文档对象
        bs = BeautifulSoup(response.text, 'lxml')
        base_info_div = bs.find('div', class_='basic-info cmn-clearfix')
        dls = base_info_div.find_all('dl')
        for dl in dls:
            dts = dl.find_all('dt')
            for dt in dts:
                if "".join(str(dt.text).split()) == '民族':
                    star_info['nation'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '星座':
                    star_info['constellation'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '血型':
                    star_info['blood_type'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '身高':
                    height_str = str(dt.find_next('dd').text)
                    star_info['height'] = str(height_str[0:height_str.find('cm')]).replace("\n","")
                if "".join(str(dt.text).split()) == '体重':
                    star_info['weight'] = str(dt.find_next('dd').text).replace("\n","")
                if "".join(str(dt.text).split()) == '出生日期':
                    birth_str = str(dt.find_next('dd').text).replace("\n","")
                    if '年' in birth_str:
                        star_info['birth'] = birth_str[0:birth_str.rfind('年')]
        star_infos.append(star_info)
        if bs.select('.summary-pic a'):
            pic_list_url = bs.select('.summary-pic a')[0].get('href')
            pic_list_url = 'https://baike.baidu.com' + pic_list_url
            pic_list_response = requests.get(pic_list_url, headers=headers)
            bs = BeautifulSoup(pic_list_response.text, 'lxml')
            pic_list_html = bs.select('.pic-list img')
            pic_urls = []
            for pic_html in pic_list_html:
                pic_url = pic_html.get('src')
                pic_urls.append(pic_url)
            down_save_pic(name,pic_urls)
        json_data = json.loads(str(star_infos).replace("\'","\"")).replace("\\xa0","")
        with open('work/' + 'stars_info.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
if __name__ == "__main__":
    html = crawl_wiki_data()
    #print(html)
    parse_wiki_data(html)
    
    crawl_everyone_wiki_urls()
    print("所有信息爬取完成！")