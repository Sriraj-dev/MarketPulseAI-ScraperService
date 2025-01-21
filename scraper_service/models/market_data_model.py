
from dataclasses import dataclass

## We scrape the data from news websites in the following format .

@dataclass
class MarketDataModel:
    headline : str
    description : str
    content : str
    author : str # news websites name / blogs author name


