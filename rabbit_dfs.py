def dfs_rabbit_leap(initial_state, goal_state, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if initial_state == goal_state:
        return path

    visited.add(tuple(initial_state))

    for i in range(len(initial_state)):
        if initial_state[i] == "_":
            # Check possible moves for 'E'
            if i > 0 and initial_state[i-1] == "E":  # Move left one step
                new_state = initial_state[:]
                new_state[i], new_state[i-1] = new_state[i-1], new_state[i]
                if tuple(new_state) not in visited:
                    result = dfs_rabbit_leap(new_state, goal_state, path + [(initial_state, new_state)], visited)
                    if result:
                        return result
            
            if i > 1 and initial_state[i-2] == "E":  # Jump left over a rabbit
                new_state = initial_state[:]
                new_state[i], new_state[i-2] = new_state[i-2], new_state[i]
                if tuple(new_state) not in visited:
                    result = dfs_rabbit_leap(new_state, goal_state, path + [(initial_state, new_state)], visited)
                    if result:
                        return result
            
            # Check possible moves for 'W'
            if i < len(initial_state) - 1 and initial_state[i+1] == "W":  # Move right one step
                new_state = initial_state[:]
                new_state[i], new_state[i+1] = new_state[i+1], new_state[i]
                if tuple(new_state) not in visited:
                    result = dfs_rabbit_leap(new_state, goal_state, path + [(initial_state, new_state)], visited)
                    if result:
                        return result
            
            if i < len(initial_state) - 2 and initial_state[i+2] == "W":  # Jump right over a rabbit
                new_state = initial_state[:]
                new_state[i], new_state[i+2] = new_state[i+2], new_state[i]
                if tuple(new_state) not in visited:
                    result = dfs_rabbit_leap(new_state, goal_state, path + [(initial_state, new_state)], visited)
                    if result:
                        return result

    return None


initial_state = ["E", "E", "E", "_", "W", "W", "W"]
goal_state = ["W", "W", "W", "_", "E", "E", "E"]
solution_dfs = dfs_rabbit_leap(initial_state, goal_state)

if solution_dfs:
    print("DFS Solution:")
    for step in solution_dfs:
        print(f"{step[0]} -> {step[1]}")
else:
    print("No solution found using DFS")