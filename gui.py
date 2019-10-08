import tkinter as tk


def on_space(event):
    """
    Gets the value that has been input thus far and
    determines if it matches anything from the list
    if it does we update the listbox with that data
    :param event: space bar is pressed
    :return: None
    """
    print("Hey you hit the space bar!")
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = ""
    else:
        data = []
        # a very basic sort, if any item in the list contains the text we got from the entry,
        # then that is added to the results list
        for item in querylog_data:
            if value in item.lower():
                data.append(item)

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
    print(result)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    """
    Gets the suggestion that was clicked an populates the entry box with it
    :param event:
    :return:
    """
    result = event.widget.get(event.widget.curselection())
    entry.delete(0, 'end')
    entry.insert(0, result)


if __name__ == "__main__":
    test_list = ('python how to', 'python select', 'python unit tests')

    with open('querylogs/Clean-Data-01.txt', 'r') as f:
        filedata = f.readlines()

    querylog_data = []
    for line in filedata:
        columns = line.split('\t')
        querylog_data.append(columns[1])

    root = tk.Tk()

    entry = tk.Entry(root)
    entry.pack()

    entry.bind('<space>', on_space)
    entry.bind('<Return>', on_return)

    listbox = tk.Listbox(root)
    listbox.pack()

    listbox.bind('<<ListboxSelect>>', on_select)

    root.mainloop()
