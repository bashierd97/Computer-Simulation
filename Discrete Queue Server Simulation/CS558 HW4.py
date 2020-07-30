# Bashier Dahman
# CS 558 HW 4

import simpy
import statistics


###################################################################
################ PROMPTING THE USERS FOR INFO #####################

# asking for server name
server_name = input("Please enter a server name: ")

# creating my simpy environment
enviornment = simpy.Environment()


# asking for server capacity and throw an exception if 0 or less
server_capacity = int(input("\nNow please enter a server capacity (Must be greater than 0): "))
if server_capacity <= 0:
    raise ValueError("Please enter a number that is not negative or zero")

# setting the server capacity as a my resource capacity 
storeQueue = simpy.Resource(enviornment, capacity=server_capacity) 

# asking user for an entity name
entity_name = input("\nNow what would you like your entity to be named? ")

# prompting the user for the number of customers coming into the establishment and throwing an exception if 0 or less
num_of_customers = int(input("\nPlease enter the amount of entities coming in: ")) 
if num_of_customers <= 0:
    raise ValueError("You can't have negative entities dummy, please try again :).")

# creating an empty list to store my customers in there
customers = []

# looping through and adding them into my list
for i in range(1, num_of_customers+1):
    customers.append(i)


### asking user for a list of inter-arrival times & service times ###

# creating an empty list for inter_arrival times
inter_arrival = [] 
  
print("\nNow for each entity please enter they're respective Inter-arrival time: ")  
# iterating for the length of customers and telling the user for which customer they're adding the time for
for i in range(0, num_of_customers): 
    print(entity_name + " " + str(i) + " Inter-Arrival Time: ")
    i_a_time = float(input())
    if i_a_time < 0:
        raise ValueError("Please enter a number that is not negative")

    inter_arrival.append(i_a_time) # adding the element 
      
print("\nHere is your complete inter-arrival time list: ")
print(inter_arrival)

# asking the user for each customer's respective service time
print("\nNow once more, for each customer please enter they're respective service time: ")  

# creating an empty list for my service time
service = []

# iterating for the length of customers and telling the user for which customer they're adding the time for
for i in range(0, num_of_customers): 
    print(entity_name + " " + str(i) + " Service Time: " )
    service_time = float(input())
    if service_time <= 0:
        raise ValueError("Please enter a number that is not negative or zero")

    service.append(service_time) # adding the element 
      
print("\nHere is your complete service time list: ")
print(service)


print("\nPlease enter a value for each entity's weight")

entity_weight = []

# iterating for the length of customers and telling the user for which customer they're adding the time for
for i in range(0, num_of_customers): 
    print(entity_name + " " + str(i) + " Weight: " )
    weight = float(input())
    if service_time <= 0:
        raise ValueError("Please enter a number that is not negative or zero")

    entity_weight.append(weight)

print("\nHere is your complete entity weight list: \n")
print(entity_weight)



waiting_times = []
max_queue = 0
current_queue = 0
min_queue = 9999999
idle_time = 0
last_served = 0

def queueMethod(environment, entity_name, store, arrival_time, service_time):
    global max_queue
    global current_queue
    global min_queue
    global last_served
    global idle_time

    yield environment.timeout(arrival_time)


    print('%s arriving at %s' % (entity_name, round(environment.now,3)))
    with storeQueue.request() as request:
        yield request

        queue = len(storeQueue.queue)
        min_queue = min(min_queue, queue)
        max_queue = max(max_queue, queue)


        # calculates waiting times
        waiting_time = environment.now - arrival_time
        print('%s waiting time %s' % (entity_name, round(waiting_time,3)))


        # calculates when entity starts to be served and when it leaves

        print('%s starting to be served at %s' % (entity_name, round(environment.now,3)))
        yield environment.timeout(service_time)
        print('%s leaving at %s' % (entity_name, round(environment.now,3)))

        # calculating my idle time
        if abs(0 - waiting_time) <= 0.001 and storeQueue.count == 1:
            idle_time += arrival_time - last_served

        # using this variable to help calculate my idle time
        last_served = environment.now

        waiting_times.append(waiting_time)

        # # section for finding max queue length 
        # if (len(storeQueue.queue) != 0):
        #     for i in range(len(storeQueue.queue)):
        #         current_queue += 1
        #         if current_queue > max_queue:
        #             max_queue += 1
        #             current_queue = 0                    

        # elif (len(storeQueue.queue) == 0):
        #     current_queue = 0

        #######################################

        # # this calculates my minimum length for queue
        # new_min_queue = len(storeQueue.queue)

        # if new_min_queue < min_queue:
        #     min_queue = new_min_queue
        #############################################

        # far more simple methods of finding max and min queue lenghts...
        queue = len(storeQueue.queue)
        min_queue = min(min_queue,queue)
        max_queue = max(max_queue,queue)


arrival_time = 0

for i in range(num_of_customers):
    arrival_time += inter_arrival[i]
    service_time = service[i]
    enviornment.process(queueMethod(enviornment, '%s %d:' % (entity_name, i), storeQueue, arrival_time, service_time))


enviornment.run()

# this calculates the total time in my queue
total_waiting = sum(waiting_times)

print("\n===================STATISTICAL DATA===================")
print ("Average Waiting Time in %s: %3.1f minutes" % (server_name, statistics.mean(waiting_times)))
print ("Variance of Waiting Time in %s: %3.1f minutes" % (server_name, statistics.variance(waiting_times)))
print("Maximum Queue:", max_queue)
print("Minimum Queue:", min_queue)
print("Total Waiting Time in Queue: %3.1f minutes" % total_waiting)
print("Total Idle Time of %s: %3.1f minutes" % (server_name, idle_time))

# calculating resource utilization and rounding it up 2 decimal points
resource_utilization = (((enviornment.now - idle_time)/ enviornment.now) * 100)
print("Resource Utilization:", round(resource_utilization,2), "%")
print("======================================================")