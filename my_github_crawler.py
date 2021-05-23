import requests
from bs4 import BeautifulSoup

def user_profile(username):
    profile_url = "https://github.com/"+ username
    user_profile_results = user_profile_parser(profile_url,username)
    return user_profile_results

def user_profile_parser(profile_url,username):
    URL = profile_url + '?tab=repositories'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    user_followers = user_followers_parser(soup,username)
    user_repositories_urls = user_repositories_parser(soup,username)
    sumstargazers = 0
    for i in user_repositories_urls:
        sumstargazers += user_repos_parser(i)
    user_profile_results = {
        "username" : username,
        "followers" : user_followers,
        "stars" : sumstargazers
    }
    return user_profile_results

def user_followers_parser(soup,username):
    user_followers = soup.find('a', href= 'https://github.com/'+ username+'?tab=followers')
    user_followers = user_followers.find('span').get_text()
    if user_followers[-1:] == 'k':
        user_followers = float(user_followers.replace('k',''))*1000
    return int(user_followers)

def user_repositories_parser(soup,username):
    user_repositories_text = soup.find('div', id = 'user-repositories-list')
    user_repositories_urls = user_repositories_text.find_all('a', itemprop = "name codeRepository")
    for i in range(len(user_repositories_urls)):
        user_repositories_urls[i] = user_repositories_urls[i].get('href')
    return user_repositories_urls

def user_repos_parser(url):
    URL = "https://github.com"+url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    stargazers = int(repo_stargazers(soup,url))
    return stargazers

def repo_stargazers(soup,url):
    stargazers_text  = url+"/stargazers"
    stargazers = soup.find('a', href=stargazers_text)
    stargazers = stargazers.text
    stargazers = stargazers.replace('\n','')    
    stargazers = stargazers.replace(' ','')
    if stargazers[-1:] == 'k':
        stargazers = float(stargazers.replace('k',''))*1000
    return stargazers

def repo_info(url):
    user_repos_results = user_repos_parser(url)
    return user_repos_results

print(user_profile("minjae705"))

