import nltk
import json
from hashIndex import is_ascii
from fullStopWordList import stopwords as stop_words

"""
    ONLY RUN IF HARDWARE IS GREATER THAN 27GB!!!!!
"""


def pre_process_query(query):
    stemmer = nltk.stem.snowball.EnglishStemmer()
    tokens = nltk.word_tokenize(query)
    ascii_tokens = [ascii_token for ascii_token in tokens if is_ascii(ascii_token)]
    filtered = [token.lower() for token in ascii_tokens if token not in stop_words]
    processed_tokens = [stemmer.stem(token) for token in filtered if token.isalpha()]
    final_tokens = [token for token in processed_tokens if token not in stop_words]

    return final_tokens


def search_index(term, current_index):
    """
    Load the index and look for documents related to a term

    :param term: Term to find documents for
    :return: List of documents related to the term
    """

    # Set up storage variables
    token_docs = list()
    shortest = list()
    final_final_documents = dict()

    # Pre-process the search term, same as we do for generating the index
    search_tokens = pre_process_query(term)

    # Iterate through each index we have, and look for any documents for the term
    for token in search_tokens:
        token_docs.append(current_index.get(token))

    token_docs.sort(key=len)

    if len(search_tokens) > 1:
        def compare(item):
            return item.split(":")[0] in shortest_doc_ids

        shortest = token_docs[0]
        shortest_doc_ids = [doc_id.split(":")[0] for doc_id in shortest]
        if len(token_docs) > 1:
            for token_doc in token_docs[1:]:
                matches = list(filter(compare, token_doc))
                if len(matches) > 0:
                    shortest = matches
                    shortest_doc_ids = [doc_id.split(":")[0] for doc_id in shortest]
    else:
        for token_doc in token_docs:
            shortest.extend(token_doc)
    for token_finalDoc in shortest:
        splitArray = token_finalDoc.split(":")
        splitID = splitArray[0]
        splitTFIDF = float(splitArray[1])
        if splitID in final_final_documents:
            pastTFIDF = float(final_final_documents.get(splitID).split(":")[1])
            final_final_documents.update({splitID: f"{splitID}:{((pastTFIDF + splitTFIDF) / len(search_tokens))}"})
        else:
            final_final_documents.update({splitID: f"{splitID}:{splitTFIDF}"})
    return sorted(list(final_final_documents.values()), key=lambda x: x.split(":")[1], reverse=True)


if __name__ == "__main__":
    search_term = input("Give me a term: ")
    documents = search_index(search_term)
    print(f"Found {len(documents)} related documents:\n\n")
