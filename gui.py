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
        for item in test_list:
            if value in item.lower():
                data.append(item)

    # update data in listbox
    listbox_update(data)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    # display element selected on list
    print('(event) previous:', event.widget.get('active'))
    print('(event)  current:', event.widget.get(event.widget.curselection()))
    print('---')


if __name__ == "__main__":
    test_list = ('python how to', 'python select', 'python unit tests')

    root = tk.Tk()

    entry = tk.Entry(root)
    entry.pack()

    entry.bind('<space>', on_space)

    listbox = tk.Listbox(root)
    listbox.pack()

    listbox.bind('<<ListboxSelect>>', on_select)

    root.mainloop()
