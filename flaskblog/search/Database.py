class Database:
    """
    In memory database representing the already indexed documents.
    """

    def __init__(self):
        self.db = dict()

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.__dict__)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        """
        Adds a document to the DB.
        """
        return self.db.update({document['id']: document})

    def remove(self, document):
        """
        Removes document from DB.
        """
        return self.db.pop(document['id'], None)

    def get_db(self):
        return self.db

    def set_db(self, new_db):
        self.db = new_db
