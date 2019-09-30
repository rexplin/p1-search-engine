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

    def lookup(self, word):                 # this returns the document id so far, if we want to use it later, need to
                                            # add the frequancy to the return
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return [self.documents.get(id, None) for id in self.index.get(word)]

    def add(self, document):                # adding documents to the index

        self.__unique_id = 1
        clean_text = re.sub(r'[^\w\s]', '', document['content'])        #remove all grammer i.e. periods
        for token in [t.lower() for t in nltk.word_tokenize(clean_text)]:       #double through the list tokenized and lowercase
            if token in self.stopwords:     # check if tokened work is in the stopword list
                continue

            if self.stemmer:        # stem the word
                token = self.stemmer.stem(token)

            if self.__unique_id not in self.index[token]:
                self.index[token].append(document['id'])        # add the document id
                self.index[token].append(self.__unique_id)      # followed by the line location into the dictionary/list
#            else:
#                self.index[token].append(document['id'])           # adds the indevidual document to each word,
#                self.index[token].append(self.__unique_id)         # too much time and space for large collections
 #           self.documents[self.__unique_id] = document
            self.__unique_id += 1
#file = open("fullStopWordList.txt","r")                            # these lines should work but some error
#fullList = file.read()                                             # is preventing me from extending the nltk list
#stopwordlist = nltk.corpus.stopwords.words('english')              # or using the file format.
#stopwordlist.extend(fullList)
index = Index(nltk.word_tokenize,
              EnglishStemmer(),
              ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'you\'re', 'you\'ve', 'you\'ll',
               'you\'d', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'she\'s',
               'her',
               'hers', 'herself', 'it', 'it\'s', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
               'what', 'which', 'who', 'whom', 'this', 'that', 'that\'ll', 'these', 'those', 'am', 'is', 'are', 'was',
               'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
               'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
               'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
               'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
               'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
               'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
               't', 'can', 'will', 'just', 'don', 'don\'t', 'should', 'should\'ve', 'now', 'd', 'll', 'm', 'o', 're',
               've', 'y', 'ain', 'aren', 'aren\'t', 'couldn', 'couldn\'t', 'didn', 'didn\'t', 'doesn', 'doesn\'t',
               'hadn',
               'hadn\'t', 'hasn', 'hasn\'t', 'haven', 'haven\'t', 'isn', 'isn\'t', 'ma', 'mightn', 'mightn\'t', 'mustn',
               'mustn\'t', 'needn', 'needn\'t', 'shan', 'shan\'t', 'shouldn', 'shouldn\'t', 'wasn', 'wasn\'t', 'weren',
               'weren\'t', 'won', 'won\'t', 'wouldn', 'wouldn\'t', 'can\'t', 'cannot', 'could', 'he\'d', 'he\'ll',
               'he\'s',
               'here\'s', 'how\'s', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'let\'s', 'ought', 'she\'d', 'she\'ll', 'that\'s',
               'there\'s', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve',
               'what\'s',
               'when\'s', 'where\'s', 'who\'s', 'why\'s', 'would', 'a\'s', 'able', 'according', 'accordingly', 'across',
               'actually', 'afterwards', 'ain\'t', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also',
               'although', 'always', 'among', 'amongst', 'another', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway',
               'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'around', 'aside', 'ask',
               'asking', 'associated', 'available', 'away', 'awfully', 'became', 'become', 'becomes', 'becoming',
               'beforehand', 'behind', 'believe', 'beside', 'besides', 'best', 'better', 'beyond', 'brief', 'c\'mon',
               'c\'s', 'came', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com',
               'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing',
               'contains', 'corresponding', 'course', 'currently', 'definitely', 'described', 'despite', 'different',
               'done', 'downwards', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely',
               'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere',
               'ex', 'exactly', 'example', 'except', 'far', 'fifth', 'first', 'five', 'followed', 'following',
               'follows', 'former', 'formerly', 'forth', 'four', 'furthermore', 'get', 'gets', 'getting', 'given',
               'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'happens', 'hardly', 'hello',
               'help', 'hence', 'hereafter', 'hereby', 'herein', 'hereupon', 'hi', 'hither', 'hopefully', 'howbeit',
               'however', 'ie', 'ignored', 'immediate', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated',
               'indicates', 'inner', 'insofar', 'instead', 'inward', 'it\'d', 'it\'ll', 'keep', 'keeps', 'kept', 'know',
               'known', 'knows', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let',
               'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'mainly', 'many', 'may', 'maybe',
               'mean', 'meanwhile', 'merely', 'might', 'moreover', 'mostly', 'much', 'must', 'name', 'namely', 'nd',
               'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next',
               'nine', 'nobody', 'non', 'none', 'noone', 'normally', 'nothing', 'novel', 'nowhere', 'obviously',
               'often', 'oh', 'ok', 'okay', 'old', 'one', 'ones', 'onto', 'others', 'otherwise', 'outside', 'overall',
               'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably',
               'probably', 'provides', 'que', 'quite', 'qv', 'rather', 'rd', 'really', 'reasonably', 'regarding',
               'regardless', 'regards', 'relatively', 'respectively', 'right', 'said', 'saw', 'say', 'saying', 'says',
               'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves',
               'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'since', 'six', 'somebody',
               'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry',
               'specified', 'specify', 'specifying', 'still', 'sub', 'sup', 'sure', 't\'s', 'take', 'taken', 'tell',
               'tends', 'th', 'thank', 'thanks', 'thanx', 'thats', 'thence', 'thereafter', 'thereby', 'therefore',
               'therein', 'theres', 'thereupon', 'think', 'third', 'thorough', 'thoroughly', 'though', 'three',
               'throughout', 'thru', 'thus', 'together', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try',
               'trying', 'twice', 'two', 'un', 'unfortunately', 'unless', 'unlikely', 'unto', 'upon', 'us', 'use',
               'used', 'useful', 'uses', 'using', 'usually', 'value', 'various', 'via', 'viz', 'vs', 'want', 'wants',
               'way', 'welcome', 'well', 'went', 'whatever', 'whence', 'whenever', 'whereafter', 'whereas', 'whereby',
               'wherein', 'whereupon', 'wherever', 'whether', 'whither', 'whoever', 'whole', 'whose', 'willing', 'wish',
               'within', 'without', 'wonder', 'yes', 'yet', 'zero', 'b', 'c', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'n',
               'p', 'q', 'r', 'u', 'uucp', 'v', 'w', 'x', 'z', ' ', '\'', '!', '?', '`', '-', ', ', '.', ': ', ';',
               '\"', '<', '>', '{', '}', '[', ']', '+', '(', ')', '&', '%', '$', '@', '^', '#', '*', 'I'])                      #best to minimize list for work space


i = 0                                                   # counting var for testing purposes
myfile = open("wikipedia_text_files.json", "r")         # open json wiki file in read only
data = json.load(myfile)                                # load wiki file in a list format
while i < 100:                                          # testing while loop to add 100 documents
    index.add(data[i])
    i += 1

#for documents in data:                                 # for loop to add whole document to index
#    index.add(documents)
#    print(i)                                           # number of documents added counter for testing only
#    i += 1
myfile.close()

with open('indexDump.txt', 'wb') as fp:                 # write the index as an object to an encoded file
    pickle.dump(index, fp)
