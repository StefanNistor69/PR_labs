import requests
from bs4 import BeautifulSoup
import json


def extract_info(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")


    result = {}


    title = soup.find('h1', itemprop='name')
    if title:
        result['Title'] = title.text.strip()


    desc = soup.find('div', itemprop='description')
    if desc:
        result['Description'] = desc.text.strip()


    price = soup.find('span', class_='adPage__content__price-feature__prices__price__value')
    currency = soup.find('span', itemprop='priceCurrency')
    if price:
        result['Price'] = f"{price.text.strip()} {currency.get('content').strip()}" if currency else price.text.strip()


    locality = soup.find('meta', itemprop='addressLocality')
    country = soup.find('meta', itemprop='addressCountry')
    if locality and country:
        result['Location'] = f"{locality['content'].strip()}, {country['content'].strip()}"


    ad_info_keys = ['Views', 'Update Date', 'Ad Type', 'Owner Username']
    selectors = ['adPage__aside__stats__views', 'adPage__aside__stats__date', 'adPage__aside__stats__type']
    result['Ad Info'] = {
        key: soup.find('div', class_=selector).text.strip() if soup.find('div', class_=selector) else None
        for key, selector in zip(ad_info_keys, selectors)}

    owner_username = soup.find('a', class_='adPage__aside__stats__owner__login')
    if owner_username:
        result['Ad Info']['Owner Username'] = owner_username.text.strip()

    for section, class_name in [('General Info', 'adPage__content__features__col'),
                                ('Features', 'adPage__content__features__col grid_7 suffix_1')]:
        data = {}
        div = soup.find('div', class_=class_name)
        if div:
            for li in div.find_all('li'):
                key = li.find('span', class_='adPage__content__features__key')
                value = li.find('span', class_='adPage__content__features__value')
                if key and value:
                    data[key.text.strip()] = value.text.strip()
            result[section] = data

    return json.dumps(result, indent=4, ensure_ascii=False)


URL = "https://999.md/ro/82197657"
print(extract_info(URL))
