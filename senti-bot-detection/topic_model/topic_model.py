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


def create_bow_corpus(docs):
    """
    Using Sklearn's CountVectorizer, we create a Bag-of-words representation of the corpus
    :param corpus: Collection of documents
    :return: A vectorized corpus and vocabulary
    """
    vectorizer = CountVectorizer()
    corpus = vectorizer.fit_transform(docs)
    vocab = vectorizer.get_feature_names()
    vocab = dict([(i, s) for i, s in enumerate(vocab)])
    corpus = gensim.matutils.Sparse2Corpus(corpus.T)

    return corpus, vocab


def clean_document(text):
    """
    Executes the final round of data cleaning
    :param text: A single tweet
    :return: A processed tweet ready for vectorization 
    """
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
    :param nouns:  A boolean value indicating usage of only nouns
    :return: we'll see :)
    """

    # TODO: Parallelize?
    docs = list()
    for tweet in dataset['clean_text']:
        docs.append(clean_document(tweet))

    corpus, vocab = create_bow_corpus(docs)
    
    print(corpus)
    print(vocab)
    


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
