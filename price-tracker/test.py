import requests
import html5lib
from bs4 import BeautifulSoup

url = "https://www.cardmarket.com/fr/YuGiOh/Products/Singles/25th-Anniversary-Tin-Dueling-Heroes-Mega-Pack/Lady-Labrynth-of-the-Silver-Castle?sellerCountry=12&language=1,2"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

req = requests.get(url, headers=headers)
#print(req.content)
soup = BeautifulSoup(req.content, "html5lib")
print(req)

# "col-6 col-xl-7" 
dd_tags = soup.find_all("dd", class_="col-6 col-xl-7")
prices = []

for dd in dd_tags:
    try:
        price.append(dd.span.text)
    except AttributeError:
        continue

# Prices:
# 0: tendance des prix
# 1: prix moyen 30 jours
# 2: prix moyen 7 jours
# 3: prix moyen 1 jour