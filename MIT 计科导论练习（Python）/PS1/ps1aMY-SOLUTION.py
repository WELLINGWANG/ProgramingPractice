###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:Welling Wang
# Collaborators:Boe Wang
# Time:6hours

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cows={}
    f=open(filename)
    line=f.readline()
    while line != "":
        split=line.split(",")
        cows[split[0]]=int(split[1])
        line=f.readline()
        f.close
    return cows

if __name__=="__main__":
    cows=load_cows("ps1_cow_data.txt")

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    trip,monitor=[],[]
    sort=sorted(cows.items(), key=lambda items:items[1], reverse=True)
    while len(monitor) < len(sort):
        subtrip=[]
        for cow in sort:
            if cow[0] not in monitor and cow[1] < limit:
                limit-=cow[1] 
                subtrip.append(cow[0])
                monitor.append(cow[0])         
            else:
                continue
        trip.append(subtrip)
        limit=10
    return trip

limit=10
##if __name__=="__main__":
##    trips=(greedy_cow_transport(cows,limit))
##    print(trips)


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    tripnum=len(cows)
    for trips in get_partitions(cows):
        cargons=[]
        for subtrip in trips:
            cargon=[]
            for cow in subtrip:
                cargon.append(cows[cow])
            cargons.append(sum(cargon))
        if max(cargons)<=limit and len(trips)<tripnum:
            tripnum=len(trips)
            tmp=trips
        else:
            continue
    return tmp,tripnum

limit=10
##if __name__=="__main__":
##    trips,num=brute_force_cow_transport(cows,limit)
##    print(trips,num)
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start=time.time()
    tripA=(greedy_cow_transport(cows,limit))
    print(tripA,len(tripA))
    end=time.time()
    print("Greedy takes:",end-start,"seconds")
    start=time.time()
    trips,num=brute_force_cow_transport(cows,limit)
    print(trips,num)
    end=time.time()
    print("Brute force takes:",end-start,"seconds")
 
compare_cow_transport_algorithms()
