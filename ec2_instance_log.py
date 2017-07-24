import boto3
import json
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
def ec2_instance_log():
        session = boto3.session.Session()
        regions=session.get_available_regions('ec2')
        ses_con=boto3.client('ses',region_name='us-east-1')
        msg = MIMEMultipart()
        msg1 = MIMEMultipart()
        email={'arya' : 'arya@got.com','ned':'ned@got.com','jon':'jon@got.com'}   #Email list
	ins_run = MIMEMultipart()
        owner='root' #Name of the Owner
        root_account='ned'
        recipients=['tejprakash.sharma@tothenew.com']
        unamed_instances=[]
        part= MIMEText('Region Name --- Instance ID --- Instance Type --- Instance User')
        msg.attach(part)
        ins_run.attach(part)
        for region in regions:
                ec2_con = boto3.client('ec2', region_name=region)
                print region
                instances=ec2_con.describe_instances()
                cloudtrail_con = boto3.client('cloudtrail',region_name=region)
                for reservation in instances['Reservations']:
                        for instance in reservation['Instances']:
                                ins_run = MIMEMultipart()
                                part= MIMEText('Region Name --- Instance ID --- Instance Type --- Instance User')
                                ins_run.attach(part)
                                instance_id=instance['InstanceId'] #instance ID of the instance
                                instance_type=instance['InstanceType'] #instance Type of the instance
                                if instance['State']['Name'] == 'running': #check if instance is running
                                        print instance_id
                                        ct_details=cloudtrail_con.lookup_events(LookupAttributes=[{'AttributeKey':'ResourceName','AttributeValue': instance_id}])
                                        for event in ct_details['Events']: #Checking events inside ct_details is not empty
                                                CloudTrailEvent=json.loads(event['CloudTrailEvent'])
                                                username=event['Username']
                                                username=str(username)
                                                part = MIMEText(region+'--- '+instance_id+'---'+instance_type+'---'+username) #the BODY for the mail
                                                for name in email.keys():
                                                    if name == username:
                                                        ins_run['To'] = email[username]
                                                if username is None or username == root_account:
                                                        unamed_instances.append(instance_id)
                                                        part1 = MIMEText(region+'--- '+instance_id+'---'+instance_type+'---'+'Unamed instance') #the BODY for the mail
                                                        msg1.attach(part1)
                                                        break
                                                else:
                                                        if CloudTrailEvent['eventName'] == 'StartInstances' or CloudTrailEvent['eventName'] == 'RunInstances':
                                                                ec2_con.create_tags(Resources=[instance_id], Tags=[{'Key':'owner', 'Value':username},])
                                                                recipients.append(email[username])
                                                                break
                                        msg1.attach(part)
                                        ins_run.attach(part)   #attaching the body to the mail
                                        ins_run['Subject'] = 'EC2 Instances Currently in your Account' #SUBJECT for the mail
                                        ins_run['From'] = 'robb@got.com' #the SENDER of the mail
                                        result = ses_con.send_raw_email(RawMessage={'Data': ins_run.as_string() }, Source=ins_run['From'], Destinations=[ins_run['To']])
        msg1['Subject'] = 'EC2 Instances Currently Running with and without any Owner--TO THE NEW' #SUBJECT for the mail
        msg1['From'] = 'sansa@got.com' #the SENDER of the mail
        msg1['To'] = email[owner]

# and send the message
        result_msg1 = ses_con.send_raw_email(RawMessage={'Data': msg1.as_string() }, Source=msg1['From'], Destinations=[msg1['To']])

def lambda_handler(event, context):
    ec2_instance_log()

