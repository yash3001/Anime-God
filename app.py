import requests
import os
from bs4 import BeautifulSoup
from termcolor import colored

os.system("clear")

banner = colored("""
 ▄▄▄       ███▄    █  ██▓ ███▄ ▄███▓▓█████      ▄████  ▒█████  ▓█████▄
▒████▄     ██ ▀█   █ ▓██▒▓██▒▀█▀ ██▒▓█   ▀     ██▒ ▀█▒▒██▒  ██▒▒██▀ ██▌
▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒▓██    ▓██░▒███      ▒██░▄▄▄░▒██░  ██▒░██   █▌
░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░▒██    ▒██ ▒▓█  ▄    ░▓█  ██▓▒██   ██░░▓█▄   ▌
 ▓█   ▓██▒▒██░   ▓██░░██░▒██▒   ░██▒░▒████▒   ░▒▓███▀▒░ ████▓▒░░▒████▓
 ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  ░ ▒░   ░  ░░░ ▒░ ░    ░▒   ▒ ░ ▒░▒░▒░  ▒▒▓  ▒
  ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░░  ░      ░ ░ ░  ░     ░   ░   ░ ▒ ▒░  ░ ▒  ▒
  ░   ▒      ░   ░ ░  ▒ ░░      ░      ░      ░ ░   ░ ░ ░ ░ ▒   ░ ░  ░
      ░  ░         ░  ░         ░      ░  ░         ░     ░ ░     ░
                                                                  ░
""", 'cyan')

print(banner)

#scrapping the anime names after searching
url = "https://gogoanime.vc//search.html?keyword="

name = input(colored("Enter the name of the anime: ", 'yellow'))
url = url+name

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
names = soup.find("div", class_="last_episodes").find("ul", class_="items").find_all("li")

#quiting if no anime for the given name found
if(not len(names)):
    exit

#getting the specific season or type
os.system('clear')
print(banner)
print(colored(f"Search topic: {name}\n", 'green', attrs=['bold']))
print(colored("Choose the correct series and season:\n", 'yellow'))
d = {}
n = {}
index = 1
for name in names:
    ele = name.find("p", class_="name").find("a")
    d[index] = ele["href"]
    n[index] = ele['title']
    print(colored(f"{index}) {ele['title']}", 'green'))
    index += 1

num = input(colored(f"\nEnter your choice(1-{index-1}): ", 'yellow'))

#scrapping the specific anime for episode selection
os.system("clear")
print(banner)
print(colored(f"Chosen anime: {n[int(num)]}", 'green', attrs=['bold']))
url = "https://gogoanime.vc"+d[int(num)]

r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

episodes = soup.find("div", class_="anime_video_body").find("ul").find("li").find("a")
ep_start = int(episodes['ep_start'])
ep_end = int(episodes['ep_end'])

ep_num = input(colored(f"\nChoose an episode({ep_start+1}-{ep_end}): ", 'yellow'))

series_name = url.split('/')[-1]

url = f"https://gogoanime.vc/{series_name}-episode-{ep_num}"

#downloading / streaming the anime episode
r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

download_page_link = soup.find("div", class_="download-anime").find("ul").find_all("li")[0].find('a')['href']

url = download_page_link

r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

divs = soup.find_all("div", class_="mirror_link")

#getting the resolution
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

#running the anime on mpv
cmd = f"mpv {url}"
os.system(cmd)