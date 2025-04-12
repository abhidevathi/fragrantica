import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from decimal import Decimal

def p2f(x):
    return Decimal(x.strip('%'))/100

def s2f(x):
    return Decimal(x.replace(',',''))

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


def scrape_fragrance(url, ua=UserAgent()):
    headers = {"User-Agent": ua.random} # Create a new header every time we do a pull from the API
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    
        perfume_dict={}
        perfume_dict['url']=url
        
        # Extract data
        perfume_dict['name'] = soup.find("h1").text.strip()
        name = soup.find("h1").text.strip()
        gender=''
        if 'women' in name and 'men' in name:
            gender='unisex'
        elif 'men' in name:
            gender='male'
        elif 'female' in name:
            gender='female'
        
        perfume_dict['gender']=gender
        perfume_dict['brand'] = soup.find("span", {"itemprop": "name"}).text.strip()
        perfume_dict['rating'] = s2f(soup.find("span", {"itemprop": "ratingValue"}).text.strip())
        perfume_dict['vote'] = s2f(soup.find("span", {"itemprop": "ratingCount"}).text.strip())
        
        # Accords
        accords = soup.find_all("div", class_="accord-bar")
        accord_dict = {}
        for accord in accords:
            style=accord['style']
            width_match = re.search(r"width\s*:\s*([^;]+)", style, re.IGNORECASE)
            if width_match:
                width = p2f(width_match.group(1).strip())
            else:
                width = 0
            accord_dict[accord.get_text()]=width
    
        perfume_dict['accords']=accord_dict
        '''
            Get notes saved into a_tags
        '''
        
        a_tags = soup.find_all("a", href=lambda href: href and href.startswith("https://www.fragrantica.com/notes/"))
        note_dict={}
        if a_tags:
            for a_tag in a_tags:
                target_div = a_tag.parent
                note_text = target_div.get_text(strip=True, separator=" ").replace(a_tag.get_text(strip=True), "").strip().lower()
                note_dict[note_text]=a_tag['href']
        else:
            print("No matching <a> tags found.")
        perfume_dict['notes']=note_dict
        return perfume_dict
        
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None
