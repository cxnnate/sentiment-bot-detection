import os
import re
import sys
import argparse
import gensim
import sklearn
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Grab root directory for project (FIXME)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_document(text):
    processed_docs = []
    text = re.sub(r'\d+', '', str(text))
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            processed_docs.append(gensim.parsing.preprocessing.stem(token))
    
    return ' '.join(processed_docs)


def data_processing(dataset, nouns=False):
    """
    Executes the functions to prepare our data to fit the model
    :param dataset: The dataset of Tweets
    :param nouns: A boolean value indicating usage of only nouns
    :return: we'll see :)
    """

    # print(dataset)
    corpus = list()
    for tweet in dataset['clean_text']:
        corpus.append(clean_document(tweet))
    
    print(corpus)
    


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
    corpus = data_processing(dataset)

    output = args.o


if __name__ == '__main__':
    main(parse_cli())
