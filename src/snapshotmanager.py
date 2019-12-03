import boto3

session = boto3.Session(profile_name='snapshotmanager')
ec2 = session.resource('ec2')

if __name__ == '__main__':
    for i in ec2.instances.all():
        print(i)
