import pandas as pd
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    preds = pd.read_csv("predictions.csv")
    avg_demands = preds.groupby('location')['predicted_demand'].mean()
    
    # Depot (Index 0) + 10 Nodes = 11 locations
    demands = [0] + [int(avg_demands[f"Node_{i}"]) for i in range(1, 11)]
    
    data = {}
    num_locations = len(demands)
    np.random.seed(42)
    # Create a distance matrix where traveling is actually required
    data['distance_matrix'] = np.random.randint(10, 100, size=(num_locations, num_locations)).tolist()
    # Ensure distance from a node to itself is 0
    for i in range(num_locations):
        data['distance_matrix'][i][i] = 0
        
    data['demands'] = demands
    data['vehicle_capacities'] = [150, 150, 150]
    data['num_vehicles'] = 3
    data['depot'] = 0
    return data

def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return data['demands'][manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, data['vehicle_capacities'], True, 'Capacity')

    # THE KEY ADDITION: FORCE VISITS 
    # This ensures the solver doesn't just "skip" cities to save money
    for node in range(1, len(data['demands'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], 100000) # Penalty for skipping

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(data, manager, routing, solution)

def print_solution(data, manager, routing, solution):
    print(f"\n FINAL FLEET ROUTING PLAN")
    print("-" * 30)
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f"Truck {vehicle_id}: Depot"
        route_dist = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            plan_output += f" -> Node {manager.IndexToNode(index)}"
            route_dist += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        print(f"{plan_output}\n Distance: {route_dist}km\n")

if __name__ == '__main__':
    main()