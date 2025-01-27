from shared import BUSINESSTODAY_BASE_URL,upload_to_s3
from bs4 import BeautifulSoup
from datetime import date,datetime
import requests
from models import MarketDataModel

def store_businesstoday_feeds(rundate : date):
    print("Collecting data from business today website")
    feed_data = scrape_news_data(rundate)

    print("Data Collected from Business today, No.Of Blogs Collected : " , feed_data.__len__())
    upload_to_s3("businesstoday", feed_data, rundate)


def scrape_news_data(rundate : date):
    response = requests.get(BUSINESSTODAY_BASE_URL)

    if(response.status_code != 200):
        print("Error in scraping data from businesstoday.com")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tags = soup.find_all('div', class_ = 'widget-listing')

    listings : list[MarketDataModel] = []
    for div in div_tags:
        title_tag = div.find('h2').find('a')
        updated_date_tag = div.find('span')
        link = title_tag['href'] if title_tag else None
        updated_date = get_blog_date(updated_date_tag.text.strip()) if updated_date_tag else None

        if(updated_date < rundate): break

        if(updated_date == rundate):
            listings.append(scrape_blog_content(link, rundate))
    
    return listings


def scrape_blog_content(link : str, rundate : date):
    print("Collecting data from - " , link)
    response = requests.get(link)

    if(response.status_code != 200):
        print("Error in scraping data from Business Today blogs")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    heading_tag = soup.find_all('div', class_ = 'story-heading headline', limit=1)
    desc_tag = soup.find_all('div', class_ = 'sab-head-tranlate-sec summary',limit=1)
    author_tag = soup.find_all('div', class_ = 'usericons', limit=1)

    title = heading_tag[0].find('h1').text.strip() if heading_tag else None
    description = desc_tag[0].find('h2').text.strip() if desc_tag else None
    author = author_tag[0].find("img")["title"] if author_tag else None

    p_tags = soup.find_all('p')
    content = ' '.join([p.text.strip() for p in p_tags])

    return MarketDataModel(title, description, content, author)



def get_blog_date(updated_date : str):
    date_str = updated_date.replace("Updated", "").strip()
    date_str = date_str.replace(":","").strip()

    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    return date_obj.date()

