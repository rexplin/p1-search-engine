import pickle
import nltk
from hashIndex import is_ascii
from fullStopWordList import stopwords as stop_words


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


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
    current_index = None
    shortest = list()
    final_final_documents = dict()

    # Pre-process the search term, same as we do for generating the index
    search_tokens = pre_process_query(term)

    # Iterate through each index we have, and look for any documents for the term
    for token in search_tokens:
        potential_docs = list()
        for num in range(1, 9):
            with open(f"hashed-tfidf/hashTFIDFPickle{num}", "rb") as index_file:
                current_index = pickle.load(index_file)
                potential_docs.extend(current_index.get(token))

        token_docs.append(potential_docs)
    if current_index:
        current_index.clear()
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
        split_array = token_finalDoc.split(":")
        split_id = split_array[0]
        split_tfidf = float(split_array[1])
        if split_id in final_final_documents:
            past_tfidf = float(final_final_documents.get(split_id).split(":")[1])
            final_final_documents.update({split_id: f"{split_id}:{((past_tfidf + split_tfidf) / len(search_tokens))}"})
        else:
            final_final_documents.update({split_id: f"{split_id}:{split_tfidf}"})

    return sorted(list(final_final_documents.values()), key=lambda x: x.split(":")[1], reverse=True)


if __name__ == "__main__":
    search_term = input("Give me a term: ")
    documents = search_index(search_term)
    print(f"Found {len(documents)} related documents:\n\n")
