from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
from urllib.parse import quote_plus

chromedriver ='C:\dev_python\Webdriver\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(1)

# go to the login page & login
driver.get('https://everytime.kr/login')
driver.find_element_by_name('userid').send_keys('userid')  #send_keys에는 실제로 로그인할 계정의 id와 pw
driver.find_element_by_name('password').send_keys('password')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
driver.implicitly_wait(1)

# result text files
results = []
cnt = 0 # 첫번째 페이지부터 순환하기 위함.

# go to the list (first page)
while True:

    #print('Page '+str(cnt))
    
    if cnt > 10: # 나중에 10,000 개로 수정
        break
        
    cnt = cnt + 1
    driver.get('https://everytime.kr/374399/p/'+ str(cnt)) #374399는 홍익대 서울캠 야 넌홍대생인데 홍대맛집도모르냐 게시판 번호
    driver.implicitly_wait(1)

    # get articles link
    posts = driver.find_elements_by_css_selector('article > a.article')
    links = [post.get_attribute('href') for post in posts]
    
    # get detail article
    for link in links:
        driver.get(link)
        
        # get text
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        comments = soup.select('#container > div.wrap.articles > article > a > p')
        
        #for comment in comments:
        results.append([comments])

f = open(f'everytime.csv', 'w', encoding = 'utf-8', newline='')
csvWriter = csv.writer(f)
for i in results:
    # 한줄씩 써 내려감
    csvWriter.writerow(i)
f.close()
print("success")
