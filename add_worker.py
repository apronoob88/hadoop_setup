### to be execute on the current base image running automation script

import boto3
from botocore.exceptions import ClientError
from scp import SCPClient
import paramiko
import time
import os


key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")

cluster_name = input("please enter the name of you cluster: ")
key_name = input("please enter the key pair name(without .pem) to lauch the cluster: ")
number_to_add = int(input("please enter the number of nodes to add (we strongly encourage you to add one at a time): "))

os.environ['AWS_ACCESS_KEY_ID'] = key
os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
os.environ['AWS_SESSION_TOKEN'] = session_token

ec2_key = key_name +".pem"


ec2_client = boto3.client('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secrete_key,
    aws_session_token= session_token,
    region_name='us-east-1')

pkey = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


flintrock_manager_filter = [{
    'Name':'tag:Name', 
    'Values': [f'flintrock_manager_{cluster_name}']}]

response_flintrock_manager = ec2_client.describe_instances(Filters=flintrock_manager_filter)

flintrock_manager_ip = ''
# place safe there, check if indeed only 1 instance of master node returned, the length are almost always 1
if len(response_flintrock_manager['Reservations']) != 1:
    print('either 0 or multiple master node exists')
    exit()
    if len(response_flintrock_manager['Reservations'][0]['Instances']) != 1:
        print('either 0 or multiple master node exists')
        exit()
else:
    flintrock_manager_ip = response_flintrock_manager['Reservations'][0]['Instances'][0]['PublicIpAddress']


os.environ['AWS_ACCESS_KEY_ID'] = key
os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
os.environ['AWS_SESSION_TOKEN'] = session_token

# Connect/ssh to mongodb instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    ssh_client.connect(hostname=flintrock_manager_ip, username="ec2-user", pkey=pkey)

    cmd = f'python3 add_node.py {cluster_name} {key_name} {number_to_add} {key} {secrete_key} {session_token}'

    print(f"Adding in a node. This may take a while....")
    print(cmd)
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read())
    print(stderr.read())



except Exception as e:
    print (e)