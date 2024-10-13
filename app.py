########### Gen AI using AWS Bedrock ###########
import json

#to invoke foundation models
import boto3
import botocore.config
from datetime import datetime

#credit
"""
Krish Naik Gen AI using AWS Demo 
https://www.youtube.com/watch?v=3OP39y4dO_Y&list=PLZoTAELRMXVP5zpBfH7pab4aB1LbmCM1z&index=5


"""

def blog_generation_using_bedrock(blogtopic: str) -> str:
    prompt = f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
                          Assistant:[/INST]
                """
    body = {
        "prompt": "this is where you place your input text",
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }

    try:
        bedrock = boto3.client("bedrock-runtime",
                               region_name="us-east-1",
                               config=botocore.config.Config(read_timout=300, retries={'max_attempts': 3})
                               )
        bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama3-8b-instruct-v1:0")

        response_content = response.get('body').read()

        response_data = json.loads(response_content)

        print(response_data)

        blog_details = response_data['generation']

        return blog_details

    except Exception as e:
        print(f"Error generating the blog: {e}")
        return ""


#Saving code to S3
def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, key=s3_key, Body=generate_blog)
        print("Code saved to s3 ")
    except Exception as e:
        print("Error when saving code to s3")


#lambda handler to call bedrock and save the blog in s3
def lambda_handler(event, context):
    event = json.loads(event['body'])
    blogtopicname = event['blog_topic']

    generate_blog = blog_generation_using_bedrock(blogtopic=blogtopicname)

    if generate_blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = "aws_bedrock_course1"
        save_blog_details_s3(s3_bucket, s3_key, generate_blog)

    else:
        print('No blog was generated')

    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is Complete!!')
    }
