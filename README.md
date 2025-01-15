Serverless Sentiment Analysis API

A serverless, Python-powered application that uses AWS Lambda, Amazon API Gateway, Amazon S3 and Amazon Comprehend to determine the sentiment (Positive, Negative, Neutral, or Mixed) of any given text. This project demonstrates how to build, deploy, and scale a sentiment analysis service without managing servers—and often at little to no cost under the AWS Free Tier.

Table of Contents
	1.	Project Overview
	2.	Features
	3.	Use Cases
	4.	Architecture
	5.	Prerequisites
	6.	Setup Instructions
	7.	Deployment with AWS SAM
	8.	Usage
	9.	Additional Enhancements
	10.	Logging and Monitoring
	11.	Cleanup
	12.	Contributing
	13.	License

1. Project Overview

This Serverless Sentiment Analysis API leverages Amazon Comprehend to detect sentiment in user-provided text. It can handle simple, single-sentence input or multi-sentence paragraphs, automatically detect the input language, and cache repeated requests. By using Infrastructure as Code (AWS SAM), you can deploy and manage this API with ease, keeping infrastructure costs minimal.

2. Features
	1.	Single & Multi-Sentence Analysis
	•	Utilizes NLTK to split text and analyzes each sentence independently.
	2.	Language Detection
	•	Identifies the dominant language via Amazon Comprehend before sentiment analysis.
	3.	Caching
	•	Reduces redundant API calls by storing previously computed results in an in-memory cache (within the same Lambda execution context).
	4.	Sentiment Summary
	•	Aggregates sentiment scores across multiple sentences to provide an overall sentiment rating and confidence.
	5.	Logging & Metadata
	•	Includes timestamps, request IDs, and logs to Amazon CloudWatch for debugging and analytics.
	6.	Scalability & Free Tier Compatibility
	•	Runs entirely on serverless services, so you can scale automatically while paying only for what you use.

3. Use Cases
	•	Customer Feedback: Analyze product reviews or feedback forms to gauge customer sentiment.
	•	Social Media Analysis: Process tweets, comments, or posts for brand sentiment in real time.
	•	Email & Support Tickets: Automatically classify incoming messages to determine urgency and tone.
	•	Market Research: Collect and interpret consumer feedback or survey responses with minimal overhead.

4. Architecture

Client → API Gateway → Lambda (app.py) → Amazon Comprehend
                      → Amazon CloudWatch (Logs)

	1.	API Gateway
Exposes a RESTful endpoint (POST /analyze-sentiment).
	2.	Lambda
A Python function that receives requests, invokes Amazon Comprehend for sentiment analysis, and returns a result.
	3.	Amazon Comprehend
Provides the core Natural Language Processing (NLP) capabilities like sentiment detection and language identification.
	4.	Amazon CloudWatch Logs
Collects logs for performance monitoring, debugging, and analytics.

5. Prerequisites
	1.	AWS Account
	•	Sign up for AWS Free Tier.
	2.	AWS CLI (configured)
	•	Install the AWS CLI and run aws configure to set up your credentials.
	3.	AWS SAM CLI
	•	Install from the AWS SAM docs.
	4.	Python 3.9+
	•	Ensure Python and pip are installed.
	5.	Virtual Environment (Recommended)
	•	Create one via python -m venv venv and activate it.

6. Setup Instructions
	1.	Clone or Download the Repo

git clone https://github.com/sanjojoys/Serverless_sentiment_analysis.git
cd Serverless_sentiment_analysis


	2.	Project Structure

Serverless_sentiment_analysis/
├── src/
│   ├── app.py
│   └── requirements.txt
├── template.yaml
├── README.md
└── .gitignore


	3.	Install Dependencies

cd src
pip install -r requirements.txt
cd ..


	4.	(Optional) NLTK Data
	•	If using multi-sentence analysis or special language tokenizers, ensure you have local nltk_data or package it in your deployment.

7. Deployment with AWS SAM
	1.	Build

sam build


	2.	Deploy

sam deploy --guided

	•	Provide a stack name (e.g., sentiment-analysis-api).
	•	Choose your region.
	•	Accept defaults if unsure.

	3.	Endpoint
	•	After deployment, note the API Gateway endpoint that SAM prints out.

8. Usage

8.1 Single-Sentence Request
      
      curl -X POST -H "Content-Type: application/json" \
           -d '{"text": "I love AWS!"}' \
           <API_ENDPOINT>

Sample Response:

      {
        "Sentiment": "POSITIVE",
        "SentimentScore": {
          "Positive": 0.99,
          "Negative": 0.01,
          "Neutral": 0.00,
          "Mixed": 0.00
        }
        ...
      }

8.2 Multi-Sentence Request

      curl -X POST -H "Content-Type: application/json" \
           -d '{"text": "I love AWS. The weather is great today."}' \
           <API_ENDPOINT>

Sample Response (truncated):

      {
        "results": [
          {
            "Sentiment": "POSITIVE",
            "SentimentScore": { ... }
          },
          {
            "Sentiment": "POSITIVE",
            "SentimentScore": { ... }
          }
        ]
      }

8.3 Language Detection

If enabled, your response will include a "language" field, for instance "language": "en".

8.4 Caching

If caching is activated, repeated requests with the same text return:

      {
        "cached": true,
        "result": {
           ...
        }
      }

9. Additional Enhancements
	1.	API Key Authentication
Require an API Key in API Gateway to restrict who can call your endpoint.
	2.	Parameter Store
Store secrets or environment variables securely in AWS Systems Manager.
	3.	CI/CD Pipeline
Automate builds and deployments with GitHub Actions or AWS CodePipeline.
	4.	Detailed Logging & Tracing
Use structured logging and AWS X-Ray for deeper insights.
	5.	Response Transformation
Include additional metadata like timestamps, request IDs, or debug info in your JSON output.

10. Logging and Monitoring
	•	Amazon CloudWatch Logs
Each Lambda invocation logs data here. Check your function’s Log Group to debug or view performance metrics.
	•	AWS X-Ray (Optional)
Trace requests in detail across your serverless architecture.


This project is licensed under the MIT License. See the LICENSE file for more details.
