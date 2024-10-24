from collections import deque 
from db_connection import get_db_connection 
import heapq
from collections import defaultdict
import math

# Function to get the city_id based on the city_name from the cities table
def get_city_id(city_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT city_id FROM Cities WHERE city_name = %s", (city_name,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            print("No city found")
    finally:
        cur.close()
        conn.close()

# Function to get the city_name based from the cities table
def get_city_name(city_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT city_name FROM Cities WHERE city_id = %s", (city_id,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            print("No city_name found")
    finally:
        cur.close()
        conn.close()

# Function to check whether a city is in the database 
def city_in_DB(city_name):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get the city ID 
    city_id = get_city_id(city_name)
    try:
        cur.execute("""
            SELECT city_name 
            FROM Cities
            WHERE city_id = %s""",
                    (city_id,))

        result = cur.fetchone()
        
        if result:
            return True
        else:
            return False
    finally:
        cur.close()
        conn.close()

# Function to get the neighbor cities of particular cities from the connections table 
def get_neighbors(city_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Cities.city_name, Connections.distance
            FROM Cities JOIN Connections 
            ON Cities.city_id = Connections.end_city_id
            WHERE Connections.start_city_id = %s 
        """, (city_id,))
        results = cur.fetchall()

        neighbors = []
        if results:
            for neighbor in results:
                # Convert the distance from Decimal (from the database) to an integer
                city_name = neighbor[0]
                distance = int(neighbor[1])
                neighbors.append((city_name, distance))
            return neighbors
        else:
            print("No neighbor city found")
    finally:
        cur.close()
        conn.close()

# BFS function to find the goal city starting from a particular city.
# It explores cities using a queue. It uses the FIFO (First In First Out) structure.
# The first city in the queue is explored first.
def bfs(start_city_name, goal_city_name):
    # Getting the start and goal city ID 
    start_city_id = get_city_id(start_city_name)
    goal_city_id = get_city_id(goal_city_name)

    if start_city_id is None or goal_city_id is None:
        return None

    queue = deque()
    queue.append((start_city_id, [start_city_name]))
    visited = set()

    while queue:
        current_city_id, path = queue.popleft()

        # Check if a goal was found
        if current_city_id == goal_city_id:
            return path

        # Otherwise look for the goal
        if current_city_id not in visited:
            visited.add(current_city_id)

            # Get neighbors and sort them alphabetically before appending
            neighbors = sorted(get_neighbors(current_city_id), key=lambda x: x[0])
            for neighbor, _ in neighbors:
                # Get the neighbor city_id 
                neighbor_id = get_city_id(neighbor)

                if neighbor_id not in visited:
                    if neighbor_id == goal_city_id:
                        return path + [neighbor]
                
                    queue.append((neighbor_id, path + [neighbor]))
   
    return None # Return None if no path is found 

# DFS function to find the goal city starting from a particular city.
# It explores cities using a stack. It uses the LIFO (Last In First Out) structure.
# The last city in the stack (top) is explored First
def dfs(start_city_name, goal_city_name):
    start_city_id = get_city_id(start_city_name)
    goal_city_id = get_city_id(goal_city_name)

    if start_city_id is None or goal_city_id is None:
        return None 
    
    stack = deque()
    stack.append((start_city_id, [start_city_name]))
    visited = set()
    
    while stack:
        current_city_id, path = stack.pop()

        # if the city has already been visited, skip it 
        if current_city_id in visited:
            continue

        # Check if a goal was found
        if current_city_id == goal_city_id:
            return path
        
        # Otherwise look for the goal
        if current_city_id not in visited:
            visited.add(current_city_id)

        # Get and push to the stack all univisted neighbors in reverse alphabetical order
        neighbors = sorted(get_neighbors(current_city_id), key = lambda x: x[0], reverse=True)
        for neighbor, _ in neighbors:
            # Get the neighbor city_id
            neighbor_id = get_city_id(neighbor)

            if neighbor_id not in visited:
                if neighbor_id == goal_city_id:
                    return path + [neighbor]

                stack.append((neighbor_id, path + [neighbor]))

    return None # Return None if no path is found 

# UCS function to find the goal city from the current_city using 
# the weight of the graph to get an optimal solution. 
# It starts exploring using the city that has the lowest edge-weight (cost).
def ucs(start_city_name, goal_city_name):
    start_city_id = get_city_id(start_city_name)
    goal_city_id = get_city_id(goal_city_name)

    if start_city_id is None or goal_city_id is None:
        return None

    pq = []
    heapq.heappush(pq, (0, start_city_id, [f"{start_city_name} : {0}"])) # The starting cost is 0
    visited = set()

    while pq:
        path_cost, current_city_id, path = heapq.heappop(pq)

        # Check if a goal was found
        if current_city_id == goal_city_id:
            return path

        # Otherwise look for the goal
        if current_city_id not in visited:
            visited.add(current_city_id)

        # Get neighbors of the current_city
        neighbors = get_neighbors(current_city_id)

        # Push the neighbors to the priority_queue in order to get them 
        # in terms of their edge-weight (cost) (lowest to highest)
        for neighbor, cost in neighbors:
            neighbor_id = get_city_id(neighbor)

            if neighbor_id not in visited:
                new_cost = path_cost + cost
                heapq.heappush(pq, (new_cost, neighbor_id, path + [f"{neighbor} : {new_cost}"]))

    return None # Return None if no path is found

# Function to get the latitude and longitude for each city
def get_coordinates(city_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT latitude, longitude
            FROM Cities
            WHERE city_id = %s 
        """, (city_id,))
        result = cur.fetchone()
        
        if result:
            latitude = float(result[0])
            longitude = float(result[1])
            coordinates = (latitude, longitude)
            return coordinates
        else:
            print("No city_coordinates found")
    finally:
        cur.close()
        conn.close()

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    x1, y1 = a 
    x2, y2 = b 

    # Calculate the Manhattan distance 
    manhattan_distance = abs(x1 - x2) + abs(y1 - y2)

    return manhattan_distance

# A* algorithm implementation. It finds the path by using a prioirity queue.
# The cost/priority which is the estimated total cost (fScore) is calculate by adding
# the actual cost of the node (gScore) and the heuristic cost.
# It starts exploring the node that has the lowest estimated total cost (fscore).
def a_star_search(start_city_name, goal_city_name):
    start_city_id = get_city_id(start_city_name)
    goal_city_id = get_city_id(goal_city_name)

    if start_city_id is None or goal_city_id is None:
        return None 
    
    openSet = [] # Nodes to be evaluated, prioritized by f(n) = g(n) + h(n)
    heapq.heappush(openSet, (0, start_city_id))
    openSet_set = {start_city_id}

    cameFrom = {} # To keep track of the path 

    gScore = defaultdict(lambda: math.inf) # Initialize the default value of g(n) as infinity
    gScore[start_city_id] = 0

    fScore = defaultdict(lambda: math.inf) # Initialize the default value of f(n) as infinity
    fScore[start_city_id] = heuristic(get_coordinates(start_city_id), get_coordinates(goal_city_id))

    # If there are nodes in the priority_queue, try to find the path 
    while openSet:
        current_city_id = heapq.heappop(openSet)[1]
        openSet_set.remove(current_city_id)

        # If the goal is found, return the path found
        if current_city_id == goal_city_id:
            return reconstructPath(cameFrom, current_city_id) # Goal reached, build the path 
        
        # Get the neighbors of the current_city 
        neighbors = get_neighbors(current_city_id)

        # Calculate the gScore and the fScore for the neighbor city and add them to the priority queue
        for neighbor, distance in neighbors:
            neighbor_id = get_city_id(neighbor)
            tentative_gScore = gScore[current_city_id] + distance

            if tentative_gScore < gScore[neighbor_id]:
                cameFrom[neighbor_id] = current_city_id # Record path 
                gScore[neighbor_id] = tentative_gScore
                fScore[neighbor_id] = gScore[neighbor_id] + heuristic(get_coordinates(neighbor_id), get_coordinates(goal_city_id))

                if neighbor_id not in openSet_set:
                    heapq.heappush(openSet, (fScore[neighbor_id], neighbor_id))
                    openSet_set.add(neighbor_id)

    return None # No path found 

# Function to reconstruct the path found using a*star algorithm
def reconstructPath(cameFrom, current_city_id):
    total_path = [current_city_id]
    while current_city_id in cameFrom:
        current_city_id = cameFrom[current_city_id]
        total_path.append(current_city_id)

    total_path.reverse()

    total_path_names = []
    for city_id in total_path:
        total_path_names.append(get_city_name(city_id))

    return total_path_names

