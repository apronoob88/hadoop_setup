import os

os.system('sudo apt update')
os.system('sudo apt install python3-pip -y')
os.system('pip3 install flintrock')
os.system('chmod 400 hadoop.pem')
# os.system('sudo yum install python37 -y')
# os.system('sudo yum -y install python3-pip')
# os.system('sudo pip3 install flintrock')


key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")
# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = key
os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
os.environ['AWS_SESSION_TOKEN'] = session_token


num = 1

flintrock_cmd = f'flintrock launch hadoop-cluster3 \
    --num-slaves {num} \
    --hdfs-version 2.10.1 \
    --spark-version 2.4.7 \
    --ec2-key-name hadoop \
    --ec2-identity-file /home/ec2-user/hadoop.pem \
    --ec2-ami ami-04d29b6f966df1537 \
    --ec2-user ec2-user \
    --ec2-instance-type t2.medium \
    --ec2-region us-east-1 \
    --install-hdfs \
    --install-spark'

os.system(flintrock_cmd)





# import os

# key = input("Enter your aws_access_key_id: ")
# secrete_key = input("Enter your aws_secret_access_key: ")
# session_token = input("Enter your aws_session_token: ")
# # Set environment variables
# os.environ['AWS_ACCESS_KEY_ID'] = key
# os.environ['AWS_SECRET_ACCESS_KEY'] = secrete_key
# os.environ['AWS_SESSION_TOKEN'] = session_token

# os.system('echo $AWS_ACCESS_KEY_ID')



# os.system('flintrock launch hadoop-cluster3 \
#     --num-slaves 3 \
#     --hdfs-version 2.10.1 \
#     --spark-version 2.4.7 \
#     --ec2-key-name hadoop \
#     --ec2-identity-file /home/ec2-user/hadoop.pem \
#     --ec2-ami ami-04d29b6f966df1537 \
#     --ec2-user ec2-user \
#     --ec2-instance-type t2.medium \
#     --ec2-region us-east-1 \
#     --install-hdfs \
#     --install-spark')