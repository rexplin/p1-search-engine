import pickle
import sys

import pandas as pd
import json
if __name__ == "__main__":
    for num in range(1, 9):
        with open(f'hashed-index/hashIndexPickle{num}', 'rb') as hashedIndexFile:
            print("loading first pickled index")
            hashedIndex = pickle.load(hashedIndexFile)
            print("finished, starting tfidf generation")
        # x = (hashedIndex.generate_feature_matrix(mode='tfidf'))
        maxTermFreq = dict()  # array to hold the max term freq
        tfidf = dict()
        # print(hashedIndex)
        print("starting max term freq per doc")
        for terms in hashedIndex.terms():  # loop through all terms in the collection
                # cmp the term freq with the max and replace with larger one
            for DocWithTerm in hashedIndex.get_documents(terms):    # loop through all documents that have term in them
                if maxTermFreq.get(DocWithTerm):
                    maxed = hashedIndex.get_term_frequency(terms, DocWithTerm) \
                        if hashedIndex.get_term_frequency(terms, DocWithTerm) > maxTermFreq.get(DocWithTerm) \
                        else maxTermFreq.get(DocWithTerm)
                    maxTermFreq.update({DocWithTerm: maxed})
                else:
                    maxTermFreq.update({DocWithTerm: hashedIndex.get_term_frequency(terms, DocWithTerm)})
        print("finished, writing max term freq per doc to pickle")
        pickle.dump(maxTermFreq, open(f"hashMaxTermFreqPickle{num}", "wb"))
        # print(maxTermFreq)
        print("finished, starting tfidf calculations")
        for terms in hashedIndex.terms():  # loop through all terms in the collection
            for DocWithTerm in hashedIndex.get_documents(terms):     # loop through all documents that have term in them
                tf = hashedIndex.get_term_frequency(terms, DocWithTerm, maxTermFreq[DocWithTerm])
                idf = hashedIndex.get_document_frequency(terms)
                if tf / idf:  # check if tf/idf > 0
                    if terms not in tfidf:
                        tfidf.update({terms: [f"{DocWithTerm}:{round(tf/idf,5)}"]})  # build tfidf
                    else:
                        tfidf[terms].append(f"{DocWithTerm}:{round(tf / idf, 5)}")
        # print(tfidf)
        print("finished, starting file dump")
        # df = pd.DataFrame(tfidf, index=tfidf.get('documents'))
        # print("finished, starting panda file dump")
        # df.to_json('hashedIndexDumpTest.json')
        with open(f'hashedIndexDump{num}.json', 'w')as fp:
            json.dump(tfidf, fp)
        pickle.dump(tfidf, open(f"hashTFIDFPickle{num}", "wb"))
    print("finished")
