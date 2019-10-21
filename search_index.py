import pickle
import nltk
import json
from hashIndex import is_ascii
from fullStopWordList import stopwords as stop_words


def pre_process_query(query):
    stemmer = nltk.stem.snowball.EnglishStemmer()
    tokens = nltk.word_tokenize(query)
    ascii_tokens = [ascii_token for ascii_token in tokens if is_ascii(ascii_token)]
    filtered = [token.lower() for token in ascii_tokens if token not in stop_words]
    processed_tokens = [stemmer.stem(token) for token in filtered if token.isalpha()]
    final_tokens = [token for token in processed_tokens if token not in stop_words]

    return final_tokens


def search_index(term):
    """
    Load the index and look for documents related to a term

    :param term: Term to find documents for
    :return: List of documents related to the term
    """

    # Set up storage variables
    token_docs = list()
    final_documents = list()

    # Pre-process the search term, same as we do for generating the index
    search_tokens = pre_process_query(term)

    # Iterate through each index we have, and look for any documents for the term
    for token in search_tokens:
        potential_docs = list()
        for num in range(1, 9):
            with open(f"hashTFIDFPickle{num}", "rb") as index_file:
                current_index = pickle.load(index_file)
                potential_docs.extend(current_index.get(token, []))

        token_docs.append(potential_docs)

    token_docs.sort(key=len)

    if len(search_tokens) > 1:
        def compare(item):
            return item.split(":")[0] in shortest_doc_ids

        shortest = token_docs[0]
        shortest_doc_ids = [doc_id.split(":")[0] for doc_id in shortest]

        for token_doc in token_docs:
            matches = list(filter(compare, token_doc))
            if len(matches) > 0:
                final_documents.extend(matches)

    else:
        for token_doc in token_docs:
            final_documents.extend(token_doc)

    return sorted(final_documents, key=lambda x: x.split(":")[1], reverse=True)


def retrieve_originals(related_documents):
    """
        Grabs the titles of the related documents to be returned

    :param related_documents: List of document ids retrieved from the index
    :return: List of document titles to be displayed for the user
    """
    document_titles = list()

    # Right now only finds 10 documents
    retrieval_list = [doc.split(":")[0] for doc in related_documents[:20]]

    print("Building titles list...")
    for related_doc in retrieval_list:
        # TODO Change to final pathway that's self contained to project structure
        filename = f"../wiki-files-separated/output/wiki-doc-{related_doc}.json"
        with open(filename, "r") as original_doc:
            document = json.load(original_doc)
            document_titles.append(document["title"])

    return document_titles


if __name__ == "__main__":
    search_term = input("Give me a term: ")
    documents = search_index(search_term)
    titles = retrieve_originals(documents)
    # print(f"Found {len(documents)} related documents:\n\n")
    # print(sorted([int(document.split(":")[0]) for document in documents]))