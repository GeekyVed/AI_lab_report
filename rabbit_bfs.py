from collections import deque

def bfs_rabbit_leap(initial_state, goal_state):
    queue = deque([(initial_state, [])])  # Each element is (state, path to reach state)
    visited = set()  # To keep track of visited states
    
    while queue:
        current_state, path = queue.popleft()
        
        if current_state == goal_state:
            return path
        
        visited.add(tuple(current_state))
        
        # Generate all possible moves
        for i in range(len(current_state)):
            if current_state[i] == "_":
                # Check possible moves for 'E'
                if i > 0 and current_state[i-1] == "E":  # Move left one step
                    new_state = current_state[:]
                    new_state[i], new_state[i-1] = new_state[i-1], new_state[i]
                    if tuple(new_state) not in visited:
                        queue.append((new_state, path + [(current_state, new_state)]))
                
                if i > 1 and current_state[i-2] == "E":  # Jump left over a rabbit
                    new_state = current_state[:]
                    new_state[i], new_state[i-2] = new_state[i-2], new_state[i]
                    if tuple(new_state) not in visited:
                        queue.append((new_state, path + [(current_state, new_state)]))
                
                # Check possible moves for 'W'
                if i < len(current_state) - 1 and current_state[i+1] == "W":  # Move right one step
                    new_state = current_state[:]
                    new_state[i], new_state[i+1] = new_state[i+1], new_state[i]
                    if tuple(new_state) not in visited:
                        queue.append((new_state, path + [(current_state, new_state)]))
                
                if i < len(current_state) - 2 and current_state[i+2] == "W":  # Jump right over a rabbit
                    new_state = current_state[:]
                    new_state[i], new_state[i+2] = new_state[i+2], new_state[i]
                    if tuple(new_state) not in visited:
                        queue.append((new_state, path + [(current_state, new_state)]))

    return None

initial_state = ["E", "E", "E", "_", "W", "W", "W"]
goal_state = ["W", "W", "W", "_", "E", "E", "E"]
solution_bfs = bfs_rabbit_leap(initial_state, goal_state)

if solution_bfs:
    print("BFS Solution:")
    for step in solution_bfs:
        print(f"{step[0]} -> {step[1]}")
else:
    print("No solution found using BFS")