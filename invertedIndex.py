import json
import pickle
import re
from collections import defaultdict

import nltk
import pprint
from nltk.stem.snowball import EnglishStemmer


class Index:

    def __init__(self, tokenizer, stemmer=None, stopwords=None):

        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = defaultdict(list)
        self.documents = {}
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)

    def lookup(self, word):

        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return [self.documents.get(id, None) for id in self.index.get(word)]

    def add(self, document):

        self.__unique_id = 1
        clean_text = re.sub(r'[^\w\s]', '', document['content'])
        for token in [t.lower() for t in nltk.word_tokenize(clean_text)]:
            if token in self.stopwords:
                continue

            if self.stemmer:
                token = self.stemmer.stem(token)

            if self.__unique_id not in self.index[token]:
                self.index[token].append(document['id'])
                self.index[token].append(self.__unique_id)
            else:
                self.index[token].append(document['id'])
                self.index[token].append(self.__unique_id)
            self.documents[self.__unique_id] = document
            self.__unique_id += 1


index = Index(nltk.word_tokenize,
              EnglishStemmer(),
              nltk.corpus.stopwords.words('english'))
# nltk.corpus.stopwords.words('english'))

i = 0
myfile = open("wikipedia_text_files.json", "r")
data = json.load(myfile)
# index.add(data[0])
# index.add(data[1])
for documents in data:
    index.add(documents)
    print(i)
    i += 1
myfile.close()

with open('indexDump.txt', 'wb') as fp:
    pickle.dump(index, fp)
