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
    instance_id = args['<id>']
