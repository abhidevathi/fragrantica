import requests
from bs4 import BeautifulSoup

def get_page(url,
             user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'):
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)

    page.raise_for_status()

    return page

def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')

def create_attributes(page):
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('h1', itemprop='name')
    title = title.text

    rating = soup.find('span', itemprop='ratingValue')
    rating = float(rating.text)

    votes = soup.find('span', itemprop='ratingCount')
    votes = int(votes.text)

    description = soup.find('div', itemprop='description')
    description = description.text.split('\n')[1].strip()

    title = title.split('for')
    genders = title[1].strip()
    title = title[0].strip()

    if ('men' in genders) and ('women' in genders):
        gender = 'both'
    elif 'women' in genders:
        gender = 'female'
    elif 'men' in genders:
        gender = 'male'
    name = description.split('by')[0].strip()
    designer = description.split('by')[1].split('is')[0].strip()

    # Create attributes dictionary
    attributes = {}
    attributes['title'] = title
    attributes['name'] = name
    attributes['designer'] = designer
    attributes['rating'] = rating
    attributes['votes'] = votes
    attributes['gender'] = gender
    attributes['url'] = page.url
    return attributes
