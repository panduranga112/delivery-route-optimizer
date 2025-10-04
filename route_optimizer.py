import math
import sys

class RouteOptimizer:
    """
    A class to find an efficient delivery route using the Nearest Neighbor algorithm.
    """

    def __init__(self, locations):
        """
        Initialize the optimizer with delivery locations.

        Args:
            locations (list): A list of tuples where each tuple is (location_name, x_coordinate, y_coordinate).
                            The first location is assumed to be the warehouse/start point.
        """
        self.locations = locations
        self.num_locations = len(locations)
        self.graph = self._create_graph()

    def _calculate_distance(self, point1, point2):
        """
        Calculate the Euclidean distance between two points.

        Args:
            point1 (tuple): (x1, y1)
            point2 (tuple): (x2, y2)

        Returns:
            float: The Euclidean distance between point1 and point2.
        """
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def _create_graph(self):
        """
        Create a distance graph (adjacency matrix) from the list of locations.

        Returns:
            list: A 2D list representing the adjacency matrix of the graph.
        """
        graph = [[0 for _ in range(self.num_locations)] for _ in range(self.num_locations)]
        
        for i in range(self.num_locations):
            for j in range(i+1, self.num_locations):
                # Get coordinates for location i and j. Index 1 and 2 are x and y.
                dist = self._calculate_distance(
                    (self.locations[i][1], self.locations[i][2]),
                    (self.locations[j][1], self.locations[j][2])
                )
                graph[i][j] = dist
                graph[j][i] = dist
        return graph

    def find_optimal_route(self):
        """
        Find a sub-optimal route using the Nearest Neighbor greedy algorithm.

        Returns:
            tuple: (route_list, total_distance)
        """
        # Start from the warehouse (index 0)
        start_node = 0
        unvisited = set(range(1, self.num_locations))  # All nodes except the start
        route = [start_node]
        current_node = start_node
        total_distance = 0.0

        while unvisited:
            # Find the nearest unvisited neighbor
            nearest_node = None
            min_distance = sys.maxsize

            for neighbor in unvisited:
                if self.graph[current_node][neighbor] < min_distance:
                    min_distance = self.graph[current_node][neighbor]
                    nearest_node = neighbor

            # Move to the nearest neighbor
            route.append(nearest_node)
            unvisited.remove(nearest_node)
            total_distance += min_distance
            current_node = nearest_node

        # Return to the warehouse
        total_distance += self.graph[current_node][start_node]
        route.append(start_node)

        return route, total_distance

    def print_route(self, route, total_distance):
        """
        Print the optimized route in a human-readable format.

        Args:
            route (list): List of location indices representing the route.
            total_distance (float): Total distance of the route.
        """
        print("\n" + "="*50)
        print("          OPTIMIZED DELIVERY ROUTE")
        print("="*50)
        for i, location_index in enumerate(route):
            location_name = self.locations[location_index][0]
            if i == 0:
                print(f"Start -> {location_name} (Warehouse)")
            elif i == len(route) - 1:
                print(f"End   -> {location_name} (Back to Warehouse)")
            else:
                print(f"Stop {i:2d} -> {location_name}")
        print("="*50)
        print(f"Total Distance: {total_distance:.2f} units")
        print("="*50)

# --- INNOVATION & DEMONSTRATION ---
def create_sample_locations():
    """
    Create a sample set of delivery locations for demonstration.
    Returns a list of (name, x, y) tuples.
    """
    return [
        ("Warehouse", 0, 0),
        ("Office A", 2, 4),
        ("Office B", 7, 3),
        ("Cafe", 1, 6),
        ("School", 8, 7),
        ("Mall", 4, 1),
        ("Hospital", 6, 5),
        ("Park", 3, 8),
        ("Restaurant", 5, 2),
        ("Gym", 9, 4)
    ]

def main():
    """
    Main function to demonstrate the Route Optimizer.
    """
    print("🚚 DELIVERY ROUTE OPTIMIZER")
    print("Using Nearest Neighbor Algorithm for Efficient Routing\n")

    # Get user choice
    print("Choose an option:")
    print("1. Use sample locations (10 locations)")
    print("2. Enter custom locations")
    
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        locations = create_sample_locations()
    elif choice == "2":
        locations = [("Warehouse", 0, 0)]  # Start with warehouse
        print("\nEnter delivery locations (enter 'done' to finish):")
        i = 1
        while True:
            name = input(f"Enter name for location {i}: ").strip()
            if name.lower() == 'done':
                break
            try:
                x = int(input(f"  X coordinate for {name}: "))
                y = int(input(f"  Y coordinate for {name}: "))
                locations.append((name, x, y))
                i += 1
            except ValueError:
                print("  Please enter valid integers for coordinates.")
    else:
        print("Invalid choice. Using sample locations.")
        locations = create_sample_locations()

    # Create optimizer and find route
    optimizer = RouteOptimizer(locations)
    optimal_route, total_distance = optimizer.find_optimal_route()

    # Display results
    optimizer.print_route(optimal_route, total_distance)

    # Show efficiency comparison
    n = len(locations)
    print(f"\n💡 EFFICIENCY METRICS:")
    print(f"   Number of locations: {n}")
    print(f"   Operations performed by our algorithm: ~{n**2}")
    print(f"   Operations for brute force (theoretical): {math.factorial(n-1):,}")
    print(f"   Our algorithm is {math.factorial(n-1) / (n**2):,.0f} times faster than brute force!")

if __name__ == "__main__":
    main()

#     Innovation & Optimization Highlights:
# Object-Oriented Design: The code is structured in a class for reusability and clarity.

# User Interaction: Users can choose between sample data or enter their own custom locations.

# Efficiency Visualization: The program calculates and displays how much faster it is than the brute-force method.

# Clean Output: The route is presented in a clear, easy-to-read format.

# Mathematical Foundation: Uses Euclidean distance for realistic route calculation.
