from bplustree import BPlusTree, StrSerializer
from bplustree.memory import ReachedEndOfFile
from collections import OrderedDict
from fullStopWordList import stopwords as stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import simplejson
import nltk
from queue import Queue
import threading
import sys


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


# def extract_topn_from_vector(feature_names, sorted_items, topn=10):
#    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
#     sorted_items = sorted_items[:topn]

#     score_vals = []
#     feature_vals = []

    # word index and corresponding tf-idf score
#     for idx, score in sorted_items:
#         # keep track of feature name and its corresponding score
#         score_vals.append(round(score, 3))
#         feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
#     results = {}
#     for idx in range(len(feature_vals)):
#         results[feature_vals[idx]] = score_vals[idx]

#     return results


def index_worker(queue, index_queue, pp_docs_queue):
    while True:
        item = queue.get()

        if item is None or queue.empty():
            break

        do_work(item, index_queue, pp_docs_queue)
        queue.task_done()

    # Make sure last task completes or it locks
    queue.task_done()


def do_work(document, index_tree, pp_docs_queue):
    # process
    index = dict()
    unique_id = 1
    doc_id = document["id"]
    stemmer = nltk.stem.snowball.EnglishStemmer()
    tokens = nltk.word_tokenize(f"{document['title']} {document['content']}")
    ascii_tokens = [ascii_token for ascii_token in tokens if is_ascii(ascii_token)]
    filtered = [token.lower() for token in ascii_tokens if token not in stop_words]
    processed_tokens = [stemmer.stem(token) for token in filtered if token.isalpha()]

    # Process one more time for stop words after lemmatizing cause we might still have things like 'a' leftover
    final_tokens = [token for token in processed_tokens if token not in stop_words]
    pp_docs_queue.put({"id": doc_id, "text": " ".join(final_tokens)})

    for token in final_tokens:
        pos = unique_id
        try:
            existing = tree.get(token)
            if existing:
                existing = existing.decode()
                updated = "|".join([existing, f"{doc_id}:{pos}"])
                index_tree.insert(token, updated.encode(), replace=True)
            else:
                index_tree.insert(token, f"{doc_id}:{pos}".encode())
        except AssertionError:
            with open("error-log.txt", "a") as log:
                log.write(f"Assertion: {token} - {doc_id}:{pos}")
                log.write('\n')
            continue
        except ReachedEndOfFile:
            with open("error-log.txt", "a") as log:
                log.write(f"EOF: {token} - {doc_id}:{pos}")
                log.write('\n')
            continue
        except IndexError:
            with open("error-log.txt", "a") as log:
                log.write(f"Index: {token} - {doc_id}:{pos}")
                log.write('\n')
            continue

        unique_id += 1
    # for token in final_tokens:
    #     # add the document id followed by the line location into the dictionary/list
    #     pos = unique_id
    #     if token not in index:
    #         index.update({token: [f"{doc_id}:{pos}"]})
    #     else:
    #         index[token].append(f"{doc_id}:{pos}")
    #     unique_id += 1
    #
    # index_queue.put(index)


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
    work = Queue()
    # results = Queue()
    tree = BPlusTree("./index/index.db", serializer=StrSerializer(), order=50, key_size=20)
    pp_docs = Queue()
    num_workers = 8
    threads = []
    total_index = dict()
    count = 0

    try:
        # produce data
        with open("test_data_lines.json", "r") as f:
        # with open("wikipedia_data_lines.json", "r") as f:
            for entry in f:
                if count == 10000:
                    break
                work.put(simplejson.loads(entry))
                count += 1

        # start for workers
        for i in range(num_workers):
            t = threading.Thread(target=index_worker, args=(work, tree, pp_docs))
            t.daemon = True
            t.start()
            threads.append(t)

        print("Performing work.join()")
        work.join()

        # get the results
        # print("Retrieving results and building final index")
        # while not results.empty():
        #     partial = results.get()
        #     if partial is not None:
        #         for key, val in partial.items():
        #             if key in total_index:
        #                 total_index[key].extend(val)
        #             else:
        #                 total_index[key] = val
        #
        #     results.task_done()

        # Load the pre-processed docs into an array
    #     pp_docs_list = list()
    #     while not pp_docs.empty():
    #         entry = pp_docs.get()
    #         if entry is not None:
    #             pp_docs_list.append(entry)
    #        pp_docs.task_done()

        # Generate vector
    #     pp_docs_list = sorted(pp_docs_list, key=lambda k: k["id"])
    #     tfidf_docs = [doc["text"] for doc in pp_docs_list]
    #     tfidf_vectors = list()
    #     cv = CountVectorizer()
    #     word_count_vector = cv.fit_transform(tfidf_docs)
    #     tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    #     tfidf_transformer.fit(word_count_vector)

    #     for doc in tfidf_docs:
    #         tfidf_vectors.append(sort_coo(tfidf_transformer.transform(cv.transform([doc])).tocoo()))

    #     featured_names = cv.get_feature_names()
    #     keywords = extract_topn_from_vector(featured_names, tfidf_vectors[0], 10)
    #     print(keywords)

        # Clean up
        print("Terminating workers...")
        for i in range(num_workers):
            work.put(None)

        print("Terminating threads...")
        for t in threads:
            t.join()

        # print("Writing index file...")
        # ordered_index = OrderedDict(sorted(total_index.items()))
        # with open("ascii_index.json", "w") as file:
        #     file.write(simplejson.dumps(ordered_index))
        #     file.write("\n")
        #     sys.exit()

        print(f"# Keys: {len(tree.keys())}")


    except KeyboardInterrupt:
        print("Terminating workers...")
        for i in range(num_workers):
            work.put(None)

        print("Terminating threads...")
        for t in threads:
            t.join()
