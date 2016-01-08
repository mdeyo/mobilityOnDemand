__author__ = 'mdeyo'

from couchdb import Server,Database
import time
from MapGraph import MapGraph
from Search import RoutingProblem

#server = Server('http://localhost:5984/') #connects to remote server
#server = Server('http://mdeyo.iriscouch.com:5984/') #connects to remote server

class MapNode(object):

    def __init__(self, number,coords,neighbors):
        self.time_start = time.clock()
        #self.server = Server('http://'+laptop_address+':5984/') #connects to remote server
        self.server = Server('http://swarm:mobility@veh10.mit.edu:5984/') #connects to remote server
        self._number = number
        self.neighbors = neighbors
        self.coords = coords
        self.lat = coords[0]
        self.lon = coords[1]
        # print("created: "+str(number)+" at "+str(coords)+" with nearby "+str(neighbors))

    def get_neighbors(self):
        return self.neighbors

    def get_coords(self):
        return self.coords

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def print_string(self):
        return ("node:"+str(self._number)+" coords:"+str(self.coords)+" neighbors:"+str(self.neighbors))

    def distance_from(self,lat,lon):
        return abs((lat-self.lat)*(lat-self.lat)+(lon-self.lon)*(lon-self.lon))

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




