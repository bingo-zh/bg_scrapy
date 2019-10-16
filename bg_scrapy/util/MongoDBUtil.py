# -*- coding= utf-8 -*-


import pymongo

host = 'localhost'
port = 27017
username = 'username'
password = 'password'
db = 'db'
url = 'mongodb://{}:{}@{}:{}/{}'.format(username, password, host, port, db)


class MongoDBUtil(object):
    def __init__(self):
        self.client = pymongo.MongoClient(url)

    def get_client(self):
        return self.client

    def get_db(self):
        return self.get_client().get_database(db)

    def get_coll(self, collection='test'):
        return self.get_db().get_collection(collection)

    def close_client(self):
        if self.client:
            self.client.close()