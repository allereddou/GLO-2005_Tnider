import urllib.parse
from bs4 import BeautifulSoup
import requests

text = 'birb'
text = urllib.parse.quote_plus(text)

url = 'https://google.com/search?q=' + text + '&tbm=isch&source=lnms'
print(url)

response = requests.get(url)
# with open('output.html', 'wb') as f:
#    f.write(response.content)
# webbrowser.open('output.html')

links = []

soup = BeautifulSoup(response.text, 'lxml')
print(soup)
for link in soup.find_all('img'):
    links.append(link)
    #print(str(link).partition('src="')[2].partition('"')[0])

birbs = ["https://i.ytimg.com/vi/R_8bwhiHGHc/hqdefault.jpg", "https://i.ytimg.com/vi/0fLvvYO_C5U/hqdefault.jpg",
         "https://i.ytimg.com/vi/TWw4l347KDI/maxresdefault.jpg", "https://i.ytimg.com/vi/CXROU_gbEMg/maxresdefault.jpg",
         "https://i1.wp.com/www.cutesypooh.com/wp-content/uploads/2017/10/1-NAudFQB-650x650.jpg?resize=600%2C600",
         "https://pics.me.me/thatgirlwiththeguitar-it-me-source-awwww-cute-knit-birb-and-real-birb-28151256.png",
         "https://i0.wp.com/dangriffinyucatan.com/sitenew/wp-content/uploads/2016/06/Amazona_albifrons_-upper_body-8a.jpg?fit=800%2C536",
         "https://vignette.wikia.nocookie.net/animaljam/images/9/9a/Luinifer.jpg/revision/latest?cb=20150920145349",
         "https://assets.change.org/photos/6/dn/fd/NldNfdcEtlICmEs-800x450-noPad.jpg?1478120469", ]
