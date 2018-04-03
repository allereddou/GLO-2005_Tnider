import urllib.parse
from bs4 import BeautifulSoup
import requests

text = 'birb'
text = urllib.parse.quote_plus(text)

url = 'https://google.com/search?q=' + text + '&tbm=isch&source=lnms'

response = requests.get(url)
#with open('output.html', 'wb') as f:
#    f.write(response.content)
#webbrowser.open('output.html')

links = []

soup = BeautifulSoup(response.text, 'lxml')
print(soup)
for link in soup.find_all('img'):
    links.append(link)
    print(str(link).partition('src="')[2].partition('"')[0])
