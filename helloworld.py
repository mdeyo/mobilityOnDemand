from flask import Flask
from flask import request
from flask import render_template
from flask.ext.cors import CORS
from flask.ext.mail import Mail,Message
import requests
# import MapNode
import json
from MapGraph import MapGraph
from MapNode import MapNode
from Search import RoutingProblem
from couchdb import client, http, util, Server
import time
import random

####running test code####
# node1 = MapNode(1,[42.362071777875414, -71.08984494212564],[2,3,4,14])
node2 = MapNode(2, [42.36113631958969, -71.08957672122415], [1, 3, 4, 7, 8])
node3 = MapNode(3, [42.36110460889526, -71.08898663524087], [1, 2, 4, 6])
node4 = MapNode(4, [42.362008357414815, -71.0888471603721], [1, 2, 3, 5])
node5 = MapNode(5, [42.362194258434606, -71.08872967956813], [4])
node6 = MapNode(6, [42.3610645740965, -71.08832198379787], [3])
node7 = MapNode(7, [42.3610645740965, -71.08832198379787], [2])
node8 = MapNode(8, [42.36087510229148, -71.09040981527869], [2, 9, 10, 11])
node9 = MapNode(9, [42.3606729454999, -71.09032398459021], [8])
node10 = MapNode(10, [42.3606729454999, -71.09032398459021], [8])
node11 = MapNode(11, [42.36089888540067, -71.09097307917182], [8, 12, 13])
node12 = MapNode(12, [42.36079582519585, -71.09101599451606], [11])
node13 = MapNode(13, [42.36176696272522, -71.09148269888465], [11, 14])
node14 = MapNode(14, [42.36242494941883, -71.09015768763129], [13, 1])

map = MapGraph()
map.add_node(MapNode(1, [42.362071777875414, -71.08984494212564], [2, 3, 4, 14]))
map.add_node(node2)
map.add_node(node3)
map.add_node(node4)
map.add_node(node5)
map.add_node(node6)
map.add_node(node7)
map.add_node(node8)
map.add_node(node9)
map.add_node(node10)
map.add_node(node11)
map.add_node(node12)
map.add_node(node13)
map.add_node(node14)


# the vehicles currently logged on and running
available_vehicles = dict()
available_vehicles.clear()

# map.print_nodes()

app = Flask(__name__)
CORS(app)
mail = Mail(app)

app.config.update(
	# DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'mobilityondemand10@gmail.com',
	MAIL_PASSWORD = 'uavswarm'
	)

mail= Mail(app)

server = Server('http://swarm:mobility@veh10.mit.edu:5984/')
db = server['collect_data']
user_db = server['app_users']





# localtime = time.localtime()
# timeString  = time.strftime("%Y"+"/"+"%m"+"/"+"%d"+"/"+"%H"+":"+"%M"+":"+"%S", localtime)
# print(timeString)


@app.route('/')
def hello_world():


    return 'Hello World!'


@app.route('/more', methods=["GET", "POST"])
def showmore():
    return render_template('index.html', "name")
    # return 'more Hello World!'


@app.route('/user/<username>')
def profile(username):
    print username
    return username


@app.route('/signup/<username>')
def get_data(username):
    url = 'http://web.mit.edu/bin/cgicso?options=general&query=' + str(username)
    content = requests.get(url).content
    # print content
    checkline = "mailto:" + username
    goodKerberos = (checkline in content)

    msg = Message(
              'Mobility on Demand Project',
	       sender='mobilityondemand10@gmail.com',
	       recipients=
               [username+'@mit.edu'])

    password = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))

    msg.html = "<table><tr><td align='center'><img src=http://acl.mit.edu/members/images/newheader.jpg></td></tr><tr><td><h2>Thanks for signing up!</h2>Your password: "+password+" </td></tr><tr><td>From: ACL Mobility On Demand Group</td></tr></table>"

    mail.send(msg)

    if(goodKerberos):
        newID = getNextID()
        newDoc = {"check":goodKerberos,"_id":newID,'kerberos':username,'password':password}
        user_db.save(newDoc)
        return json.dumps(newDoc)
    else:
        return json.dumps({"check":goodKerberos,"user_id":"000"})

def getNextID():
    numberOfDocs = user_db.info()["doc_count"]
    newID = "%03d" % (numberOfDocs+1,)+"-"+str(random.randint(0,9999))
    print "newID: "+newID
    return newID;

@app.route('/testing')
def test_post():
    return requests.get(
        'http://stackoverflow.com/questions/15463004/how-can-i-send-a-get-request-from-my-flask-app-to-another-site').content


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print "login POST"
        content = request.get_json()
        print content
        print content['uid']

        uid = content['uid']
        password = content['pass']


        if (user_db.__contains__(uid)):
            print 'contains uid!'
            if(user_db.get(uid)['password']==password):
                print 'correct password!'
                return '1';
        else:
            return "0";

    else:
        return "GET"
        # show_the_login_form()


@app.route('/send', methods=['GET', 'POST'])
def check_json():
    print "got sendData"
    print "method:" + str(request.method)
    if request.method == 'POST':
        print "posted"
        content = request.get_json()
        print content

        start = content['start']
        goal = content['goal']
        id = content['id']

        problem = RoutingProblem(start, goal, available_vehicles, map)

        solution = problem.breadth_first_search

        doc = None

        if (db.__contains__(id)):
            doc = db.__getitem__(id)
            doc['status'] = "assigned"
            db.save(doc)
            print("assigned", doc.id)
        else:
            print 'request does not exist'

        print str(solution)

        send_to_vehicle(solution)

        return json.dumps(solution)
    else:
        problem2 = RoutingProblem([42.36113, -71.089576], [42.360672, -71.09032], map)
        solution = problem2.breadth_first_search
        print(solution)
        # return str(solution)
        return "<h1>Woah woah woah </h1>"
        # return "GET"
        # show_the_login_form()

def send_to_vehicle(routing):
    vehicle_number = routing['vehicle']
    if isinstance(vehicle_number, dict):
        vehicle_number=vehicle_number['driverNumber']
    print vehicle_number
    print('vehicle: ' + str(vehicle_number))
    # return vehicle_number
    # timestamp = time.localtime()
    # id = "route-"+timestamp
    firsttime = time.localtime()
    print firsttime
    localtime = time.strftime("%Y"+"/"+"%m"+"/"+"%d"+"/"+"%H"+":"+"%M"+":"+"%S", firsttime)
    print localtime
    newdoc = {"_id": "route-"+localtime,'routing':routing,"type": "route","created_at": localtime,"status":"allocated"}
    print newdoc
    # db.save(doc)
    return True



@app.route('/driverLogin', methods=['GET', 'POST'])
def driver_login():
    print "got driverLogin"
    # localtime = time.localtime()
    # timeString  = time.strftime("%Y"+"/"+"%m"+"/"+"%d"+"/"+"%H"+":"+"%M%"+":"+"S", localtime)
    # print(timeString)

    if request.method == 'POST':
        print "posted"
        content = request.get_json()
        print content

        driver_number = content['driverNumber']

        available_vehicles[driver_number] = content

        print(available_vehicles)

        # add vehicle to list of available vehicles

        return 'logged in!'
    else:
        print "gotted"
        return 'logged in!'


@app.route('/driverLogout', methods=['GET', 'POST'])
def driver_logout():
    if request.method == 'POST':
        print "logout posted"
        content = request.get_json()
        print content

        driver_number = content['driverNumber']

        if (available_vehicles.has_key(driver_number)):
            available_vehicles.__delitem__(driver_number)

        print('available_vehicles', available_vehicles)

        # add vehicle to list of available vehicles

        return 'logged out!'


# return json.dumps(r.json(), indent=4)


if __name__ == '__main__':
    # app.debug = True
    #app.run()
    app.run(host='0.0.0.0')
