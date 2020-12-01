from flaskblog.search.Database import Database
from flaskblog.search.InvertedIndex import InvertedIndex
import pickle
import sys
from flaskblog.search import Appearance
from collections import Counter
from random import randrange

sys.modules['Appearance'] = Appearance


class Search:
    """
    Inverted Index class.
    """

    def __init__(self):
        with open('flaskblog/static/paper_db.p', 'rb') as fp:
            new_db = pickle.load(fp)
        with open('flaskblog/static/paper_index.p', 'rb') as fp:
            new_index = pickle.load(fp)

        self.db = Database()
        self.index = InvertedIndex(self.db)

        self.db.set_db(new_db)
        self.index.set_index_and_db(new_index, new_db)

    def get_titles(self, docids):
        title_list = []
        for docid in docids:
            doc = self.db.get(docid)
            title_list.append([doc["title"], doc["link"]])
        return title_list

    def get_avoid_words(self, avoiding_docs, query):
        avoid_words = {}
        if(avoiding_docs):
            for docid in avoiding_docs:
                avoid_doc = self.db.get(docid)
                split = avoid_doc['text'].split(' ')
                counted = Counter(split)
                counted_final = {k: v for k, v in counted.items() if v > 2}
                for word, count in counted_final.items():
                    if(word not in query.split(' ')):
                        if(word in avoid_words):
                            avoid_words[word] += count
                        else:
                            avoid_words[word] = count
        return avoid_words

    def search_query(self, search_term, avoid_words=None):
        result = self.index.lookup_query(search_term)

        if(avoid_words):
            result = self.index.adjust_avoid_words(result, avoid_words)

        result_sorted = sorted(
            result.items(), key=lambda item: item[1], reverse=True)

        best_results = {}

        # loop through words instead of documents?

        for docfreqlist in result_sorted[:5]:
            # Belgium: { docId: 1, frequency: 1}
            document = self.db.get(docfreqlist[0])
            best_results[docfreqlist[0]] = [document['title'],
                                            str(docfreqlist[1]), document['summary'], document['link']]

        return best_results

    def search_dummy(self, search_term, docids=None):
        result = self.index.lookup_query(search_term)

        if(docids):
            result = self.index.scramble(result, docids)

        result_sorted = sorted(
            result.items(), key=lambda item: item[1], reverse=True)

        best_results = {}

        # loop through words instead of documents?
        random_freqs = [0.5 * randrange(20) + 15 for i in range(5)]
        iteration = 0
        for docfreqlist in result_sorted[:5]:
            # Belgium: { docId: 1, frequency: 1}
            document = self.db.get(docfreqlist[0])
            best_results[docfreqlist[0]] = [document['title'],
                                            str(random_freqs[iteration]), document['summary'], document['link']]
            iteration += 1

        return best_results