import requests
import psycopg2
from bs4 import BeautifulSoup

def updatePage(users, conn, cur):
    for user in users:
        # userCurData[2]=userCurData[2].strip()
        # userCurData[3]=int(userCurData[3].replace(",",""))
        # if userCurData[4] == '–':
        #     userCurData[4] = "0"
        # userCurData[4]=int(userCurData[4].replace("⁺",""))
        # userCurData[5]=int(userCurData[5].replace(",",""))
        print(user)
        cur.execute("SELECT class, entered, cfrating FROM userinfo WHERE userid='{}'".format(user[0]))
        userPrevData = cur.fetchall()
        print(userPrevData)
        if len(userPrevData) == 0:
            print("First user")
            cur.execute("INSERT INTO userinfo VALUES(%s, %s, %s, %s, %s)",
                        (user[0], user[1], user[3], user[2], "now"))
        else:
            print("Dup.")
            cur.execute("UPDATE userinfo SET class=%s, entered=%s, cfrating=%s, enteredgap=%s, cfratinggap=%s, lastupdated=%s WHERE userid=%s",
                        (user[1], user[2], user[3], 
                        # int(user[1])-int(userPrevData[0][0]),  # classgap=%s, 
                         int(user[2])-int(userPrevData[0][1]),
                         int(user[3])-int(userPrevData[0][2]),
                         "now",
                         user[0]))
    conn.commit()

conn = psycopg2.connect(host='localhost', dbname='codeforces', user='postgres', password='1234')
cur = conn.cursor()

baseUrl='https://codeforces.com/ratings/organization/9105'
response = requests.get(baseUrl)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    hi_class=[]
    hi_id=[]
    hi_num=[] #enter
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

    users=[]
    for i in range(len(hi_id)):
        users.append([hi_id[i],hi_class[i],hi_num[i],hi_rating[i]])        
    updatePage(users, conn, cur)
    print("completed")



cur.execute("SELECT userid FROM userinfo ORDER BY entered DESC LIMIT 10")
print("참가 콘테스트 수 상위 10명")
print(cur.fetchall())

cur.execute("SELECT userid FROM userinfo ORDER BY enteredgap DESC LIMIT 10")
print("참가 콘테스트 수 변동 상위 10명")
print(cur.fetchall())

cur.execute("SELECT userid FROM userinfo ORDER BY class DESC LIMIT 10")
print("CLASS 상위 10명")
print(cur.fetchall())

# cur.execute("SELECT userid FROM userinfo ORDER BY classgap DESC LIMIT 10")
# print("CLASS 변동 상위 10명")
# print(cur.fetchall())

cur.execute("SELECT userid FROM userinfo ORDER BY cfrating DESC LIMIT 10")
print("CF Rating 상위 10명")
print(cur.fetchall())

cur.execute("SELECT userid FROM userinfo ORDER BY cfratinggap DESC LIMIT 10")
print("CF Rating 변동 상위 10명")
print(cur.fetchall())
