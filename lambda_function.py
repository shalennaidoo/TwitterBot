import os
import random
import boto3
from botocore.exceptions import ClientError
import tweepy
import openai

BUCKET_NAME = os.environ['BUCKET_NAME']
KEY = 'data.txt'

s3 = boto3.resource('s3')
ssm = boto3.client('ssm')


def get_parameter(param_name):
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    credentials = response['Parameter']['Value']
    return credentials


def get_book_title():
    filename = '/tmp/' + KEY
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, filename)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f'The object {KEY} does not exist in bucket {BUCKET_NAME}.')
        else:
            raise

    with open(filename) as f:
        lines = f.readlines()
        return random.choice(lines)


def lambda_handler(event, context):

    # Get SSM parameters
    CONSUMER_KEY = get_parameter('/TwitterBot/consumer_key')
    CONSUMER_SECRET = get_parameter('/TwitterBot/consumer_secret')
    ACCESS_TOKEN = get_parameter('/TwitterBot/access_token')
    ACCESS_TOKEN_SECRET = get_parameter('/TwitterBot/access_token_secret')

    # Set up the OpenAI API client
    openai.api_key = get_parameter('/TwitterBot/OPENAPI_API_KEY')


    # Get Book Title
    bookTitle = get_book_title()
    print(bookTitle)

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = "Please summarize the following book ascertaining that your response summary is at most 250 characters: " + bookTitle

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    
    #Append Book Title to response
    response += bookTitle

    client = tweepy.Client(consumer_key=CONSUMER_KEY,
                        consumer_secret=CONSUMER_SECRET,
                        access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_TOKEN_SECRET)

    #Post Tweet
    response = client.create_tweet(text=response)
    print(response)