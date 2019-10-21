import nltk
import simplejson
from fullStopWordList import stopwords as stop_words
from collections import Counter
from search_index import pre_process_query
import math


def get_snippet(doc_id, query_terms):
    """
    Gets the snippet of from the document matching the passed in doc id
    it generates the snippet based on the provided query terms

    query terms are assumed to have already been processed and are passed in as a list

    The two sentences in the documents that have the highest cosine similarity with respect to query; with TF-IDF as
    the term weighting scheme.

    :param doc_id: id of the document the snippet will come from
    :param query_terms: the terms used to create the snippet
    :return: title of document and two sentence snippet
    """

    with open("test_data_lines.json", "r") as f:
        for entry in f:
            document = simplejson.loads(entry)
            # finds the document with the correct id
            if document["id"] == doc_id:
                print(document["title"])
                # tokenizes the content of the document by sentences
                sentences = nltk.sent_tokenize(f"{document['content']}")
                num_sentences = 0

                query_term_dict = {}
                for term in query_terms:
                    for sentence in sentences:
                        num_sentences += 1
                        processed_tokens = pre_process_query(sentence)
                        if term in processed_tokens:
                            if term in query_term_dict:
                                query_term_dict[term] += 1
                            else:
                                query_term_dict[term] = 1
                num_sentences /= len(query_term_dict)
                print(num_sentences)
                query_tfs = tf(query_terms)
                query_idfs = idf(num_sentences, query_term_dict)
                for sentence in sentences:
                    processed_tokens = pre_process_query(sentence)
                    sentence_tfs = tf(processed_tokens, qt=query_terms)
                    print(sentence_tfs)
                    sentence_idfs = idf(num_sentences, query_term_dict)


def tf(values, qt=None):
    tf_vals = list()
    occurrence_count = Counter(values)
    max_d = occurrence_count.most_common(1)[0][1]

    for item, count in occurrence_count.items():
        count /= max_d
        if qt:
            if item in qt:
                tf_vals.append((item, count))
            else:
                continue
        else:
            tf_vals.append((item, count))

    return tf_vals


def idf(n, nw):
    idf_vals = list()
    for term, value in nw.items():
        temp_idf = math.log2(n / value)
        idf_vals.append((term, temp_idf))

    return idf_vals


def numerator(sentence):
    val = 0

    return val


if __name__ == "__main__":
    query = ['adolf', 'swedish', 'model', 'architect']
    doc = 35
    # CURRENTLY ASSUMES THAT THE QUERY HAS ALREADY BEEN STEMMED AND TOKENIZED
    get_snippet(doc, query)
