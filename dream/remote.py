import socket

s = socket.socket()
host = socket.gethostname()
port = 12345


def send_image(image):
    s3 = boto3.resource('s3')

