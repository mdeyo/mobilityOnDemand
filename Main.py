
__author__ = 'mdeyo'


from couchdb import client, http, util, Server


#server = Server()# connects to the local_server

server = Server('http://localhost:5984/') #connects to remote server

#create new database on server
#db = server.create("new_db")

#open existing database on server
db = server['new_db']

idString = 'second_doc'

doc = None

if(db.__contains__(idString)):
    doc = db[idString]
else:
    db[idString] = {'type': 'person', 'name': idString}
    doc = db[idString]


print(doc)
print(doc.rev)
