#### this script to be executed in the flintrock manager instance


import os
import sys

cluster_name = sys.argv[1]
key_name = sys.argv[2]     #ec2 key name
num_node = sys.argv[3]
key = sys.argv[4]          #aws_access_key
secrete_key = sys.argv[5]
session_token = sys.argv[6]

ec2_key = key_name +'.pem'

os.system(f'chmod 400 {ec2_key}')


# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = key
os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
os.environ['AWS_SESSION_TOKEN'] = session_token



cmd = f'echo y | flintrock remove-slaves {cluster_name} --num-slaves {num_node} --ec2-identity-file /home/ec2-user/{ec2_key} --ec2-user ec2-user'
os.system(cmd)
