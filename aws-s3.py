import boto3


s3_client = boto3.client('s3')
# response = s3_client.create_bucket(
#     ACL= 'private',
#     Bucket= "needle-45"
# )


# print("response===", response)


buckets = s3_client.list_buckets()

bucket_lists = [bucket['Name'] for bucket in buckets['Buckets']]

print("bucket-lists", bucket_lists)


results = s3_client.upload_file(r'C:\Users\Premkumar.8265\Desktop\aws\ngo_api_document.docx', 'needle-45', 'nsdl.docx')
