import shelve
from os.path import expanduser, join

import boto3
import cv2

import dream.capture

S3_KEY = 'dream'
CALIBRATION_FILE = '.dream_calib'
CALIBRATION_PATH = join(expanduser('~'), CALIBRATION_FILE)
NO_CONFIG_ERROR = 'Please calibrate before pushing.'


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
    corners = dream.capture.get_corners()
    with shelve.open(CALIBRATION_PATH) as db:
        db['corners'] = corners


def y_or_n(question):
    while True:
        text = '{} [Y/n] '.format(question)
        accept = input(text).lower()
        if accept == 'Y' or accept == '':
            return True
        elif accept.lower() == 'n':
            return False



def push(args):
    frame = dream.capture.grab_frame()
    try:
        with shelve.open(CALIBRATION_PATH) as db:
            corners = db['corners']
    except FileNotFoundException:
        print(NO_CONFIG_ERROR)

    output_size = (int(args['image-width']), 
                   int(args['image-height']))
    flat_frame = dream.capture.flatten(frame, corners, output_size)

    print('Showing image. Press any key to continue.')
    dream.capture.show_frame('Dream Push', flat_frame)
    if not y_or_n('Accept push?'):
        return

    # path = dream.capture.save_image(image)
    # s3 = boto3.client('s3')
    # s3.upload_file(path, args['bucket-name'], S3_KEY)
    # start_instance()


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
