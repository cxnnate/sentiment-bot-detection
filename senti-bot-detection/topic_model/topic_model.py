import os
import sys
import argparse
import gensim
import sklearn
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def parse_cli():
    """
    Reads from command-line arguments
    :return: args
    """
    parser = argparse.ArgumentParser(description='Topic model settings')
    parser.add_argument('--i', type=str, help='Input file')
    parser.add_argument('--o', type=str, help='Output file')
    parser.add_argument('--n', type=int, help='Option to use only nouns')

    return parser.parse_args()


def main(args):
    """
    Run streamer
    """
    if args.i is None:
        print("- Need input file -")
        sys.exit(0)

    if args.o is None:
        print("- Need output file -")
        sys.exit(0)
    
    if args.n is None:
        nouns = False
    
    cols = ['created_at', 'tweet_id', 'text', 'clean_text', 'hashtags', 'user_id']
    dataset = pd.read_csv(ROOT + '/data/' + args.i, names=cols)
    print(dataset)
    output = args.o



if __name__ == '__main__':
    main(parse_cli())
