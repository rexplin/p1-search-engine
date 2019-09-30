import pickle
from invertedIndex import Index


with open ('indexDump.txt', 'rb') as fp:
    index = pickle.load(fp)

userQuery = input('Search ');
print(index.lookup(index,userQuery))
