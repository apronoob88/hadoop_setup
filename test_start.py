import boto3
from botocore.exceptions import ClientError
from scp import SCPClient
import paramiko
import time
import os

ec2_key = 'hadoop.pem'
master_node_ip = '35.173.35.69'

pkey = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect/ssh to mongodb instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    ssh_client.connect(hostname=master_node_ip, username="ec2-user", pkey=pkey)

    # SCPClient
    scp = SCPClient(ssh_client.get_transport())

    print("Copying sample.py file from local to master node instance")
    localpath = './sample.py'
    remotepath = '~/sample.py'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("sample2.py transferred!")

    print("Copying sample2.py file from local to MongoDB instance")
    localpath = './sample2.py'
    remotepath = '~/sample2.py'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("sample2.py transferred!")

    print("Copying start_analytic_task.sh file from local to MongoDB instance")
    localpath = './start_analytic_task.sh'
    remotepath = '~/start_analytic_task.sh'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("start_analytic_task.sh transferred!")
    scp.close()

    print("installing dependencies to perform analytics task. This might take a while....")
    cmd = 'sh start_analytic_task.sh'
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read())
    ssh_client.close()

    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ec2-user@{master_node_ip}:/home/ec2-user/sample_output.csv ./analytic_task_output/')
    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ec2-user@{master_node_ip}:/home/ec2-user/sample_output2.csv ./analytic_task_output/')
except Exception as e:
    print (e)


#'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ec2-user@{flintrock_manager_public_ip}:/home/ec2-user/output.csv ./analytic_task_output'
