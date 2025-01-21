import requests
from models import MarketDataModel
from bs4 import BeautifulSoup
import json
import datetime
from shared import upload_to_s3, MONEYCONTROL_BASE_URL

## Scrape the data from moneycontrol.com
### It is a static website and hence beautifulSoup can be used to get the scraped data.

def store_moneycontrol_feeds(runDate : datetime):
    moneycontroldata = scrape_moneycontrol(runDate)
    print("Collected data from moneycontrol.com")
    print("No. of blogs collected - ", moneycontroldata.__len__())
    upload_to_s3("moneycontrol", moneycontroldata, runDate)



def scrape_moneycontrol(runDate : datetime):

    response = requests.get(MONEYCONTROL_BASE_URL)

    if(response.status_code != 200):
        print("Error in scraping data from moneycontrol.com")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tags = soup.find_all('script', type = 'application/ld+json')
    
    blogs = []

    for script_tag in script_tags:
        try:
            data = json.loads(preprocess_string(script_tag.string))

            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "ItemList":
                        blogs = item.get("itemListElement")
            
            elif isinstance(data, dict):
                if data.get("@type") == "ItemList":
                    blogs = data.get("itemListElement")
        
        except json.JSONDecodeError:
            print("Error decoding JSON")
            continue;

    return scrape_blog_content(blogs, runDate)



def scrape_blog_content(blogs : list, runDate : datetime):
    scraped_news_data : list[MarketDataModel] = [];
    isdone = False;
    for blog in blogs:
        blogUrl = blog.get("url")
        print("Collecting data from - " , blogUrl)
        blogResponse = requests.get(blogUrl)
        blogSoup = BeautifulSoup(blogResponse.text, 'html.parser')
        script_tags = blogSoup.find_all('script', type = 'application/ld+json')
        
        for script_tag in script_tags:
            try:
                data = json.loads(preprocess_string(script_tag.string))

                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") == "NewsArticle":
                            dateModified = datetime.datetime.fromisoformat(item.get("dateModified")).date()
                            if(dateModified == runDate): scraped_news_data.append(build_market_data_model(item))
                            else: 
                                if(dateModified < runDate): isdone = True
                                break;

                elif isinstance(data, dict):
                    if data.get("@type") == "NewsArticle":
                        dateModified = datetime.datetime.fromisoformat(item.get("dateModified")).date()
                        if(dateModified == runDate): scraped_news_data.append(build_market_data_model(data))
                        else: 
                            if(dateModified < runDate): isdone = True
                            break;
            
            except json.JSONDecodeError:
                print("Error decoding Loop JSON")
        if(isdone): break

    return scraped_news_data


def build_market_data_model(blog : dict):
    headline = blog.get("headline","")
    description = blog.get("description","")
    content = blog.get("articleBody","")
    author = blog.get("author",{}).get("name","")
    #date_published = datetime.datetime.fromisoformat(blog.get("datePublished", datetime.datetime.now())).date().strftime("%Y-%m-%d")
    #url = blog.get("url")
    return MarketDataModel(headline, description, content, author)


def preprocess_string(json_string : str):
    json_string = json_string.replace("\n", " ").replace("\r", " ")

    return json_string