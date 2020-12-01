from flaskblog.search.Appearance import Appearance
import re
import copy
from random import randrange


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """

        # Remove punctuation from the text.
        clean_text = re.sub(r'[^\w\s]', '', document['text'])
        terms = clean_text.split(' ')
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(
                document['id'], term_frequency + 1)

        # Update the inverted index
        update_dict = {key: {appearance.docId: appearance.frequency}
                       if key not in self.index
                       else self.index[key].update({appearance.docId: appearance.frequency})
                       for (key, appearance) in appearances_dict.items()}

        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        weights = dict()
        for term in query.split(' '):
            if(term in self.index):
                for (docid, frequency) in self.index[term].items():
                    if(docid in weights):
                        weights[docid] += frequency
                    else:
                        weights[docid] = frequency
        return weights

    def adjust_avoid_words(self, freqdic, avoid_words):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        weights = copy.deepcopy(freqdic)
        for docid in freqdic:
            for avoid_word, count in avoid_words.items():
                if(docid in self.index[avoid_word]):
                    weights[docid] -= 0.5 * \
                        self.index[avoid_word][docid] * count

        return weights
        
    def scramble(self, freqdic, docids):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        for docid in docids:
            if docid in freqdic:
                del freqdic[docid]

        weights = copy.deepcopy(freqdic)
        for docid in freqdic:
            weights[docid] = 0.5 * randrange(40)

        return weights

    def get_index(self):
        return self.index

    def set_index_and_db(self, new_index, new_db):
        self.index = new_index
        self.db = new_db
