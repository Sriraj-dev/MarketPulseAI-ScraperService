from datetime import date, datetime
import json
from moneycontrol import store_moneycontrol_feeds
from businesstoday import store_businesstoday_feeds
from shared import produce_event_to_SQS


def lambda_handler(event,context):
    
    runDate_str = event.get('RunDate', None)
    
    # If runDate is not present in the event
    if not runDate_str:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: 'RunDate' is missing in the event.")
        }
    

    runDate : date = datetime.fromisoformat(runDate_str.replace("Z", "+00:00")).date()
    print("RunDate = ", runDate)
    store_moneycontrol_feeds(runDate)
    ##store other news feeds functions here
    store_businesstoday_feeds(runDate)

    produce_event_to_SQS(runDate)