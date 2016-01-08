__author__ = 'mdeyo'

class MapGraph(object):

    def __init__(self):
        self.nodes = dict()
        # print("created: MapGraph")

    def add_node(self,node):
        self.nodes[node._number] = node
        # print("added "+str(node._number)+" to map")

    def get_node(self,num):
        return self.nodes.get(num)

    def get_node_coords(self,num):
        # print "coords: "+str(self.nodes.get(num).get_coords())
        return self.nodes.get(num).get_coords()

    def get_nodes(self):
        return self.nodes

    def get_neighbors(self,num):
        return self.nodes.get(num).get_neighbors()

    def get_neighbor_nodes(self,num):
        neighbors = self.nodes.get(num).get_neighbors
        neighbor_nodes = list()
        for i in neighbors:
            neighbor_nodes.add(self.nodes.get(i))
        return neighbor_nodes

    def print_nodes(self):
        for n in self.nodes:
            print(self.nodes.get(n).print_string())

    def closest_node(self,lat,lon):
        min_distance = 999
        closest = None
        for n in self.nodes:
            node = self.nodes.get(n)
            distance = node.distance_from(lat,lon)
            if(distance<min_distance):
                min_distance = distance
                closest = node

        return closest._number



