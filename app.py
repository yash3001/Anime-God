import requests
from bs4 import BeautifulSoup

url = "https://gogoanime.vc//search.html?keyword="
name = input("Enter the name of the anime: ")
url = url+name
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

names = soup.find("div", class_="last_episodes").find("ul", class_="items").find_all("li")
if(not len(names)):
    exit
d = {}
index = 1
for name in names:
    ele = name.find("p", class_="name").find("a")
    d[index] = ele["href"]
    print(f"{index}) {ele['title']}")
    index += 1

num = input("\nEnter your choice: ")

url = "https://gogoanime.vc"+d[int(num)]

r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

# print(soup.prettify)
episodes = soup.find("div", class_="anime_video_body").find("ul").find("li").find("a")
ep_start = int(episodes['ep_start'])
ep_end = int(episodes['ep_end'])

ep_num = input(f"\nChoose an episode({ep_start+1}-{ep_end}): ")

series_name = url.split('/')[-1]

url = f"https://gogoanime.vc/{series_name}-episode-{ep_num}"


r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

download_page_link = soup.find("div", class_="download-anime").find("ul").find_all("li")[0].find('a')['href']
#print(download_page_link)

url = download_page_link

r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")
#print(soup.prettify)

divs = soup.find_all("div", class_="mirror_link")
# print(len(divs))

d = {}
index = 1
for div in divs[:-1]:
    qualities = div.find_all('div')
    for quality in qualities:
        q=quality.find('a')
        # print(index, q.text.split()[1][1:])
        d[index] = q['href']
        index += 1

# quality_num = input("Choose the quality: ")
# url = d[int(quality_num)]
url = d[1]

import os

cmd = f"mpv {url}"
os.system(cmd)