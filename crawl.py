from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
from urllib.parse import quote_plus

chromedriver ='C:\dev_python\Webdriver\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(1)

driver.get('https://codeforces.com/ratings/organization/9105')

hi_class=[]
hi_id=[]
hi_num=[]
hi_rating=[]
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

for title in soup.select('#pageContent > div.datatable.ratingsDatatable > div:nth-of-type(6) > table > tbody > tr > td > a'):
    cls, id = str(title.get('title')).split(' ')
    hi_class.append(cls)
    hi_id.append(id)

for num in soup.select('#pageContent > div.datatable.ratingsDatatable > div:nth-of-type(6) > table > tbody > tr > td:nth-of-type(3)'):
    tmp = str(num.text).replace(' ','')
    tmp = tmp.replace('\n','')
    hi_num.append(tmp)

for rating in soup.select('#pageContent > div.datatable.ratingsDatatable > div:nth-of-type(6) > table > tbody > tr > td:nth-of-type(4)'):
    tmp = str(rating.text).replace(' ','')
    tmp = tmp.replace('\n','')
    hi_rating.append(tmp)

print(hi_class)
print(hi_id)
print(hi_num)
print(hi_rating)

# f = open(f'codeforces.csv', 'w', encoding = 'utf-8', newline='')
# csvWriter = csv.writer(f)
# for i in results:
#     # 한줄씩 써 내려감
#     csvWriter.writerow(i)
# f.close()
# print("success")