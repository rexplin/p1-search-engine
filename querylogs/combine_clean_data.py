if __name__ == "__main__":
    with open('Clean-Data.txt', 'x') as final:
        with open('Clean-Data-01.txt', 'r') as current:
            final.writelines(current.readlines())
        with open('Clean-Data-02.txt', 'r') as current:
            current.readline()  # gets rid of the column titles after the first doc
            final.writelines(current.readlines())
        with open('Clean-Data-03.txt', 'r') as current:
            current.readline()  # gets rid of the column titles after the first doc
            final.writelines(current.readlines())
        with open('Clean-Data-04.txt', 'r') as current:
            current.readline()  # gets rid of the column titles after the first doc
            final.writelines(current.readlines())
        with open('Clean-Data-05.txt', 'r') as current:
            current.readline()  # gets rid of the column titles after the first doc
            final.writelines(current.readlines())
