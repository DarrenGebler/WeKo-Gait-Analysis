############################
WeKo's Gait Analysis Project
############################

Documentation on the Gait Analysis Project developed by the QUT 2020 Capstone team RAD^2.
This documentation will describe all the necessary steps used to get the project up and running.
It will not describe building the initial database of user videos, as this will
be able to be done on the AWS EC2 Instance. It should be noted, that you will need access
to an AWS account with sufficient credits, as the EC2 instance we will be using does cost money
to run.

Requirements
============

* Access to an AWS account with sufficient credits
* Install SSH Client (recommended https://mobaxterm.mobatek.net/download.html)

Setup AWS
=========
S3 Bucket
---------
To setup the S3 Bucket, follow the steps below:

1. On the AWS Management Console page, under Storage select 'S3'

2. Press 'Select Bucket' and set the bucket name and your preferred region

3. Click 'Next' 2 times, then un-tick 'Block all public access' and confirm. Press 'Next' again and then 'Create Bucket'

4. Navigate to the bucket you created and create 7 folders named; 'config', 'input', 'output', 'output_keypoints', 'output_keypoints_abnormal', 'output_videos', 'processing'

5. Under 'Permissions', select 'Bucket Policy' then copy and paste the following code, changing the BUCKET_NAME to your bucket name

.. code-block:: JSON

    {
        "Version": "2012-10-17",
        "Id": "Policy1597987556023",
        "Statement": [
            {
                "Sid": "Stmt1597987554594",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:PutObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": "arn:aws:s3:::BUCKET_NAME/*"
            }
        ]
    }

6. Select 'CORS configuration' then copy and paste the following code

.. code-block:: XML

    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
    </CORSConfiguration>

Your S3 bucket is now setup. IAM Roles have to be created to allow different services
to access the bucket.

IAM Roles
---------
EC2 Role
*********
To setup the correct IAM Roles for the EC2, follow the steps below:

1. On the AWS Management Console page, under Security, Identity, & Compliance select 'IAM'

2. Press 'Roles', then 'Create role'

3. Find 'EC2', then press 'Next: Permissions'

4. Search for 'AmazonS3FullAccess' and select

5. Click 'Review policy' and name your policy. Remember the name you entered.

6. Click 'Next' until you get to Review

7. Enter a role name and click 'Create role'. Remember the name you entered.


EC2
---
Launching
*********
To launch the EC2 instance, follow the steps below:

1. On the AWS Management Console page, under Compute select 'EC2'

2. Select 'Launch instance'

3. Search for 'Deep Learning AMI (Ubuntu 18.04)' and select

4. Filter instance types to GPU instances and select 'g4dn.xlarge' and press 'Next: Configure Instance Details'

5. Under 'IAM role' select the IAM policy name you created above

6. Click 'Next: Add Storage'

7. Un-tick 'Delete on Termination' and click 'Review and Launch'

8. Click 'Launch'

9. From the drop down menu, select 'Create a new key pair' and enter a key pair name. Remember the name you entered.

10. Download the key pair and keep it somewhere safe.

11. Click 'Launch Instances'

Setting up
**********
To setup the EC2 Instance, follow the steps below:

1. Open MobaXterm and click 'Session' at the top left, then SSH

2. On the AWS EC2 Instances page, select your instance and click 'Actions', 'Instance Settings' and then 'View/Change User Data'

3. Input the following code and press save

.. code-block:: XML

    #!/bin/bash
    python3 EC2Prediction.py

4. Start the EC2 Instance you created

5. Copy the 'Public DNS (IPv4)' address and paste it in the Remote host box in MobaXterm

6. Check 'Specify username' and input 'Ubuntu'

7. Open 'Advanced SSH settings', tick 'Use private key' and find the key pair file you downloaded above

8. Click 'Ok' and you will be presented a SSH window (black box) with a SFTP on the left

9. In the SSH window, type the following command

.. code-block:: XML

    cd ../../etc/cloud/ && sudo nano cloud.cfg

10. Scroll down until you see '# cloud-config' and change the following line from

.. code-block:: XML

    - scripts-user

to

.. code-block:: XML

    - [scripts-user, always]

11. Press 'CTRL+S', then 'CTRL+X' and type the following command

.. code-block:: XML

    cd ~ && mkdir processing data && mkdir data/output && mkdir data/output/poses

12. Using the SFTP viewer on the left, copy the file; 'gait_analysis_model_iso_ec2.sav', 'EC2Prediction.py', 'SMTPEmail.py' and 'UserDatabase.py' and enter the following command

.. code-block:: XML

    userdata.txt && sudo mv EC2Prediction.py ../.. && sudo mv SMTPEmail.py ../.. && sudo mv UserDatabase.py ../..

The EC2 instance is setup. A Lambda function will now be setup to link everything together and automate the pipeline.

Lambda
------

To setup the Lambda function, follow the steps below:

1. On the AWS Management Console page, under Compute select 'Lambda'

2. Select 'Create function', give your function a name and select the Runtime language to 'Python 3.8'

3. Click 'Add trigger' and select 'S3' from the drop down list

4. Find the S3 bucket you created above, set the Event type to 'All object create events' and the Prefix to 'input/'. Click 'Add'

5. In the 'Function code' area, copy and paste the following source code

.. literalinclude:: ../../src/Lambda.py