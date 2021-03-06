__author__ = 'mdeyo'

from couchdb import Server,Database
import time

#server = Server('http://localhost:5984/') #connects to remote server
#server = Server('http://mdeyo.iriscouch.com:5984/') #connects to remote server

class ConnectionToDatabase(object):

    def __init__(self, name='server'):
        self.time_start = time.clock()
        #self.server = Server('http://'+laptop_address+':5984/') #connects to remote server
        self.server = Server('https://swarm:mobility@veh10.mit.edu:5984/') #connects to remote server
        self._name = name
        self.ped_database = self.open_db("test_db")
        self.vehicle_database = self.open_db("vehicle_db")
        print("connected!")

    def get_server(self):
        return self.server

    def get_start_time(self):
        return self.time_start

    def open_db(self,name):
        """Opens up connection to db of name and returns  object"""
        if(self.server.__contains__(name)):
            database = self.server.__getitem__(name)
        else:
            self.server.create(name)
            database = self.server.__getitem__(name)

        return database

    def open_doc(self,name):
        """Opens up connection to db of name and returns  object"""
        if(self.database.__contains__(name)):
            doc = self.server.__getitem__(name)
        else:
            self.database.create(name)
            doc = self.server.__getitem__(name)

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

    def add_pedestrian_data2(self,id,list_of_points):
        """Adds pedestrian data to the database"""
        # add pedestrian data with "id", timestamp, and pose
        ped_data_doc = "pedestrians"
        ped_doc = None
        if(self.ped_database.__contains__(id)):
            # if pedestrian id already exists - appends to history list and updates time
            ped_doc = self.ped_database.__getitem__(id)
            history = ped_doc['history']
            history.append(list_of_points)
            ped_doc['history'] = history
            ped_doc['recent_time'] = time
            self.ped_database.save(ped_doc)
        else: # else, make new document with pedestrian id
            ped_doc = {'_id': id, 'history': [list_of_points], 'recent_time':time}
            self.ped_database.save(ped_doc)
        return ped_doc

    def print_pedestrian_doc(self,ped_doc):
        print("Print Pedestrian Document: ID="+ped_doc.id)
        print("Most Recent Time: "+ped_doc['recent_time'])

        print'History:'
        history_list = ped_doc['history']
        for i in history_list:
            print("Timestamp:"+str(i[0]),"Position:"+str(i[1]))

####running test code####

# open up connection to vehicle_db#
db = ConnectionToDatabase()

test_db = db.open_db("test_db")
print(db.add_pedestrian_data("500",5,20))

ped_doc = {'_id': "200", 'history': 5, 'recent_time':100}
data = db.ped_database.save(ped_doc)
print(data[1])

ped_doc = {'_id': "200", '_rev':data[1],'history': 10, 'recent_time':200}
data = db.ped_database.save(ped_doc)


# ped_doc = {'_id': 100, 'history': [(10,10)], 'recent_time':1240}
# print test_db.__getitem__("made by hand");

# test_db.

# test_db.save(ped_doc)

# print(test_db.info())


# server = db.get_server()

# add pedestrian data with "id", timestamp, and pose
# db.addPedestrianData("5600","12:50",(41,56))

# if pedestrian id already exists - appends to history list and updates time
# db.add_pedestrian_data("5600","13:50",(5,5))
#db.addPedestrianData("5601","12:50",(40,54))

#print(db.openDB("ped_db").__getitem__("5600"))

# db.print_pedestrian_doc(db.open_db("ped_db").__getitem__("5600"))

# print(db.open_db("ped_db").__getitem__("5600"))

#print('document',db.open_db("new_db").__getitem__("first_doc"))

#print("time elapsed",str(time.clock()-db.get_start_time()))

