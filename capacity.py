from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import distances

###########################
# Problem Data Definition #
###########################
def create_data_model(num_vehicles, names, addresses, coordinatesMap, driver_capacities, customer_capacities):
  """Creates the data for the example."""
  data = {}
  data['API_key'] = 'akshardham'
  data['addresses'] = addresses
  # Array of distances between locations.
  _distances = distances.create_distance_matrix(data)

  demands = customer_capacities
  capacities = driver_capacities
  data["distances"] = _distances
  data["num_locations"] = len(_distances)
  data["num_vehicles"] = num_vehicles
  data["depot"] = 0
  data["demands"] = demands
  data["vehicle_capacities"] = capacities
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

def create_demand_callback(data):
    """Creates callback to get demands at each location."""
    def demand_callback(from_node, to_node):
        return data["demands"][from_node]
    return demand_callback

def add_capacity_constraints(routing, data, demand_callback):
    """Adds capacity constraint"""
    capacity = "Capacity"
    routing.AddDimensionWithVehicleCapacity(
        demand_callback,
        0, # null capacity slack
        data["vehicle_capacities"], # vehicle maximum capacities
        True, # start cumul to zero
        capacity)
###########
# Printer #
###########
def print_solution(data, routing, assignment, coordinatesMap):
    """Print routes on console."""
    temp = []
    info_list = []
    total_dist = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {0}:\n'.format(vehicle_id)
        route_dist = 0
        route_load = 0
        info_string = ''
        while not routing.IsEnd(index):
            node_index = routing.IndexToNode(index)
            next_node_index = routing.IndexToNode(assignment.Value(routing.NextVar(index)))
            route_dist += routing.GetArcCostForVehicle(node_index, next_node_index, vehicle_id)
            route_load += data["demands"][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            info_string += coordinatesMap[node_index] + "->"
            index = assignment.Value(routing.NextVar(index))

        node_index = routing.IndexToNode(index)
        total_dist += route_dist
        plan_output += ' {0} Load({1})\n'.format(node_index, route_load)
        temp.append(plan_output)
        temp.append("<br>")
        temp.append(info_string)
        temp.append("iamdelimiter")
        plan_output += 'Distance of the route: {0}m\n'.format(route_dist)
        plan_output += 'Load of the route: {0}\n'.format(route_load)
        print(plan_output)
    temp.append('Total Distance of all routes: {0}m'.format(total_dist))
    print('Total Distance of all routes: {0}m'.format(total_dist))
    return " ".join(temp)
########
# Main #
########
def main_function(num_vehicles, names, addresses, coordinatesMap, driver_capacities, customer_capacities):
  """Entry point of the program"""
  # Instantiate the data problem.
  data = create_data_model(num_vehicles, names, addresses, coordinatesMap, driver_capacities, customer_capacities)
  # Create Routing Model
  routing = pywrapcp.RoutingModel(
      data["num_locations"],
      data["num_vehicles"],
      data["depot"])
  # Define weight of each edge
  distance_callback = create_distance_callback(data)
  routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
# Add Capacity constraint
  demand_callback = create_demand_callback(data)
  add_capacity_constraints(routing, data, demand_callback)
  # Setting first solution heuristic (cheapest addition).
  search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
  search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
  # Solve the problem.
  assignment = routing.SolveWithParameters(search_parameters)
  if assignment:
    foobar = print_solution(data, routing, assignment, coordinatesMap)
    return foobar

