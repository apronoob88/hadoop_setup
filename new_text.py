import boto3
from botocore.exceptions import ClientError
import paramiko
import time
import os
import datetime
def get_mastermode_ip(ec2_client,tagname):
    master_tagname = tagname + '-master'
    masternodes = []
    
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name':'tag:Name',
                'Values': [
                    master_tagname
                ]
            }
        ]
    )

    for instance in response['Reservations']:
        print('Reservation: ',instance)
        for i in instance['Instances']:
            print('Instances: ', i)
            if i['State']['Name'] == 'running':
                masternodes.append(i)

    if len(masternodes) == 1:
        public_ip = masternodes[0]['PublicIpAddress']
        key_name = masternodes[0]['KeyName']
        #print('\033[1m'+'\033[95m'+'Public ip for masternode: ',public_ip)
        #print('Key required: {}.pem'.format(key_name)+'\033[0m')

        return public_ip,key_name
    else:
        print("Alarm: There are more than 1 or no master node on this ec2 instance!")

key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")

ec2_client = boto3.client('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secrete_key,
    aws_session_token= session_token,
    region_name='us-east-1')

cluster_name = 'hadoop-cluster3'
tagname = 'hadoop-cluster3'
#master_ip, master_key = get_mastermode_ip(ec2_client,tagname)
# print(master_ip)
# print(master_key)



# get masternode ip address
master_filter = [{
    'Name':'tag:Name', 
    'Values': [f'{cluster_name}-master']}]

response = ec2_client.describe_instances(Filters=master_filter)

master_node_ip = ''
# place safe, chack if indeed only 1 instance of master node returned, mostt of cases it will be 1
if len(response['Reservations']) != 1:
    print('either 0 or multiple master node exists')
    exit()
    if len(response['Reservations'][0]['Instances']) != 1:
        print('either 0 or multiple master node exists')
        exit()
else:
    master_node_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print(master_node_ip)



