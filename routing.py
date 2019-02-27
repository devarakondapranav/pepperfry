from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from flask import Flask,render_template, request
app = Flask(__name__)
import distances
import getCoordinates
from firebase import firebase
import capacity

ref = firebase.FirebaseApplication('https://sih-pepperfry.firebaseio.com', None)
###########################
# Problem Data Definition #
###########################


def updateDatabase(optimal_routes):
  pass


def create_data_model(num_vehicles, names, addresses):
  """Creates the data for the example."""
  data = {}
  data['API_key'] = 'akshardham'
  data['addresses'] = addresses
  # Array of distances between locations.
  # _distances = \
  #         [
  #          [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
  #          [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
  #          [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
  #          [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
  #          [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
  #          [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
  #          [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
  #          [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
  #          [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
  #          [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
  #          [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
  #          [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
  #          [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
  #          [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
  #          [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
  #          [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
  #          [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0]
  #         ]
  _distances = distances.create_distance_matrix(data)
  print((distances.create_distance_matrix(data)))
  data["distances"] = _distances
  data["num_locations"] = len(_distances)
  data["num_vehicles"] = num_vehicles
  data["depot"] = 0
  return data
#######################
# Problem Constraints #
#######################
def create_distance_callback(data):
  """Creates callback to return distance between points."""
  distances = data["distances"]

  def distance_callback(from_node, to_node):
    """Returns the manhattan distance between the two nodes"""
    return distances[from_node][to_node]
  return distance_callback

def add_distance_dimension(routing, distance_callback):
  """Add Global Span constraint"""
  distance = 'Distance'
  maximum_distance = 3000000  # Maximum distance per vehicle.
  routing.AddDimension(
      distance_callback,
      0,  # null slack
      maximum_distance,
      True,  # start cumul to zero
      distance)
  distance_dimension = routing.GetDimensionOrDie(distance)
  # Try to minimize the max distance among vehicles.
  distance_dimension.SetGlobalSpanCostCoefficient(100)
###########
# Printer #
###########
def print_solution(data, routing, assignment, coordinatesMap):
  """Print routes on console."""
  temp = []
  total_distance = 0

  
  info_list = []

  for vehicle_id in range(data["num_vehicles"]):
    index = routing.Start(vehicle_id)
    plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
    route_dist = 0
    info_string = ''
    while not routing.IsEnd(index):
      node_index = routing.IndexToNode(index)
      next_node_index = routing.IndexToNode(
        assignment.Value(routing.NextVar(index)))
      route_dist += routing.GetArcCostForVehicle(node_index, next_node_index, vehicle_id)
      plan_output += ' {0} ->'.format(node_index)
      info_string += coordinatesMap[node_index] + "->"
      index = assignment.Value(routing.NextVar(index))
    plan_output += ' {}\n'.format(routing.IndexToNode(index))
    plan_output += 'Distance of route: {}m<br>'.format(route_dist)
    #database sending ikada

    print(plan_output)
    temp.append(plan_output)
    temp.append(info_string)
    temp.append("iamdelimiter")
    total_distance += route_dist

  print('Total distance of all routes: {}m'.format(total_distance))
  temp.append('total distance is : {}m'.format(total_distance))
  return " ".join(temp)
########
# Main #
########
def main_function(num_vehicles, names, addresses,coordinatesMap):
  """Entry point of the program"""
  # Instantiate the data problem.
  data = create_data_model(num_vehicles, names, addresses)
  # Create Routing Model
  routing = pywrapcp.RoutingModel(
      data["num_locations"],
      data["num_vehicles"],
      data["depot"])
  # Define weight of each edge
  distance_callback = create_distance_callback(data)
  routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
  add_distance_dimension(routing, distance_callback)
  # Setting first solution heuristic (cheapest addition).
  search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
  search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC) # pylint: disable=no-member
  # Solve the problem.
  assignment = routing.SolveWithParameters(search_parameters)
  if assignment:
    return print_solution(data, routing, assignment, coordinatesMap)


@app.route('/')
def hello_world():
  print("hello guys")
  return render_template('table.html')

@app.route('/maps',methods=['POST','GET'])
def maps():

  a = []
  print("manager can see map")
  result = request.form
  #return str(result['num_vehicles'])
  if(result["typeOfRouting"] == "distance"):
    names = []
    addresses = []
    coordinatesMap = {}
    for i in range(int(result["rowcount"])):
      names.append(result["name" + str(i)])
      addresses.append(result["address" + str(i)])
      locCoordinate = getCoordinates.send_request(str(result["address" + str(i)]))
      coordinatesMap[i] = str(locCoordinate['lat']) + " " + str(locCoordinate['lng'])

    optimal_routes =  main_function(num_vehicles = int(result['num_vehicles']), names = names, addresses = addresses, coordinatesMap=coordinatesMap)
    updateDatabase(optimal_routes)
    return render_template("result.html", optimal_routes=optimal_routes, addresses= addresses)
  
  elif(result["typeOfRouting"] == "capacity"):
  
    names = []
    addresses = []
    customer_capacities = []
    driver_capacities = []
    coordinatesMap = {}
    for i in range(int(result["num_vehicles"])):
      driver_capacities.append(int(result["driver_capacity" + str(i)]))
    for i in range(int(result["rowcount"])):
      names.append(result["name" + str(i)])
      addresses.append(result["address" + str(i)])
      customer_capacities.append(int(result["capacity"+ str(i)]))
      
      locCoordinate = getCoordinates.send_request(str(result["address" + str(i)]))
      coordinatesMap[i] = str(locCoordinate['lat']) + " " + str(locCoordinate['lng'])


    optimal_routes =  capacity.main_function(num_vehicles = int(result['num_vehicles']), names = names, addresses = addresses, coordinatesMap=coordinatesMap, driver_capacities=driver_capacities, customer_capacities = customer_capacities)
    updateDatabase(optimal_routes)
    return render_template("result.html", optimal_routes=optimal_routes, addresses= addresses)
  

  else:
    return " SDKJVb"

@app.route('/submitToDB',methods=['POST','GET'])
def submitToDB():

  result = request.form
  optimal_routes = result["optimal_routes"];

  optimal_routes_list = list(optimal_routes.split("iamdelimiter"))
  #count = len(ref.get('/routes/26Feb2019', None))
    
  for x in range(len(optimal_routes_list)-1):
    temp = optimal_routes_list[x]
    temp = list(temp.split("<br>"))
    temp = temp[1]
    print('heyy ' + str(temp))
    obj = {}
    obj["assignedTo"] = None
    obj["status"] = "Ongoing"
    obj["coordinates"] = str(temp).strip()[:-2]


    ref.post('/routes/', obj)
  return "saved to database"



if __name__ == '__main__':
   app.run(host ='0.0.0.0', debug=True)
