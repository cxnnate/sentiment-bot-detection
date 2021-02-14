import os
import sys


def parse_cli():
    """
    Reads from command-line arguments
    :return: args
    """
    parser = argparse.ArgumentParser(description='Topic model settings')
    parser.add_argument('--creds', type=str, help='Twitter API Credentials file')
    parser.add_argument('--keys', type=str, help='List of keywords to track on Twitter')
    parser.add_argument('--time', type=int, help='Time to stream Twitter')

    return parser.parse_args()


def main(args):
    """
    Run streamer
    """
    if args.creds is not None:
        with open(ROOT + '/topic_model/' + args.creds, 'r') as f:
            creds = json.load(f)
    else:
        print('Invalid')
        sys.exit(0)

    if args.keys is not None:
        with open(ROOT + '/topic_model/' + args.keys, 'r') as f:
            keywords = f.read().splitlines()
    else:
        print('Invalid')
        sys.exit(0)

    time_limit = args.time