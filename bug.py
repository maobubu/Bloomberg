import ssl
from bs4 import BeautifulSoup
import re
import datetime
import json
import collections
import requests
from time import sleep

print('start time:', datetime.datetime.now())
ssl._create_default_https_context = ssl._create_unverified_context()
base_url = "https://www.bloomberg.com/search?query=stock&endTime=2018-02-25T00:03:02.999Z&page="
counter = 0
#proxy = {"http": "http://125.122.149.13:9000"}
headers = {'Host': 'www.bloomberg.com', 'Upgrade-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

for i in range(2217, 2800):
    try:
        counter = 0
        base = base_url + str(i + 1)
        data = dict()
        data.setdefault("date", "Default")
        s = requests.Session()
        html = s.get(base, headers=headers)
        html = html.text
        soup = BeautifulSoup(html, 'html.parser')
        arti_url = soup.find("a", dict(href=re.compile('https://www.bloomberg.com/news/articles*')))

        while type(None) != type(arti_url):
            f = requests.Session()
            arti_html = f.get(arti_url['href'], headers=headers)
            arti_html = arti_html.text
            arti_soup = BeautifulSoup(arti_html, 'html.parser')
            title = arti_soup.find('meta', {"property": "og:title"})
            abstract = arti_soup.find('meta', {"name": "twitter:description"})
            date = arti_soup.find('meta', {"name": "parsely-pub-date"})
            sentence = arti_soup.find_all('p', {"class": ""})
            text = ""
            for j in sentence:
                text = text + j.get_text("|", strip=True)
            data["date"] = date['content'][0:10] if type(None) != type(date) else 'None'
            data["title"] = title['content']
            data["abstract"] = abstract['content']
            data["article"] = text
            counter += 1
            o_data = collections.OrderedDict(data)
            with open('bugtest.json', 'a+') as f:
                json_o = json.dump(o_data, f)
                f.write('\r')
            arti_url = arti_url.find_next("a", {"href": re.compile('https://www.bloomberg.com/news/articles/*')})
            if type(None) == type(arti_url):
                break
            arti_url = arti_url.find_next("a", {"href": re.compile('https://www.bloomberg.com/news/articles/*')})
        print("page={},date={}".format(i + 1, data["date"]))
        print(counter)
        sleep(30)
    except Exception as e:
        print("There is a error:{}".format(str(e)))
        with open("error.txt", "a+") as er:
            er.write("There is a error:{},page:{},date:{}\n".format(str(e), i + 1, data["date"]))
        continue
