#Парсер для извлечения данных о недвижимости сайта циан.

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&offer_type=flat&region=1&room1=1&room2=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
print("Статус:", response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    
    items = soup.find_all('article', {'data-name': 'CardComponent'})
    
    for item in items[:10]:  
        title = item.find('span', {'data-mark': 'OfferTitle'})
        title = title.text.strip() if title else "Квартира"
        
        price = item.find('span', {'data-mark': 'MainPrice'})
        price = price.text.strip() if price else "0 ₽"
        
        address = item.find('a', {'data-name': 'GeoLabel'})
        address = address.text.strip() if address else "Адрес не указан"
        
        data.append({
            'Название': title,
            'Цена': price,
            'Адрес': address
        })
    
    df = pd.DataFrame(data)
    print(df)
else:
    print("Ошибка загрузки страницы")