# Base URLs
MONEYCONTROL_BASE_URL = "https://www.moneycontrol.com/news/business/stocks/"
BUSINESSTODAY_BASE_URL = "https://www.businesstoday.in/markets/stocks"
ECONOMIC_TIMES_BASE_URL = "https://economictimes.indiatimes.com/markets/stocks/news"
NEWS18_BASE_URL = "https://www.news18.com/business/markets/"

# AWS Configurations
S3_BUCKET_NAME = "market-pulse-ai"
SQS_URL = "https://sqs.us-east-1.amazonaws.com/829982859440/stockdataupdates.fifo"
SQS_NAME = "stockdataupdates.fifo"
AWS_REGION = "us-east-1" ##TODO : should change to ap-south-1
SCRAPED_DATA_DIRECTORY_NAME = "scraped_data/"

# Date Format
DATE_FORMAT = "%Y-%m-%d"



