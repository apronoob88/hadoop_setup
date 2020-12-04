import os
import sys

cluster_name = sys.argv[1]
key_name = sys.argv[2]     #ec2 key name
num_cluster = sys.argv[3]
key = sys.argv[4]          #aws_access_key
secrete_key = sys.argv[5]
session_token = sys.argv[6]

ec2_key = key_name +'.pem'

os.system('sudo apt update')
os.system('sudo apt install python3-pip -y')
os.system('pip3 install flintrock')



os.system(f'chmod 400 {ec2_key}')


# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = key
os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
os.environ['AWS_SESSION_TOKEN'] = session_token


flintrock_cmd = f'flintrock launch {cluster_name} \
    --num-slaves {num_cluster} \
    --hdfs-version 2.10.1 \
    --spark-version 2.4.7 \
    --ec2-key-name {key_name} \
    --ec2-identity-file /home/ec2-user/{ec2_key} \
    --ec2-ami ami-04d29b6f966df1537 \
    --ec2-user ec2-user \
    --ec2-instance-type t2.medium \
    --ec2-region us-east-1 \
    --install-hdfs \
    --install-spark'

os.system(flintrock_cmd)
