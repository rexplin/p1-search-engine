import pickle
import pprint

from invertedIndex import Index


with open ('indexDump.txt', 'rb') as fp:            #retreive the index object
    index = pickle.load(fp)
pprint.pprint(index.index)                          #print the index in alphabetical format
#userQuery = input('Search ');
#print(index.lookup(index,userQuery))
