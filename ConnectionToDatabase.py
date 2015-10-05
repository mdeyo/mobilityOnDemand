__author__ = 'mdeyo'

from couchdb import Server,Database

#server = Server('http://localhost:5984/') #connects to remote server
database = None

laptop_address = '18.189.46.85'
#server = Server('http://'+laptop_address+':5984/') #connects to remote server

server = Server('http://mdeyo.iriscouch.com:5984/') #connects to remote server

class ConnectionToDatabase(object):

    def __init__(self, name='server'):
        #self.server = Server('http://'+laptop_address+':5984/') #connects to remote server
        self.server = Server('http://mdeyo.iriscouch.com:5984/') #connects to remote server
        self._name = name
        self.ped_database = self.openDB("ped_db")
        self.vehicle_database = self.openDB("vehicle_db")
        print("connected!")

    def get_server(self):
        return self.server

    def openDB(self,name):
        """Opens up connection to db of name and returns  object"""
        if(server.__contains__(name)):
            database = server.__getitem__(name)
        else:
            server.create(name)
            database = server.__getitem__(name)

        return database

    def openDoc(self,name):
        """Opens up connection to db of name and returns  object"""
        if(self.database.__contains__(name)):
            doc = server.__getitem__(name)
        else:
            self.database.create(name)
            doc = server.__getitem__(name)

        return doc

    def add_pedestrian_data(self,id,time,pose):
        """Adds pedestrian data to the database"""
        # add pedestrian data with "id", timestamp, and pose
        ped_data_doc = "pedestrians"
        ped_doc = None
        if(self.ped_database.__contains__(id)):
            # if pedestrian id already exists - appends to history list and updates time
            ped_doc = self.ped_database.__getitem__(id)
            history = ped_doc['history']
            history.append((time,pose))
            ped_doc['history'] = history
            ped_doc['recent_time'] = time
            self.ped_database.save(ped_doc)
        else: # else, make new document with pedestrian id
            ped_doc = {'_id': id, 'history': [(time,pose)], 'recent_time':time}
            self.ped_database.save(ped_doc)
        return ped_doc

    def print_pedestrian_doc(self,ped_doc):
        print("Print Pedestrian Document: ID="+ped_doc._id)
        print('History:',)
        history_list = ped_doc['history']
        for i in history_list:
            print("Timestamp:"+i[0],"Position"+i[1])

####running test code####

# open up connection to vehicle_db#
db = ConnectionToDatabase()

server = db.get_server()

# add pedestrian data with "id", timestamp, and pose
#db.addPedestrianData("5600","12:50",(41,56))

# if pedestrian id already exists - appends to history list and updates time
#db.addPedestrianData("5600","12:50",(40,54))
#db.addPedestrianData("5601","12:50",(40,54))

#print(db.openDB("ped_db").__getitem__("5600"))

db.print_pedestrian_doc(db.openDB("ped_db").__getitem__("5600"))

#print('document',db.openDB("new_db").__getitem__("first_doc"))

