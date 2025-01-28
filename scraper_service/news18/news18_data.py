from shared import NEWS18_BASE_URL
from models import MarketDataModel
from datetime import date,timedelta
from shared import upload_to_s3
import requests
import dateparser
from bs4 import BeautifulSoup

def store_news18_feeds(rundate : date):
    print("Collecting data from News18.com")

    feed_data = scrape_news_data(rundate)
    print("Collected data from News18.com, No.Of Blogs Collected - ", len(feed_data))
    upload_to_s3("news18", feed_data, rundate)

def scrape_news_data(rundate : date):
    baseurl = NEWS18_BASE_URL
    response = requests.get(baseurl)

    if(response.status_code != 200):
        print("Error fetching data from News18.com")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tags = soup.find_all('div', class_ = 'jsx-50600299959a4159 blog_list_row')

    listings : list[MarketDataModel] = []
    print(rundate)
    for div_tag in div_tags:
        updated_date = div_tag.find('sub', class_ = 'jsx-50600299959a4159 story_date').get_text(strip=True)
        link = div_tag.find('a', class_ = 'jsx-50600299959a4159')['href']

        if(rundate > get_published_date(updated_date)):
            break

        if(rundate == get_published_date(updated_date)):
            listings.append(scrape_blog_content(link))
        
    return listings


def scrape_blog_content(blogUrl : str):
    print("Collecting from ", blogUrl)
    response = requests.get(blogUrl)

    if(response.status_code != 200):
        print("Error fetching data from the blog")
        return 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title', class_ = 'jsx-5209c605120af8').text.strip()
    desc = soup.find('meta' , attrs={'name' : 'description'}).get('content')
    p_tags = soup.find_all('p')
    content = ' '.join([p.text.strip() for p in p_tags])

    return MarketDataModel(title, desc, content, "News18")



def get_published_date(updated_date : str) -> date :
    # updated_Date is in this format - "Updated 2 days ago"
    updated_date = updated_date.replace("Updated", "").strip()
    updated_date = updated_date.replace("Published", "").strip()

    published_date = dateparser.parse(updated_date).date()
    return published_date
    