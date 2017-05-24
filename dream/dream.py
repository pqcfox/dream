import boto3
import cv2

from dream.capture import get_corners, save_image

S3_KEY = 'dream'
corners = None


def run(args):
    if args['calibrate']:
        calibrate(args)
    elif args['push']:
        push(args)
    elif args['pull']:
        pull(args)
    elif args['status']:
        status(args)


def calibrate(args):
    corners = get_corners()


def push(args):
    if corners is None:
        print('Please calibrate before pushing.')
    image = grab_frame()
    path = save_image(image)
    s3 = boto3.client('s3')
    s3.upload_file(path, args['bucket-name'], S3_KEY)
    start_instance()


def pull(args):
    pass


def status(args):
    ec2 = boto3.resource('ec2')
    instance_id = args['instance-id']
    instance = ec2.Instance(instance_id)
    state = instance.state['Name']
    print('instance: {} ({})'.format(instance_id, state))
    if state == 'running':
        pass
    else:
        print('no process running')
