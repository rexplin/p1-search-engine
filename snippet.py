import nltk
from collections import Counter
from search_index import pre_process_query
import math
import json


def get_snippet(doc_id, query_terms, relevance_score):
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
    query_terms = pre_process_query(query_terms)
    filename = f"../wiki-files-separated/file{int(doc_id/200000)+1}/wiki-doc-{doc_id}.json"
    with open(filename, "r") as original_doc:
        document = json.load(original_doc)
    # for entry in f:
        # document = simplejson.loads(entry)
    # finds the document with the correct id
    if document["id"] == doc_id:
        snippet = f"{doc_id}:\t{document['title']} ({relevance_score})\n"
        # tokenizes the content of the document by sentences
        sentences = nltk.sent_tokenize(f"{document['content']}")
        num_sentences = 0

        # find how many sentences each query term is in. This value is used to calculate the
        # idf. Also find the number of sentences in the document
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
        num_query_terms = len(query_term_dict)
        num_sentences /= num_query_terms if num_query_terms > 0 else 1
        # calculates for the query
        query_tfs = tf(query_terms)
        query_idfs = idf(num_sentences, query_term_dict)
        query_tf_idfs = tf_idf(query_tfs, query_idfs)

        similarities = list()
        # calculates for each sentence
        for sentence in sentences:
            processed_tokens = pre_process_query(sentence)
            sentence_tfs = tf(processed_tokens, qt=query_terms)
            sentence_idfs = idf(num_sentences, query_term_dict)
            if len(sentence_tfs) == 0:
                continue
            else:
                sentence_tf_idfs = tf_idf(sentence_tfs, sentence_idfs)
                numer = numerator(sentence_tf_idfs, query_tf_idfs)
                denom = denominator(sentence_tf_idfs, query_tf_idfs)
                cosine = cosine_similarity(numer, denom)
                similarities.append((sentence, cosine))
                # sorts the list by the cosine similarity value in descending order
        similarities.sort(key=lambda tup: tup[1], reverse=True)
        top_two = similarities[:2]
        if len(top_two) == 2:
            snippet = f"{snippet}\n\t{top_two[0][0]}\n\t{top_two[1][0]}\n\n"
        elif len(top_two) == 1:
            snippet = f"{snippet}\n\t{top_two[0][0]}\n\n"

        return snippet


def tf(values, qt=None):
    """
    function to find the term frequency for each term in the provided list, this is found by dividing
    the frequency of a word in the list by the most frequenc word in that list
    TF(w,d) = freq(w,d)/max_d
    :param values: the words to find the frequency of
    :param qt: optional: list of query terms to be used
    :return: list of (term: frequency) pairs
    """
    tf_vals = list()
    occurrence_count = Counter(values)
    if not occurrence_count - Counter() == Counter():
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
    """
    function to calculate the inverse document frequency score this is found by taking the log of the number of sentences
    divided by the number of sentences the word appears in
    IDF(w) = log2(N/n_w)
    :param n: the number of sentences in the document
    :param nw: the number of sentences in which the query term appears at least once,
    it is a list of (query term: num sentences) pairs
    :return:list of (term: idf) pairs
    """
    idf_vals = list()
    for term, value in nw.items():
        temp_idf = math.log2(n / value)
        idf_vals.append((term, temp_idf))

    return idf_vals


def tf_idf(tfs, idfs):
    """
    this function finds the tf_idf score for each term passed in the lists
    the tf idf is only calculated when the term appears in both tfs and idfs, because
    if it is missing in one the calculation would lead it to be zero, which will effectively be
    thrown out in later summation
    :param tfs: list of (term:term frequency) pairs
    :param idfs: list of (term: inverse document frequency) pairs
    :return: list of (term: tf_idf) pairs
    """
    tf_idf_vals = list()
    for tf_val in tfs:
        for idf_val in idfs:
            if tf_val[0] == idf_val[0]:
                tf_idf_val = tf_val[1] * idf_val[1]
                tf_idf_vals.append((tf_val[0], tf_idf_val))
    return tf_idf_vals


def numerator(sentence_tf_idfs, query_tf_idfs):
    """
    This function determines the numerator of the cosine similarity equation
    cosine(d,q) = (Σ d * q)/( Σ d^2 *  Σ q^2)
    :param sentence_tf_idfs: the tf-idf of each word in the sentence
    :param query_tf_idfs: the tf-idf of each word the query
    :return: value for the numerator of equation
    """
    result = list()
    for query_tf_idf in query_tf_idfs:
        for sentence_tf_idf in sentence_tf_idfs:
            if sentence_tf_idf[0] == query_tf_idf[0]:
                val = query_tf_idf[1] * sentence_tf_idf[1]
                result.append(val)

    num = sum(result)

    return num


def denominator(sentence_tf_idfs, query_tf_idfs):
    """
    determines the denominator of the cosine similarity equation
    cosine(d,q) = (Σ d * q)/( Σ d^2 *  Σ q^2)
    :param sentence_tf_idfs: the tf-idf of each word in the sentence
    :param query_tf_idfs: the tf-idf of each word the query
    :return: value for the denominator of equation
    """
    query_results = list()
    sentence_results = list()
    for query_tf_idf in query_tf_idfs:
        query_results.append(math.pow(query_tf_idf[1], 2))
    for sentence_tf_idf in sentence_tf_idfs:
        sentence_results.append(math.pow(sentence_tf_idf[1], 2))
    query_sum = sum(query_results)
    sentence_sum = sum(sentence_results)
    result = query_sum * sentence_sum
    final_result = math.sqrt(result)
    return final_result


def cosine_similarity(numer, denom):
    result = numer / denom if denom > 0 else 1
    return result


if __name__ == "__main__":
    query = ['adolf', 'swedish', 'model', 'architect']
    doc = 35
    query2 = ['anthoni', 'unit', 'state', 'post', 'offic']
    doc1 = 333467
    doc2 = 204409
    doc3 = 863570
    doc4 = 855044
    doc5 = 376121
    doc6 = 71736
    doc7 = 249810
    doc8 = 282272
    doc9 = 1069218
    doc10 = 275269
    # print(get_snippet(doc, query))
    print(get_snippet(doc1, query2))
    print(get_snippet(doc2, query2))
    print(get_snippet(doc3, query2))
    print(get_snippet(doc4, query2))
    print(get_snippet(doc5, query2))
    print(get_snippet(doc6, query2))
    print(get_snippet(doc7, query2))
    print(get_snippet(doc8, query2))
    print(get_snippet(doc9, query2))
    print(get_snippet(doc10, query2))
