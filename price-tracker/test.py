import requests
from bs4 import BeautifulSoup

url = "https://www.cardmarket.com/fr/YuGiOh/Products/Singles/25th-Anniversary-Tin-Dueling-Heroes-Mega-Pack/Lady-Labrynth-of-the-Silver-Castle?sellerCountry=12&language=1,2"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

req = requests.get(url, headers=headers)
#print(req.content)
soup = BeautifulSoup(req.content, "html5lib")
print(req)

# Traitement en fonction de la réponse
dd_tags = soup.find_all("dd", class_="col-6 col-xl-7")
prices = []

for dd in dd_tags:
    try:
        prices.append(dd.span.text)
    except AttributeError:
        continue

print(prices)

# Prices:
# - tendance des prix
# - prix moyen 30 jours
# - prix moyen 7 jours
# - prix moyen 1 jour

# Result: ['', '1,06 €', '1,23 €', '1,15 €', '1,35 €']