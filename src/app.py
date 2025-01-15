import os
import json
import logging
import datetime

import boto3 # type: ignore
import nltk    # type: ignore
from nltk.tokenize import sent_tokenize # type: ignore

dynamo_table_name = os.environ.get('MyDynamoTable', 'DefaultTableName')
# Set the NLTK data path to the local directory that contains nltk_data/
nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# In-memory cache
CACHE = {}

def calculate_summary(results):
    """
    Summarize the sentiment analysis results.
    """
    try:
        overall_sentiment = max(
            ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED'],
            key=lambda s: sum(result['SentimentScore'][s.capitalize()] for result in results)
        )
        confidence = sum(result['SentimentScore'][overall_sentiment.capitalize()] for result in results) / len(results)
        return {'overall_sentiment': overall_sentiment, 'confidence': round(confidence, 2)}
    except Exception as e:
        logger.error(f"Error calculating summary: {e}", exc_info=True)
        return {'overall_sentiment': 'UNKNOWN', 'confidence': 0.0}

def lambda_handler(event, context):
    """
    Main Lambda function handler.
    """
    logger.info(f"Received event: {event}")

    comprehend = boto3.client('comprehend')
    try:
        # Ensure 'body' key exists in the event
        if 'body' not in event:
            logger.error("Missing 'body' in event")
            return {'statusCode': 400, 'body': json.dumps({'error': "Missing 'body' in request"})}

        body = json.loads(event['body'])
        text = body.get('text', '')

        # Check if text was provided
        if not text:
            logger.error("Text input is missing")
            return {'statusCode': 400, 'body': json.dumps({'error': 'Text input is required'})}

        # Check cache for the text
        if text in CACHE:
            logger.info("Cache hit for text")
            cached_response = CACHE[text]
            return {'statusCode': 200, 'body': json.dumps({'cached': True, **cached_response})}

        # Detect the dominant language of the input text
        logger.info("Calling detect_dominant_language...")
        language_response = comprehend.detect_dominant_language(Text=text)
        logger.info(f"Language detection response: {language_response}")

        if not language_response.get('Languages'):
            logger.error("No languages detected")
            return {'statusCode': 400, 'body': json.dumps({'error': 'Unable to detect language of the input text'})}

        # Extract the dominant language
        language_code = language_response['Languages'][0]['LanguageCode']
        logger.info(f"Detected language: {language_code}")

        # Split text into sentences
        logger.info("Tokenizing text into sentences...")
        sentences = sent_tokenize(text)
        logger.info(f"Sentences: {sentences}")

        # Perform sentiment analysis for each sentence
        results = []
        for sentence in sentences:
            sentiment_response = comprehend.detect_sentiment(Text=sentence, LanguageCode=language_code)
            logger.info(f"Sentiment for sentence: {sentiment_response}")
            results.append(sentiment_response)

        # Summarize sentiment across all sentences
        summary = calculate_summary(results)

        # Build response
        response = {
            'language': language_code,
            'results': results,
            'summary': summary,
            'timestamp': datetime.datetime.now().isoformat(),
            'request_id': context.aws_request_id
        }

        # Cache the response
        CACHE[text] = response
        logger.info("Response cached successfully")

        return {'statusCode': 200, 'body': json.dumps({'cached': False, **response})}

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'error': 'An error occurred during processing.'})}