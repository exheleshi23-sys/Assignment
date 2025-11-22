import heapq

class PriorityQueue:
    """A simple Priority Queue wrapper around heapq."""
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        priority, item = heapq.heappop(self.elements)
        return priority, item


def a_star_search(start_state, goal_test, get_successors, get_cost, heuristic):
    """
    A* Search Algorithm
    
    f(n) = g(n) + h(n)
    
    Args:
        start_state: initial state
        goal_test(state): returns True if state is goal
        get_successors(state): returns list of (action, next_state)
        get_cost(state, action, next_state): actual cost to move
        heuristic(state): estimated cost from state to goal
    """

    frontier = PriorityQueue()
    frontier.put(0, start_state)
    visited = {}
    cost_so_far = {start_state: 0}

    while not frontier.empty():
        curr_priority, state = frontier.get()

        if goal_test(state):
            return cost_so_far[state], state

        if state in visited:
            continue
        visited[state] = True

        for action, next_state in get_successors(state):
            new_cost = cost_so_far[state] + get_cost(state, action, next_state)
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state)
                frontier.put(priority, next_state)

    return None


# ---------------------------
# Example graph
# ---------------------------

def goal_test(state):
    return state == 'Z'

def get_successors(state):
    graph = {
        'S': [('toA', 'A'), ('toB', 'B')],
        'A': [('toC', 'C'), ('toD', 'D')],
        'B': [('toD', 'D')],
        'C': [('toZ', 'Z')],
        'D': [('toZ', 'Z')],
        'Z': []
    }
    return graph.get(state, [])

def get_cost(state, action, next_state):
    costs = {
        ('S', 'toA', 'A'): 1,
        ('S', 'toB', 'B'): 4,
        ('A', 'toC', 'C'): 3,
        ('A', 'toD', 'D'): 1,
        ('B', 'toD', 'D'): 1,
        ('C', 'toZ', 'Z'): 2,
        ('D', 'toZ', 'Z'): 5
    }
    return costs[(state, action, next_state)]

# Example heuristic (straight-line estimates)
def heuristic(state):
    estimates = {
        'S': 5,
        'A': 4,
        'B': 2,
        'C': 2,
        'D': 1,
        'Z': 0
    }
    return estimates[state]

result = a_star_search('S', goal_test, get_successors, get_cost, heuristic)
print("A* Result:", result)
