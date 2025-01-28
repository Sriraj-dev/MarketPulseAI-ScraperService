from datetime import date
import requests
from bs4 import BeautifulSoup
from shared import ECONOMIC_TIMES_BASE_URL

def store_economictimes_feed(rundate : date):
    print("Collecting data from economic times ...")

    scrape_economictimes(rundate)


def scrape_economictimes(rundate : date):
    baseUrl = ECONOMIC_TIMES_BASE_URL
    response = requests.get(ECONOMIC_TIMES_BASE_URL)
    
    if(response.status_code != 200):
        print("Error in scraping data from businesstoday.com")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tags = soup.find_all('div', class_ = 'eachStory',limit=1)

    for div_tag in div_tags:
        anchor_tag = div_tag.find('h3').find('a')["href"]
        print(anchor_tag)
    

