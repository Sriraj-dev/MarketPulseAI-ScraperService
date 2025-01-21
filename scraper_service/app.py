import datetime
import json
from moneycontrol import store_moneycontrol_feeds
from shared import produce_event_to_SQS


def lambda_handler(event,context):

    runDate_str = event.get('RunDate', None)
    
    # If runDate is not present in the event, handle it gracefully
    if not runDate_str:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: 'RunDate' is missing in the event.")
        }
    

    runDate : datetime = datetime.datetime.fromisoformat(runDate_str.replace("Z", "+00:00")).date()
    print("RunDate = ", runDate)
    store_moneycontrol_feeds(runDate)
    ##store other news feeds functions here

    produce_event_to_SQS(runDate)



    
## For triggering the next processing function.
# Resources:
#   ProcessingServiceFunction:
#     Type: AWS::Serverless::Function
#     Properties:
#       Handler: app.lambda_handler
#       Runtime: python3.9
#       CodeUri: .
#       Events:
#         SQSTrigger:
#           Type: SQS
#           Properties:
#             Queue: arn:aws:sqs:region:account-id:queue-name
