#coding:utf-8
import requests
import urllib.request
import urllib
from bs4 import BeautifulSoup
import re
from lxml import etree
import xlrd
import xlwt
import xlutils.copy


a1 = '影片名字'
a2 = '导演'
a3 = '编剧'
a4 = '主演'
a5 = '类型'
a6 ='制片国家/地区'
a7 = '语言'
a8 = '上映日期'
a9 = '片长'
a10 = '又名'
a11 = '影评'
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('photo', cell_overwrite_ok=True)
sheet.write(0, 0, a1)
sheet.write(0, 1, a2)
sheet.write(0, 2, a3)
sheet.write(0, 3, a4)
sheet.write(0, 4, a5)
sheet.write(0, 5, a6)
sheet.write(0, 6, a7)
sheet.write(0, 7, a8)
sheet.write(0, 8, a9)
sheet.write(0, 9, a10)
sheet.write(0, 10, a11)
book.save('E:/Python编程包/ctf/test.xls')
url = 'https://movie.douban.com/top250'
headers = {'User-Agen':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'}
html = requests.get(url,headers=headers)
con = re.compile('start=(.*?)&amp;filter=" >')
ans = re.findall(con,html.text)
yeshu = int(ans[-2])
jiange = int(ans[-1])
num = 0
for i in range(jiange-jiange,yeshu+jiange,jiange):
    realurl = url+'?start='+str(i)
# for i in range(0,25):
#     realurl = url+'?start='+str(i)
    ht = requests.get(realurl,headers=headers)
    soup = BeautifulSoup(ht.text,'lxml')
    list = soup.find('div', class_='hd').find_all('a')
    for li in list:
        num = num+1
        href = li['href']
        ht2 = requests.get(href).text
        se = etree.HTML(ht2)
        bianju = []
        nr = []
        mingzi = se.xpath('//*[@id="content"]/h1/span[1]/text()')
        daoyan = se.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        bianju_len = len(se.xpath('//*[@id="info"]/span[2]/span[2]/a'))
        for k in range(bianju_len):
            bianju.append(se.xpath('//*[@id="info"]/span[2]/span[2]/a['+str(k+1)+']/text()'))

        con2 = re.compile('rel="v:starring">(.*?)</a>')
        zhuyan = re.findall(con2,ht2)
        con3 = re.compile('property="v:genre">(.*?)</span>')
        leixing = re.findall(con3,ht2)
        con4 = re.compile('class="pl">制片国家/地区:</span>(.*?)<br/>')
        zhipianguo = re.findall(con4,ht2)
        con5 = re.compile('class="pl">语言:</span>(.*?)<br/>')
        yuyan = re.findall(con5, ht2)
        con6 = re.compile('property="v:initialReleaseDate" content="(.*?)">')
        shangyin = re.findall(con6, ht2)
        pianchang = se.xpath('//*[@id="info"]/span[13]/text()')
        con7 = re.compile('class="pl">又名:</span>(.*?)<br/>')
        bieming = re.findall(con7, ht2)
        if num==1:
            res = se.xpath('//*[@id="link-report"]/span[1]/span/text()')
        else:
            res = se.xpath('//*[@id="link-report"]/span[1]/text()')


        rb = xlrd.open_workbook(r'E:/Python编程包/ctf/test.xls')
        wb = xlutils.copy.copy(rb)
        ws = wb.get_sheet(0)
        ws.write(num, 0, mingzi)
        ws.write(num, 1, daoyan)
        for x in range(bianju_len):
            ws.write(num, 2, bianju[x])
        ws.write(num, 3, zhuyan)
        ws.write(num, 4, leixing)
        ws.write(num, 5, zhipianguo)
        ws.write(num, 6, yuyan)
        ws.write(num, 7, shangyin)
        ws.write(num, 8, pianchang)
        ws.write(num, 9, bieming)
        ws.write(num, 10, res)
        wb.save(r'E:/Python编程包/ctf/test.xls')
