from collections import defaultdict
from tqdm import tqdm


class QueryLog(object):
    """
        This is a class that allows for interacting with the querylog data. Mainly used for determining query
        suggestions

    """

    def __init__(self):
        self.sid_dict = defaultdict(set)
        self.query_dict = defaultdict(set)

    def process_log(self, log_data):
        for line in tqdm(log_data):
            columns = line.split('\t')
            sid = int(columns[0])
            query = columns[1]

            self.sid_dict[sid].add(query)
            self.query_dict[query].add(sid)

    def session(self, query):
        return self.query_dict.get(query)

    def query(self, session_id):
        return self.sid_dict.get(session_id)

    def sessions(self):
        return self.sid_dict

    def queries(self):
        return self.query_dict

    def count(self, query):
        sessions = self.session(query)
        return len(sessions) if sessions else 0


def load(filename):
    # querylogs / Clean - Data.txt
    with open(filename, 'r') as f:
        filedata = f.readlines()

        iterable_data = filedata[1:]
        # iterator = tqdm(iterable_data, total=len(iterable_data))
        query_log = QueryLog()
        query_log.process_log(iterable_data)

        # columns = line.split('\t')
        # sessions[columns[1]].append({"sid": columns[0], "time": columns[2]})
        # querylog_data.append(columns[1])

        return query_log
