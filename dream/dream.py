import os
import path
import shelve
import tempfile

import boto3
import cv2

import dream.capture

S3_PUSH_KEY = 'dream_push.jpg'
S3_PULL_KEY = 'dream_pull.gzip'
CALIBRATION_FILE = '.dream_calib'
CALIBRATION_PATH = os.path.join(os.path.expanduser('~'), CALIBRATION_FILE)
NO_CONFIG_ERROR = 'Please calibrate before pushing.'
SHOW_IMAGE_TEXT = 'Showing image. Press any key to continue.'
ACCEPT_PUSH_QUESTION = 'Accept push?'

s3 = boto3.resource('s3')
bucket = s3.Bucket(args['bucket-name'])


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
    print(SHOW_IMAGE_TEXT)
    dream.capture.show_frame('Dream Push', flat_frame)
    if not y_or_n(ACCEPT_PUSH_QUESTION):
        return

    path = dream.capture.save_frame(flat_frame)
    bucket.upload_file(path, S3_PUSH_KEY)
    instance.start()


def pull(args):
    bucket.download_file(S3_PULL_KEY, os.getcwd())
    

def status(args):
    ec2 = boto3.resource('ec2')
    instance_id = args['instance-id']
    instance = ec2.Instance(instance_id)
    state = instance.state['Name']
    print('instance: {} ({})'.format(instance_id, state))
    if state == 'running':
        temp = NamedTemporaryFile()
        bucket.download_file(S3_PULL_KEY, temp.name)
        with open(temp) as f:
            print(temp.read())
