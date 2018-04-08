import urllib.parse
from bs4 import BeautifulSoup
import requests
import re

text = 'birb'
text = urllib.parse.quote_plus(text)

url = 'https://google.com/search?q=' + text + '&tbm=isch&source=lnms'

response = requests.get(url)
#with open('output.html', 'wb') as f:
#    f.write(response.content)
#webbrowser.open('output.html')

links = []

soup = BeautifulSoup(response.text, 'lxml')

m = str(soup)
m1 = re.findall("l", m)
print(m1)
for link in range(0,1):
    links.append(link)
    print(str(link).partition('src="')[2].partition('"')[0])
