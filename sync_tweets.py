import os
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS credentials and DynamoDB table name from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
table_name = os.getenv('TABLE_NAME')
tweets_file_path = os.getenv('TWEETS_FILE_PATH')

# Initialize the DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
table = dynamodb.Table(table_name)

def get_tweets_from_file(file_path):
    with open(file_path, 'r') as file:
        tweets = file.read().split('⚽️')  # Split tweets by the soccer ball emoji delimiter
    return [tweet.strip() for tweet in tweets if tweet.strip()]

def upload_tweets_to_dynamodb(tweets):
    for tweet in tweets:
        tweet_id = str(datetime.now().timestamp())
        table.put_item(
            Item={
                'id': tweet_id,
                'tweet': tweet,
                'posted': False
            }
        )
    print(f"{len(tweets)} tweets uploaded to DynamoDB table {table_name}.")

def main():
    tweets = get_tweets_from_file(tweets_file_path)
    if tweets:
        upload_tweets_to_dynamodb(tweets)
    else:
        print("No tweets to upload.")

if __name__ == "__main__":
    main()
    
    







# import boto3
# import uuid

# # Initialize a session using Amazon DynamoDB
# session = boto3.Session(
#     aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
#     aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
#     region_name='us-east-1'
# )

# # Initialize DynamoDB resource
# dynamodb = session.resource('dynamodb')
# table = dynamodb.Table('TwitterAutomation')

# def read_tweets_from_file(file_path):
#     with open(file_path, 'r') as file:
#         tweets = file.readlines()
#     return [tweet.strip() for tweet in tweets if tweet.strip()]

# def add_tweet_to_dynamodb(tweet):
#     response = table.put_item(
#         Item={
#             'id': str(uuid.uuid4()),
#             'tweet': tweet,
#             'posted': False
#         }
#     )
#     return response

# def main():
#     tweets = read_tweets_from_file('tweets.txt')
#     for tweet in tweets:
#         response = add_tweet_to_dynamodb(tweet)
#         print(f'Added tweet: {tweet}, Response: {response}')

# if __name__ == "__main__":
#     main()
    
    








# import boto3
# from datetime import datetime

# def upload_tweet_to_lambda(tweet):
#     lambda_client = boto3.client('lambda')
#     response = lambda_client.invoke(
#         FunctionName='UploadTweet',
#         InvocationType='RequestResponse',
#         Payload=json.dumps({"tweet": tweet})
#     )
#     return response

# def process_tweets(file_path):
#     with open(file_path, 'r') as file:
#         tweets = file.read().split('⚽️')
#         for tweet in tweets:
#             if tweet.strip():
#                 upload_tweet_to_lambda(tweet.strip())

#     # Clear the content of the file
#     open(file_path, 'w').close()

# if __name__ == "__main__":
#     process_tweets('/path/to/tweets.txt')
    
    
    
    
    
    
    
    
    
    
# import boto3
# import uuid
# from datetime import datetime

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('TwitterAutomation')

# def process_tweet(tweet):
#     tweet_id = str(uuid.uuid4())
#     timestamp = str(datetime.now())

#     table.put_item(
#         Item={
#             'id': tweet_id,
#             'tweet': tweet,
#             'posted': False,
#             'timestamp': timestamp
#         }
#     )

# # Example usage
# tweet = "This is a sample tweet"
# process_tweet(tweet)