import os

# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID_TO_CHANGE
os.environ['AWS_SECRET_ACCESS_KEY'] = 'AWS_SECRET_ACCESS_KEY_TO_CHANGE'
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


sudo sed -i "s/os.environ['AWS_ACCESS_KEY_ID'] = key/0.0.0.0.0/g" ~/start_cluster.py

sudo sed -i 's/127.0.0.1/0.0.0.0/g' 


"sudo sed -i 's/'AWS_SECRET_ACCESS_KEY_TO_CHANGE'/'ASIAURJ2CACXOGUSQAOW'/g' /home/ec2-user/start_cluster.py"