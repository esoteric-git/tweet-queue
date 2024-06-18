import json
import boto3
import tweepy
import random
from datetime import datetime, timezone, timedelta

# Initialize the SSM client
ssm = boto3.client('ssm', region_name='your-region')  # Replace 'your-region' with your actual AWS region

def get_secret(parameter_name):
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

# Fetch Twitter API credentials from Parameter Store
consumer_key = get_secret('/twitter/consumer_key')
consumer_secret = get_secret('/twitter/consumer_secret')
access_token = get_secret('/twitter/access_token')
access_token_secret = get_secret('/twitter/access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dynamodb = boto3.resource('dynamodb', region_name='your-region')  # Replace 'your-region' with your actual AWS