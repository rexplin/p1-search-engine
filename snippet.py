import nltk
import simplejson
from fullStopWordList import stopwords as stop_words


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
        # WOULD LIKE TO OPTIMIZE SO WE CAN INDEX DIRECTLY TO WHERE ID=DOC_ID
        stemmer = nltk.stem.snowball.EnglishStemmer()
        for entry in f:
            document = simplejson.loads(entry)
            # finds the document with the correct id
            if document["id"] == doc_id:
                print(document["title"])  # for now it prints the title, could be changed to add title to return string?
                # print(document["content"])
                # tokenizes the content of the document by sentences
                sentences = nltk.sent_tokenize(f"{document['content']}")
                for sentence in sentences:
                    # tokenizes the sentence by words, then removes stopwords and converts to lowercase
                    # then it stems the words, and makes sure they are an alphanumeric word
                    words = nltk.word_tokenize(sentence)
                    filtered = [word.lower() for word in words if word not in stop_words]
                    processed_tokens = [stemmer.stem(word) for word in filtered if word.isalpha()]

                    # searches the previously processed list of tokens to see if they contain the query terms
                    # the sentence will only be printed if all the query terms are found
                    for term in query_terms:
                        found = False
                        for token in processed_tokens:
                            if term == token:
                                found = True
                                break
                        if not found:
                            break
                    if found:
                        print(sentence)
                break


if __name__ == "__main__":
    query = ['adolf', 'swedish', 'model', 'architect']
    doc = 35
    # CURRENTLY ASSUMES THAT THE QUERY HAS ALREADY BEEN STEMMED AND TOKENIZED
    get_snippet(doc, query)
