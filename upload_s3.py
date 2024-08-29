import json
import boto3

# AWS S3 Configuration
s3_client = boto3.client('s3')
bucket_name = 'needle-45'
s3_key = 'scraped_data123.json'

# Function to upload data to S3
def upload_to_s3(data):
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(data, indent=2))
    print(f"Uploaded data to {s3_key} in S3 bucket {bucket_name}")

# Read the JSON data from the file
file_path = r'C:\Users\Premkumar.8265\Desktop\aws\scraped_data.json'
with open(file_path, 'r') as file:
    new_data = json.load(file)

# Upload the data to S3
upload_to_s3(new_data)