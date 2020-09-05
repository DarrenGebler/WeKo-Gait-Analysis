import boto3
from urllib.parse import unquote_plus

BUCKET_NAME = "gait-analysis"
CONFIG_FILE_KEY = "config/ec2-launch-config.json"
BUCKET_INPUT_DIR = "input"
BUCKET_OUTPUT_DIR = "output"


def lambda_handler(raw_event, context):
    """
    Main function call when file is uploaded to gait-analysis/input folder

    :param raw_event: Event that occured
    :param context: Methods and properties of Lambda
    :return: Dictionary of Instance states
    """

    # Used for Cloudwatch debugging
    print(f"Received raw event: {raw_event}")

    # Loops through all events that triggered Lambda
    for record in raw_event['Records']:
        # Bucket that triggered Lambda
        bucket = record['s3']['bucket']['name']
        print(f"Triggering S3 Bucket: {bucket}")

        # File that triggered Lambda
        key = unquote_plus(record['s3']['object']['key'])
        print(f"Triggering key in S3: {key}")

        # Set EC2 filters to check for existing Instance
        ec2_filters = [
            {
                'Name': "tag:Purpose",
                'Values': ['data-processing']
            }
        ]

        # Initialise boto3 s3 to copy file from input folder to processing folder
        S3 = boto3.resource('s3')
        copy_source = {
            'Bucket': f'{BUCKET_NAME}',
            'Key': f'{key}'
        }

        # Copy file
        video_name = key.replace('input/', '')
        bucket = S3.Bucket(f'{BUCKET_NAME}')
        bucket.copy(copy_source, f'processing/{video_name}')

        # Initialise boto3 ec2
        EC2 = boto3.client('ec2', region_name="ap-southeast-2")
        print("[DEBUG] Copied and created boto3 client")
        print("[INFO] Describing EC2 instances with target tags...")

        # Returns all instances with ec2_filters target tags
        resp = EC2.describe_instances(Filters=ec2_filters)

        # Checks if instance has been created
        if resp["Reservations"] is not []:  # at least one instance with target tags was found
            # Loops through all instances with target tags. Should only ever be one
            for reservation in resp["Reservations"]:
                for instance in reservation["Instances"]:
                    # Used for Cloudwatch debugging
                    print(f"[INFO] Found '{instance['State']['Name']}' instance '{instance['InstanceId']}'"
                          f" having target tags: {instance['Tags']} ")

                    # Instance found in stopped state. Start instance
                    if instance['State']['Code'] == 80:
                        print(f"[INFO] instance '{instance['InstanceId']}' has stopped: starting instance")
                        result = EC2.start_instances(InstanceIds=["i-06b5a6f33be47f482"])

                    # Instance has target tags AND also is in running state
                    if instance['State']['Code'] == 16 or instance['State']['Code'] == 0:
                        print(
                            f"[INFO] instance '{instance['InstanceId']}' is already running: so not doing anything")
                        return {
                            "newInstanceLaunched": False,
                            "old-instanceId": instance['InstanceId'],
                            "new-instanceId": ""
                        }

