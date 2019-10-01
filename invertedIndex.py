from collections import OrderedDict
from fullStopWordList import stopwords as stop_words
from multiprocessing import Pool
from nltk.stem.snowball import EnglishStemmer
import json
# import pickle
import nltk
import simplejson
import sys


class Index:
    """
    Class to process a collection into an inverted index

    """

    def __init__(self, tokenizer, stemmer=None, stopwords=None):

        self.tokenizer = tokenizer
        self.stemmer = stemmer if stemmer else EnglishStemmer()
        self.index = dict()
        self.documents = dict()
        self.stopwords = set(stopwords) if stopwords else set(stop_words)
        self.__unique_id = 1

    def lookup(self, word):
        """
        This returns the document id so far, if we want to use it later, need to
        add the frequency to the return

        :param word:
        :return: Returns document id so far
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return [self.documents.get(doc_id, None) for doc_id in self.index.get(word)]

    def add(self, document):
        """
        Adds a document to the index

        :param document: Document to be processed and added to the index
        :return: None
        """
        self.__unique_id = 1
        tokens = self.tokenizer(document["content"])
        filtered = [token for token in tokens if token not in self.stopwords]
        processed_tokens = [self.stemmer.stem(token.lower()) for token in filtered if token.isalpha()]

        # Process one more time for stop words after lemmatizing cause we might still have things like 'a' leftover
        final_tokens = [token for token in processed_tokens if token not in self.stopwords]

        for token in final_tokens:
            # add the document id followed by the line location into the dictionary/list
            doc_id = document["id"]
            pos = self.__unique_id
            if token not in self.index:
                self.index.update({token: [f"{doc_id}:{pos}"]})
            else:
                if f"{doc_id}:{pos}" not in self.index[token]:
                    self.index[token].append(f"{doc_id}:{pos}")

#            else:
#                self.index[token].append(document['id'])           # adds the indevidual document to each word,
#                self.index[token].append(self.__unique_id)         # too much time and space for large collections
#           self.documents[self.__unique_id] = document
            self.__unique_id += 1

        return self.index

    def order_index(self):
        """
        Orders the existing index lexicographically

        :return: None
        """
        self.index = OrderedDict(sorted(self.index.items()))

    def dump(self, filename):
        """
        Writes the current index to a file

        :param filename: Name of file to be written to
        :return: None
        """

        # Order the index
        self.order_index()

        # Dump it to a file
        with open(filename, "w") as dump_file:
            dump_file.write(simplejson.dumps(self.index, indent=4))

    def merge(self, partial):
        """
        Merges a partial index into the full index

        :param partial: Partial index
        :return: None
        """
        self.index.update(partial)


if __name__ == "__main__":
    pool = Pool()
    index = Index(nltk.word_tokenize)
    # counting var for testing purposes
    i = 0
    # open json wiki file in read only
    with open("test_data.json", "r") as myfile:
    # with open("wikipedia_text_files.json", "r") as myfile:
        # load wiki file in a list format
        data = json.load(myfile)

    result = pool.imap(index.add, data)

    for partial in result:
        index.merge(partial)
        sys.stdout.write(f"Progress: {i}    \r")
        sys.stdout.flush()
        i += 1

    index.dump("multi_process.json")
