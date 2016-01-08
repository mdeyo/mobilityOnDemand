__author__ = 'Matthew'

# from MapGraph import MapGraph
# from MapNode import MapNode
import json

class RoutingProblem(object):
    """Class that represents the puzzle search problem."""
    def __init__(self, start, goal,available_vehicles,map_graph):
        # print(start)
        self.start = map_graph.closest_node(start[0],start[1])
        self.goal = map_graph.closest_node(goal[0],goal[1])
        self.map = map_graph
        self.vehicles = available_vehicles
    def test_goal(self, state):
        return self.goal == state
    def expand_node(self, search_node):
        """Return a list of SearchNodes, having the correct state and parent node."""
        states = self.map.get_neighbors(search_node._state)
        list_of_SearchNodes=list()

        if(len(states)==0):
            #no searchNode to expand to
            print('error')
        for one_state in states:
            list_of_SearchNodes.append(SearchNode(one_state,self.map.get_node_coords(one_state),parent_node=search_node))

        expanded_sn=list_of_SearchNodes

        return expanded_sn

    @property
    def breadth_first_search(self):

        """This function should take a PuzzleProblem instance
        and return a 3 element tuple as described above."""

        if(len(self.vehicles)==0):
            return {'message':'no available vehicles :(','vehicle':'0'}

        #intialize Q with S
        Q = list()
        print("self.start: "+str(self.start))
        Q.append(SearchNode(self.start,self.map.get_node_coords(self.start),None))

        visitedList = set([Q[0]._state])
        #visitedList.append(Q[0]._state)
        max_Q=0
        numNodes=0
        goal = self.goal
        solution = None

        while(len(Q)>0):
            #pick partial path N from Queue
            firstNode = Q[0]

            numNodes+=1

            if(self.test_goal(firstNode._state)):
                #all done - goal found!
                solution = firstNode
                print("found goal!")
                break
            else:
                #remove current SearchNode from the Q
                Q.remove(firstNode)
                #use expand_node method to find children SearchNodes
                list_of_SearchNodes = self.expand_node(firstNode)
                #add the children SearchNodes to the Q - BFS at end of Q
                for item in list_of_SearchNodes:
                    #only if they aren't in the visitedList already
                    if item._state not in visitedList:
                        #BFS line of code - add to end of queue
                        Q.append(item)
                        #DFS line of code - add to beginning of queue
                        #Q.insert(0,item)
                        # update the visitedList - actually a set!
                        visitedList.add(item._state)

                if(len(Q)>max_Q):
                    max_Q=len(Q)

        finalPath = None

        if(solution!=None):
                finalPath = Path(solution)

        #return the three outputs described above
        #return(finalPath,numNodes,max_Q)
        print finalPath
        print finalPath.get_path_coords()
        print self.vehicles
        print self.vehicles[1]
        return {'vehicle':self.vehicles[1],'message':'solved','path':finalPath.get_path_coords()}
        # return finalPath

        # return str(finalPath.get_path_coords())
        # return(finalPath,len(visitedList),max_Q)


class SearchNode(object):
    def __init__(self, state, coords, parent_node=None):
        self._parent = parent_node
        self._state = state
        self.coords = coords

    def get_coords(self):
        return self.coords

    def __repr__(self):
        return "<SearchNode: state: %s,coords: %s parent: %s>" % (repr(self.state),str(self.coords),repr(self.parent))

    def expand(self, graph):
        """Returns new search nodes pointing to each children state of the state represented by this node."""
        return [SearchNode(state, self) for state in graph.children_of(self.state)]

    @property
    def state(self):
        """Get the state represented by this SearchNode"""
        return self._state

    @property
    def parent(self):
        """Get the parent search node that we are coming from."""
        return self._parent

    def __eq__(self, other):
        return isinstance(other, SearchNode) and self._state == other._state

    def __hash__(self):
        return hash(self._state)

class Path(object):
    """This class computes the path from the starting state until the state specified by the search_node
    parameter by iterating backwards."""
    def __init__(self, search_node):
        self.path = []
        self.path_coords = []
        node = search_node
        while node is not None:
            self.path.append(node.state)
            self.path_coords.append(node.get_coords())
            node = node.parent
        self.path.reverse()
        self.path_coords.reverse()
    def __repr__(self):
        return "Path of length %d: %s" % (len(self.path), self.path)
    def get_path_coords(self):
        return self.path_coords


####running test code####
# node1 = MapNode(1,[42.362071777875414, -71.08984494212564],[2,3,4,14])
# node2 = MapNode(2,[42.36113631958969, -71.08957672122415],[1,3,4,7,8])
# node3 = MapNode(3,[42.36110460889526, -71.08898663524087],[1,2,4,6])
# node4 = MapNode(4,[42.362008357414815, -71.0888471603721],[1,2,3,5])
# node5 = MapNode(5,[42.362194258434606, -71.08872967956813],[4])
# node6 = MapNode(6,[42.3610645740965, -71.08832198379787],[3])
# node7 = MapNode(7,[42.3610645740965, -71.08832198379787],[2])
# node8 = MapNode(8,[42.36087510229148, -71.09040981527869],[2,9,10,11])
# node9 = MapNode(9,[42.3606729454999, -71.09032398459021],[8])
# node10 = MapNode(10,[42.3606729454999, -71.09032398459021],[8])
# node11 = MapNode(11,[42.36089888540067, -71.09097307917182],[8,12,13])
# node12 = MapNode(12,[42.36079582519585, -71.09101599451606],[11])
# node13 = MapNode(13,[42.36176696272522, -71.09148269888465],[11,14])
# node14 = MapNode(14,[42.36242494941883, -71.09015768763129],[13,1])
#
# map = MapGraph()
# map.add_node(MapNode(1,[42.362071777875414, -71.08984494212564],[2,3,4,14]))
# map.add_node(node2)
# map.add_node(node3)
# map.add_node(node4)
# map.add_node(node5)
# map.add_node(node6)
# map.add_node(node7)
# map.add_node(node8)
# map.add_node(node9)
# map.add_node(node10)
# map.add_node(node11)
# map.add_node(node12)
# map.add_node(node13)
# map.add_node(node14)
#
# # print(map.get_nodes())
# map.print_nodes()
#
# problem = RoutingProblem(1,10,map)
# solution = problem.breadth_first_search()
# print solution
