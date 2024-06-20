import json
import os
import boto3
import tweepy
import random
from datetime import datetime, timezone, timedelta

# Initialize the SSM client
ssm = boto3.client('ssm', region_name='us-east-1')  

def get_secret(parameter_name):
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

# Fetch Twitter API credentials from Parameter Store
consumer_key = get_secret('/twitter/feral/consumer_key')
consumer_secret = get_secret('/twitter/feral/consumer_secret')
access_token = get_secret('/twitter/feral/access_token')
access_token_secret = get_secret('/twitter/feral/access_token_secret')
bearer_token = get_secret('/twitter/feral/bearer_token')

# Create client
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

# Authenticate using OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  
table = dynamodb.Table(os.environ['TABLE_NAME'])

def is_within_posting_hours():
    now_utc = datetime.now(timezone.utc)
    now_pst = now_utc - timedelta(hours=8)
    return 6 <= now_pst.hour < 24

def calculate_wait_time():
    wait_time = random.randint(60, 360) * 60
    now_utc = datetime.now(timezone.utc)
    now_pst = now_utc - timedelta(hours=8)
    next_run_time = now_pst + timedelta(seconds=wait_time)
    if 1 <= next_run_time.hour < 6:
        extra_wait = (6 - next_run_time.hour) * 60 * 60
        wait_time += extra_wait
    print(f"Calculated wait_time: {wait_time} seconds")
    return wait_time

def lambda_handler(event, context):
    if event.get('task') == 'calculate_wait_time':
        wait_time = calculate_wait_time()
        return {
            'statusCode': 200,
            'body': {
                'message': 'Wait time calculated.',
                'wait_time': wait_time
            }
        }
    
    wait_time = calculate_wait_time()
    if not is_within_posting_hours():
        return {
            'statusCode': 200,
            'body': {
                'message': 'Outside posting hours.',
                'wait_time': wait_time
            }
        }
    
    response = table.scan(
        FilterExpression='attribute_not_exists(posted) OR posted = :val1',
        ExpressionAttributeValues={':val1': False}
    )
    tweets = response['Items']
    
    if not tweets:
        return {
            'statusCode': 200,
            'body': {
                'message': 'No tweets to post.',
                'wait_time': wait_time
            }
        }
    
    tweet = tweets[0]
    client.create_tweet(text=tweet['tweet'])
    table.update_item(
        Key={'id': tweet['id']},
        UpdateExpression='SET posted = :val1, #ts = :val2',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={
            ':val1': True,
            ':val2': str(datetime.now())
        }
    )
    
    return {
        'statusCode': 200,
        'body': {
            'message': 'Tweet posted successfully!',
                'wait_time': wait_time
        }
    }