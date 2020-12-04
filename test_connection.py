import boto3
from botocore.exceptions import ClientError
from scp import SCPClient
import paramiko
import time
import os

key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")

key_name = 'hadoop'
ec2_key = key_name +".pem"
pkey = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

flintrock_public_ip = str('3.239.93.255')
print(f"setting up mongoDB in ec2 instance with public IP address: {flintrock_public_ip}. This may take a while....")


cluster_name = input("Enter your custom cluster name (one which is not running currently): ")
num_cluster = int(input("Enter the number(Integer) of datanode in your cluster : "))
# Connect/ssh to mongodb instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    ssh_client.connect(hostname=flintrock_public_ip, username="ec2-user", pkey=pkey)

    # SCPClient
    print("Copying files from local to flintrock instance...")
    scp = SCPClient(ssh_client.get_transport())

    print("Copying hadoop_spark_setup.sh file from local to MongoDB instance")
    localpath = './flintrock_setup.sh'
    remotepath = '~/flintrock_setup.sh'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("hadoop_spark_setup.sh transferred!")

    print("Copying start_cluster.sh file from local to MongoDB instance")
    localpath = './start_cluster.py'
    remotepath = '~/start_cluster.py'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("start_cluster.sh transferred!")
    scp.close()

    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ./{ec2_key} ec2-user@{flintrock_public_ip}:/home/ec2-user')
    

    cmd0 = f'python3 start_cluster.py {cluster_name} {key_name} {num_cluster} {key} {secrete_key} {session_token}'

    print(cmd0)
    cmd01 = 'echo helloworld'
    stdin, stdout, stderr = ssh_client.exec_command(cmd0)
    print(stdout.read())
    stdin, stdout, stderr = ssh_client.exec_command(cmd01)
    print(stdout.read())
    print("flintrock_configured")
    #close the client connection once the job is done
    ssh_client.close()
    #break

except Exception as e:
    print (e)