import json
import boto3
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Create an SSM Client to access parameter store
ssm = boto3.client('ssm')

# Define the function
def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event: " + json.dumps(event, indent=2))
        
        # Check if 'Records' key exists in the event
        if 'Records' not in event or not event['Records']:
            raise KeyError("The event does not contain 'Records'.")
        
        # Check if 'Sns' key exists in the first record
        if 'Sns' not in event['Records'][0]:
            raise KeyError("The first record does not contain 'Sns'.")
        
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        # Extract relevant information from the message
        alarm_name = message['AlarmName']
        new_state = message['NewStateValue']
        reason = message['NewStateReason']
        aws_account_id = message['AWSAccountId']
        alarm_timestamp = message['AlarmConfigurationUpdatedTimestamp']
        namespace = message['Trigger']['Namespace']
        
        # Determine the type of message based on the alarm state
        if new_state == "ALARM":
            color = 'danger'
            state_icon = ':fire:'
            state_text = "*Alert Triggered*"
        elif new_state == "OK":
            color = 'good'
            state_icon = ':white_check_mark:'
            state_text = "*Incident Resolved*"
        
        slack_message = {
            'attachments': [
                {   
                    'color': color,
                    'text': f'{state_text} {state_icon}\n'
                            f'*Namespace:* {namespace}\n'
                            f'*Alarm Name:* {alarm_name}\n'
                            f'*AWS Account ID:* {aws_account_id}\n'
                            f'*Alarm Configuration Updated Timestamp:* {alarm_timestamp}\n'
                            f'*New State:* {new_state}\n'
                            f'*Reason:* {reason}',
                }
            ]
        }
        
        # Retrieve webhook URL from parameter store
        parameter = ssm.get_parameter(Name='SLACK_WEBHOOK_URL', WithDecryption=True)
        webhook_url = '-------'
        
        # Log the webhook URL for debugging
        print(f"Webhook URL: {webhook_url}")
        
        # Make request to the Slack API
        req = Request(webhook_url, json.dumps(slack_message).encode('utf-8'))
        
        try:
            response = urlopen(req)
            response.read()
            print("Message posted to Slack")
        except HTTPError as e:
            print(f'Request failed: {e.code} {e.reason}')
        except URLError as e:
            print(f'Server Connection failed: {e.reason}')
    
    except KeyError as e:
        print(f"KeyError: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
