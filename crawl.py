import requests
from bs4 import BeautifulSoup

baseurl='https://codeforces.com/ratings/organization/9105'
req = requests.get(baseurl)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

hi_class=[]
hi_id=[]
hi_num=[]
hi_rating=[]

for title in soup.select('div.datatable.ratingsDatatable > div:nth-of-type(6) > table a'):
    cls, id = str(title.get('title')).split(' ')
    hi_class.append(cls)
    hi_id.append(id)

tables = soup.select('div.datatable.ratingsDatatable > div:nth-of-type(6) > table td')
for i in range(len(tables)//4):
    num, rating = tables[4*i+2].text, tables[4*i+3].text
    num = str(num).replace(' ','')
    num = num.replace('\n','')
    num = num.replace('\r','')
    
    rating = str(rating).replace(' ','')
    rating = rating.replace('\n','')    
    rating = rating.replace('\r','')
    
    hi_num.append(num)
    hi_rating.append(rating)

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