import boto3
from botocore.exceptions import ClientError
from scp import SCPClient
import paramiko
import time
import os

key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")

ec2_client = boto3.client('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secrete_key,
    aws_session_token= session_token,
    region_name='us-east-1')

response = ec2_client.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

def del_flintrock_sg():
    flintrock_sg_id = ''
    for security_group_info in available_security_groups_info:
        #print(security_group_info['GroupName'])
        if security_group_info['GroupName'] == 'flintrock':
            flintrock_sg_id = security_group_info['GroupId']
    try:
        response = ec2_client.delete_security_group(GroupId=flintrock_sg_id)
        print('Security Group Deleted')
    except ClientError as e:
        print(e)

def get_flintrock_sg_id():
    for security_group_info in available_security_groups_info:
        if security_group_info['GroupName'] == 'flintrock':
            flintrock_sg_id = security_group_info['GroupId']
            return flintrock_sg_id

existing_security_group_names = []
available_security_groups_info=ec2_client.describe_security_groups().get('SecurityGroups')
for security_group_info in available_security_groups_info:
    existing_security_group_names.append(security_group_info['GroupName'])


# if there is already security group named 'flintrock' , edit its inbound rules
if 'flintrock' in existing_security_group_names:
    print('Security Group "flintrock" already exists, configuring its inbound rule')
    flintrock_sg_id = get_flintrock_sg_id()
    try:
        data = ec2_client.authorize_security_group_ingress(
            GroupId=flintrock_sg_id,
            IpPermissions=[
                {'IpProtocol': '-1',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])

        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print('traffic already configured for the inbound rule')
        pass

# if there is no security goup named 'flintrock', create one
else:
    print('Creating security group for flinkrock')
    try:
        response = ec2_client.create_security_group(GroupName='flintrock',
                                            Description='Flintrock base group',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': '-1',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)


existing_key_pairs = []
existing_keys_info = ec2_client.describe_key_pairs().get('KeyPairs')
for key_info in existing_keys_info:
    existing_key_pairs.append(key_info['KeyName'])


print("Enter a ec2 key-pair name (without '.pem' behind).")
print("The key name can either be: \n\
1) existing key-pair name, but make sure they are in the current directory right now \n\
2) or, we will generate a key for you with the provided name")
key_name = input("Enter your ec2 key-pair name: ")

if not key_name in existing_key_pairs:
    print(f"entered a new key name, genrating {key_name}.pem")
    keypair = ec2_client.create_key_pair(KeyName=key_name)
    key_content = str(keypair['KeyMaterial'])
    ec2_key = key_name +".pem" 
    key_gen = open(ec2_key,'w')
    key_gen.write(key_content)
    key_gen.close()

else:
    print(f'using existing key {key_name}.pem')
os.system("chmod 400 {}.pem".format(key_name))



session = boto3.session.Session(
        aws_access_key_id=key,
        aws_secret_access_key=secrete_key,
        aws_session_token= session_token,
        region_name='us-east-1')

ec2 = session.resource('ec2')

# create new EC2 instances
instances = ec2.create_instances(
        ImageId='ami-04d29b6f966df1537',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.medium',
        SecurityGroups=['flintrock'],
        KeyName=key_name
)

print("Please wait the flintrock manager instance to be created.....")
flintrock_manager = instances[0]

flintrock_manager.wait_until_running()
flintrock_manager.load()

# sleep for 30 seconds for the instance to be fully loaded up
for i in range(30):
	time.sleep(1)

flintrock_manager_public_ip = flintrock_manager.public_ip_address
print('public_ip: ', flintrock_manager)



ec2_key = key_name +".pem"

pkey = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

cluster_name = input("Enter your custom cluster name (one which is not running currently): ")
num_cluster = int(input("Enter the number(Integer) of datanode in your cluster : "))
# Connect/ssh to mongodb instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    ssh_client.connect(hostname=flintrock_manager_public_ip, username="ec2-user", pkey=pkey)

    # SCPClient
    print("Copying files from local to flintrock manager instance...")
    scp = SCPClient(ssh_client.get_transport())

    print("Copying flintrock_setup.sh file from local to MongoDB instance")
    localpath = './flintrock_setup.sh'
    remotepath = '~/flintrock_setup.sh'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("flintrock_setup.sh transferred!")

    print("Copying start_cluster.sh file from local to MongoDB instance")
    localpath = './start_cluster.py'
    remotepath = '~/start_cluster.py'
    scp.put(localpath, remotepath)
    scp.get(remotepath)
    print("start_cluster.sh transferred!")
    scp.close()

    #copy ec2-key over to flintrock manager instance
    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ./{ec2_key} ec2-user@{flintrock_manager_public_ip}:/home/ec2-user')
    
    
    cmd1 = 'sh flintrock_setup.sh'
    cmd2 = f'python3 start_cluster.py {cluster_name} {key_name} {num_cluster} {key} {secrete_key} {session_token}'
    print(cmd2)
    print(f"initializing hadoop and spark cluster. This may take a while....")

    stdin, stdout, stderr = ssh_client.exec_command(cmd1)
    print(stdout.read())

    stdin, stdout, stderr = ssh_client.exec_command(cmd2)
    print(stdout.read())
    print("hadoop and spark cluster successfully configured!!")
    #close the client connection once the job is done
    ssh_client.close()
    #break

except Exception as e:
    print (e)


# get masternode ip address to perform analytic task there
master_filter = [{
    'Name':'tag:Name', 
    'Values': [f'{cluster_name}-master']}]

response = ec2_client.describe_instances(Filters=master_filter)

master_node_ip = ''
# place safe there, check if indeed only 1 instance of master node returned, the length are almost always 1
if len(response['Reservations']) != 1:
    print('either 0 or multiple master node exists')
    exit()
    if len(response['Reservations'][0]['Instances']) != 1:
        print('either 0 or multiple master node exists')
        exit()
else:
    master_node_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print("master node public IP adress is", master_node_ip)
print (f"to access the master node, type :\nssh ec2-user@{master_node_ip} -i hadoop.pem")



# perform analytic task

pkey = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Here 'ec2-user' is user name and 'master_node_ip' is public IP of the master node created
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

    print("performing analytics task. This might take a while....")
    cmd = 'sh start_analytic_task.sh'
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read())
    ssh_client.close()

    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ec2-user@{master_node_ip}:/home/ec2-user/sample_output.csv ./analytic_task_output/')
    os.system(f'scp -o "StrictHostKeyChecking=no" -i ./{ec2_key} ec2-user@{master_node_ip}:/home/ec2-user/sample_output2.csv ./analytic_task_output/')
except Exception as e:
    print (e)