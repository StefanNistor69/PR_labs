import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://999.md/'


def extract_urls(page_url, accumulated_urls=None):
    if accumulated_urls is None:
        accumulated_urls = []

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')


    links = soup.find_all('a')

    for link in links:
        url = link.get('href')
        if url and not url.startswith('javascript:') and 'booster' not in url:

            if not url.startswith('http') and not url.startswith('/ro/'):
                url = BASE_URL.rstrip('/') + '/' + url.lstrip('/')
            elif url.startswith('/ro/'):
                url = BASE_URL.rstrip('/') + url


            if url.startswith(BASE_URL) and url.split('/')[-2] == 'ro' and url.split('/')[-1].isdigit():
                accumulated_urls.append(url)


    next_page = soup.find('a', string='Next')
    if next_page:
        next_page_url = next_page['href']
        if not next_page_url.startswith('http'):
            next_page_url = BASE_URL.rstrip('/') + '/' + next_page_url.lstrip('/')
        return extract_urls(next_page_url, accumulated_urls)
    else:
        return accumulated_urls



urls = extract_urls('https://999.md/ro/category/real-estate')
print(urls)
