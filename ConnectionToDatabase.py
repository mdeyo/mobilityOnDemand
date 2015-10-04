__author__ = 'Matthew'

from couchdb import Server,Database

server = Server('http://localhost:5984/') #connects to remote server
database = None


class ConnectionToDatabase(object):

    def openDB(self,name):
        """Opens up connection to db of name and returns  object"""

        if(server.__contains__(name)):
            database = server.__getitem__(name)
        else:
            server.create(name)
            database = server.__getitem__(name)

        return database


#running test code
db = ConnectionToDatabase()
print('id',db.openDB("new_db").__getitem__("first_doc").id)
print('document',db.openDB("new_db").__getitem__("first_doc"))

