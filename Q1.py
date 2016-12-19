import numpy as np
from operator import add
import itertools

np.set_printoptions(linewidth=200)
np.random.seed(42)

hickers = 9

costs = np.around(np.random.rand(hickers*2, hickers*2), decimals = 2)
np.fill_diagonal(costs, 0)
costs = np.maximum( costs, costs.transpose() )
home_costs = np.around(np.random.rand(hickers,1), decimals = 2)
work_costs = np.around(np.random.rand(1,hickers), decimals = 2)

#last column - distance to drivers home
#last row - distance to drivers office
total_costs = np.zeros((hickers*2 + 1, hickers*2 + 1))
total_costs[:-1,:-1] = costs
total_col = np.zeros((hickers*2 + 1, 1))
total_col[:hickers,:] = home_costs
total_row = np.zeros((1, hickers*2 + 1))
total_row[:,hickers:-1] = work_costs
total_costs[:,-1] = total_col.reshape((hickers*2+1))
total_costs[-1,:] = total_row

car_capacity = 3

def print_location(loc):
    if loc < hickers:
        print('home of the %d passenger'%(int(loc + 1)))
    elif loc<hickers*2:
        print('office of %d passenger'%(int(loc-hickers + 1)))
    else:
        print('end/start node')

t = 0

# moving backwards
def find_route(location, seats, passengers, graph_out=False):
    
    # if it's start
    if not any(seats):
        # go to start
        #print('reached the end')
        return 0
    # nodes for next iteration    
    origin = []
    #if it's a home
    if location < hickers:
        # same passengers - not dropping off anyone
        new_pass = list(passengers)
        # remove the one whose home we are in
        new_seats = list(seats)
        new_seats[location] = 0
        # add homes for new_seats * passengers
        origin += [x for x in range(hickers) if new_seats[x]*passengers[x]]
        # add offices for old_seats * (not passengers)
        origin += [x+hickers for x in range(hickers) if seats[x]*(not passengers[x])]
        # if seats = [0...0] i.e. we are going to start (13 index in cost matrix)
        if not origin:
            origin = [hickers*2]
    #if it's an office    
    elif location < hickers*2:
        # same seats - not picking up anyone
        new_seats = list(seats)
        # gets passenger
        new_pass = list(passengers)
        new_pass[location - hickers] = 1
        # add homes for new_seats * passengers
        origin += [x for x in range(hickers) if seats[x]*new_pass[x]]
        # add offices for seats * (not passengers)
        origin += [x+hickers for x in range(hickers) if seats[x]*(not new_pass[x])]
    # if it's drivers office
    elif location is hickers*2:
        new_seats = list(seats)
        new_pass = list(passengers)
        # could only come from office of one of the seats
        origin = [x+hickers for x in range(hickers) if new_seats[x]]
        
    # list of distances to previous node: total_costs[current node, next_node]
    d_list = [total_costs[location, node] for node in origin]

    # list of next calls of functions from every possible previous node
    F_list = [find_route(node, new_seats, new_pass, graph_out) for node in origin]
    
    # min of [distance(office, next node) + F(next node)] in all next states
    min_cost_list = map(add,d_list, F_list)
    min_cost_list = np.array(list(min_cost_list))

    # the one with minimun cost - [from,to]
    min_ind = min_cost_list.argmin()
    
    if(graph_out):
        print('|')
        print('V')
        print('min_ind = ', end='')
        print(origin[min_ind])

    return min_cost_list[min_ind]


dummy = np.zeros((hickers))
dummy[:car_capacity] = np.ones((car_capacity))

all_states = list(itertools.permutations(list(dummy)))
unique = []
for c in all_states:
    if c not in unique:
        unique.append(c)

best_routes = []
for s in unique:
    #print(s)
    best_routes.append(find_route(hickers*2,s,[0]*hickers))

print('Passengers:')
for i, s in enumerate(unique[np.array(best_routes).argmin()]):
    if s:
        print(i)