import pickle
from fullStopWordList import stopwords as stop_words
import simplejson
import nltk
import sys
import hashedindex


def write_index(index, document):
    stemmer = nltk.stem.snowball.EnglishStemmer()
    tokens = nltk.word_tokenize(f"{document['title']} {document['content']}")
    ascii_tokens = [ascii_token for ascii_token in tokens if is_ascii(ascii_token)]
    filtered = [token.lower() for token in ascii_tokens if token not in stop_words]
    processed_tokens = [stemmer.stem(token) for token in filtered if token.isalpha()]
    final_tokens = [token for token in processed_tokens if token not in stop_words]
    for token in final_tokens:
        index.add_term_occurrence(token, document["id"])


def is_ascii(text):
    if isinstance(text, str):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True


if __name__ == "__main__":
    index = hashedindex.HashedIndex()
    count = 0
    with open("wikipedia_data_lines.json", "r") as f:
        for entry in f:
            sys.stdout.write(f"{count}    \r")
            sys.stdout.flush()
            if count == 200000:
                pickle.dump(index, open("hashIndexPickle1", "wb"))
                index.clear()
            if count == 400000:
                pickle.dump(index, open("hashIndexPickle2", "wb"))
                index.clear()
            if count == 600000:
                pickle.dump(index, open("hashIndexPickle3", "wb"))
                index.clear()
            if count == 800000:
                pickle.dump(index, open("hashIndexPickle4", "wb"))
                index.clear()
            if count == 1000000:
                pickle.dump(index, open("hashIndexPickle5", "wb"))
                index.clear()
            if count == 1200000:
                pickle.dump(index, open("hashIndexPickle6", "wb"))
                index.clear()
            if count == 1400000:
                pickle.dump(index, open("hashIndexPickle7", "wb"))
                index.clear()
            write_index(index, simplejson.loads(entry))
            count += 1
        pickle.dump(index, open("hashIndexPickle8", "wb"))
        index.clear()
