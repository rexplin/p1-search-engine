import pickle
import tkinter as tk
from collections import defaultdict, Counter
from sortedcontainers import SortedDict
from datetime import timedelta
from dateutil import parser
from justins_search_index import search_index
from snippet import get_snippet
import json


def most_frequent(query_log):
    """
    Return most frequent search query in the query log

    :param query_log: Log of all queries provided
    :return: Query that occurs most often
    """
    counter = Counter(query_log)
    most_common = counter.most_common(1)
    return most_common[0][0], most_common[0][1]


def query_score(candidate, query):
    """
    Determines the rank of a query suggestion candidate

    Function:     Freq(CQ) + Mod(CQ, q') + Time(CQ, q')
              ----------------------------------------------
              1 - min([Freq(CQ), Mod(CQ, q'), Time(CQ, q')])


    q': n-gram triggering the suggestion
    CQ: Candidate query to be scored
    QL: Query Log
    Freq(CQ): Frequency of CQ occurring in the Query Log, divided by the maximum frequency of
              occurrence of any query in QL
    Mod(CQ, q'): Number of sessions in which q' is modified to CQ divided by the total number
                 of sessions that q' appears in
    Time(CQ, q'): The minimum difference between the time occurrence of q' and CQ across sessions in which
                  both q' and CQ appear divided by the longest session length in QL

    :return: Score value for the candidate
    """

    # Calculate the Freq(CQ) value

    max_q_count = 83677  # Hardcoded because the above line takes a little bit to run
    freq_cq = querylog_data.count(candidate) / max_q_count

    q_sessions = set()
    mod_sessions = 0
    min_diff = timedelta(0)
    for q_occurs, c_occurs in zip(sessions[query], sessions[candidate]):
        # This is used to determine the number of sessions that contain q'
        q_sessions.add(q_occurs["sid"])

        # Determine how many times q' turns into CQ
        if q_occurs["sid"] == c_occurs["sid"] and parser.parse(c_occurs["time"]) > parser.parse(q_occurs["time"]):
            mod_sessions += 1

    total_sessions = len(q_sessions)
    mod_cq_q_prime = mod_sessions / total_sessions if total_sessions > 0 else 1

    longest_session = 7946741000
    time_cq_q_prime = (min_diff.total_seconds() * 1000) / longest_session

    num = freq_cq + mod_cq_q_prime + time_cq_q_prime
    denom = 1 - min([freq_cq, mod_cq_q_prime, time_cq_q_prime])

    return num / denom


def on_space(event):
    """
    Gets the value that has been input thus far and
    determines if it matches anything from the list
    if it does we update the listbox with that data
    :param event: space bar is pressed
    :return: None
    """
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()
    suggestions = SortedDict()

    # get data from test_list
    count = 0
    if value == '':
        data = ""
    else:
        for item in querylog_data:
            if item.lower().startswith(value):
                score = query_score(item, value)
                suggestions[score] = item

                count += 1
                if count >= 10:  # can use to decide how many results to show
                    break

        # Returns the 10 suggestions with highest scores of the 1000 found
        data = list(suggestions.values())[:10]

    # update data in listbox
    listbox_update(data)


def on_return(event):
    """
    Can be modified to sent our query into our search
    currently just prints whatever is in the entry box
    :param event: Enter is pressed
    :return: None
    """
    # get text from entry
    result = event.widget.get()

    # Change status message and empty the listbox of query suggestions
    display_message("Searching...")
    listbox_update(list())
    root.update()

    # Begin the search for the query
    related_documents = search_index(result, current_index)
    candidate_doc_ids = (related_doc.split(":")[0] for related_doc in related_documents[:20])

    # Retrieve snippets for Top 20
    snippets = list()
    for candidate_id in candidate_doc_ids:
        snippet = get_snippet(int(candidate_id), result)
        snippets.append(snippet)

    # Update status one more time
    display_message("Search complete!")
    root.update()

    textbox_update(snippets)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # put new data
    for item in data:
        listbox.insert('end', item)


def textbox_update(data):
    # delete previous data
    textbox.delete(1.0, 'end')

    # put new data
    for item in data:
        textbox.insert('end', item)


def on_select(event):
    """
    Gets the suggestion that was clicked an populates the entry box with it
    :param event:
    :return:
    """
    result = event.widget.get(event.widget.curselection())
    entry.delete(0, 'end')
    entry.insert(0, result)


def get_originals(related_documents):
    """
        Grabs the titles of the related documents to be returned

    :param related_documents: List of document ids retrieved from the index
    :return: List of document titles to be displayed for the user
    """
    document_titles = list()

    # Right now only finds 10 documents
    retrieval_list = related_documents[:10]

    for related_doc in retrieval_list:
        # TODO Change to final pathway that's self contained to project structure
        filename = f"../wiki-files-separated/output/wiki-doc-{related_doc}.json"
        with open(filename, "r") as original_doc:
            document = json.load(original_doc)
            document_titles.append(document["title"])

    return document_titles


# This is no longer used, it's simply left here to demonstrate what I did to find the value in the comment
def max_session_length(data):
    """
    Function to find longest session in a set of QL data

    Longest session value, in milliseconds in case it gets deleted: 7946741000

    :param data: Query log data
    :return: Returns length of longest session in QL
    """

    max_length = timedelta(0)
    for sid, timestamps in data.items():
        difference = timestamps[-1] - timestamps[0]
        if difference > max_length:
            max_length = difference

    return max_length


def display_message(msg):
    status_message.set(msg)


if __name__ == "__main__":
    with open('querylogs/Clean-Data.txt', 'r') as f:
        filedata = f.readlines()

    querylog_data = list()
    sessions = defaultdict(list)
    for line in filedata[1:]:
        columns = line.split('\t')
        sessions[columns[1]].append({"sid": columns[0], "time": columns[2]})
        querylog_data.append(columns[1])
    print("loading GUI")
    with open("hashTFIDFPickleFinal", "rb") as index_file:
        current_index = pickle.load(index_file)
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title("Search")

    status_message = tk.StringVar()
    display_message("What are you looking for?")
    status_label = tk.Label(root, textvariable=status_message, font="Times 12 italic", fg="black", height=1, width=75,
                            padx=10, pady=10)
    status_label.grid(row=1, column=1, sticky="W")

    label = tk.Label(root, text="Query:", font="Times 14 bold", fg="black", height=1, width=8)
    label.grid(row=2, column=0)
    entry = tk.Entry(root)
    entry.configure(width=200)
    entry.grid(row=2, column=1, columnspan=20, padx=10)

    entry.bind('<space>', on_space)
    entry.bind('<Return>', on_return)

    listbox_label = tk.Label(root, text="Suggested Queries:", font="Times 14 bold", fg="black", height=1, width=75)
    listbox_label.grid(row=4, column=1, sticky="W")

    listbox = tk.Listbox(root)
    listbox.configure(width=85, height=40)
    listbox.grid(row=5, column=1, columnspan=30, padx=10, pady=10, sticky="W")

    listbox.bind('<<ListboxSelect>>', on_select)

    textbox_label = tk.Label(root, text="Search Results:", font="Times 14 bold", fg="black", height=1, width=75)
    textbox_label.grid(row=4, column=9, sticky="W")

    textbox = tk.Text(root, wrap=tk.WORD)
    textbox.configure(width=85, height=50)
    textbox.grid(row=5, column=9, columnspan=30, padx=10, pady=10, sticky="W")

    root.mainloop()
