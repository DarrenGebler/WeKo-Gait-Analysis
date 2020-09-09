import boto3
from urllib.parse import unquote_plus

def lambda_handler(raw_event, context):
    print("LogScheduledEvent")
    print(f"Received raw event: {raw_event}")

    ec2_filters = [
        {
            'Name': "tag:Purpose",
            'Values': ['data-processing']
        }
    ]

    S3 = boto3.client('s3')
    response = S3.list_objects(Bucket='gait-analysis', Prefix='processing', MaxKeys=10)
    files = len(response['Contents'])

    EC2 = boto3.client('ec2', region_name="ap-southeast-2")
    resp = EC2.describe_instances(Filters=ec2_filters)

    if resp["Reservations"] is not []:
        for reservation in resp["Reservations"]:
            for instance in reservation["Instances"]:
                print(f"[INFO] Found '{instance['State']['Name']}' instance '{instance['InstanceId']}'"
                      f" having target tags: {instance['Tags']} ")

                if instance['State']['Code'] == 80 and files > 1:
                    print(f"[INFO] instance '{instance['InstanceId']}' has stopped and there are files"
                          f" in the processing folder: starting instance")
                    result = EC2.start_instances(InstanceIds=["i-06b5a6f33be47f482"])