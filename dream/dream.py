import boto3

def dream(args):
    if args['calibrate']:
        calibrate(args)
    elif args['push']:
        push(args)
    elif args['pull']:
        pull(args)
    elif args['status']:
        status(args)


def calibrate(args):
    pass


def push(args):
    pass


def pull(args):
    pass


def status(args):
    ec2 = boto3.client('ec2')
    instance_id = args['instance-id']
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    state = instance['State']['Name']
    instance_type = instance['InstanceType']
    print('{} ({}) is {}'.format(instance_id, instance_type, state))
