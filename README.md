
EC2_INSTANCE_LOG Script:

A lot of our accounts in AWS have multiple IAM users created. As a result, sometimes a lot of instances are created by those IAM users and are kept running. So to avoid such situation I have created a python script which checks any running instances in the account. The script uses Cloudtrail to find out which account started the instance. I have also used Lambda and SES to send a mail to the owner of Account. 

Prerequisites for running the script:
1. The script needs a dictionary(email) of users consisting of the IAM user name and the email ID of the user. For reference see line number 12 in the script attached below.
2. All the values in the 'email' should be verified via SES.
3. We also need to provide the 'owner' as well the 'root_account' of the AWS account. This may be same in some cases. The value of 'owner' should be point to the user be present in the 'email' dict created above.
4. You also need to change the 'msg1['From']' value. it the email from which we receive the emails. This email should also be verified via SES.
5. The policy required to run the below script is also attached. 

The script also creates a tag with a key as 'owner' and the value as the IAM user who launched the instance. 


