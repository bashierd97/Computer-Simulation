# CS558 Bashier Dahman HW6 Part 2 #

import simpy
import statistics
import random
import matplotlib.pyplot as plt 
import numpy as np

###################################################################
### THIS IS A REMODEL OF MY HW 4 SOME OF THE COMMENTS MAY STILL ###
###### BE THE SAME, BUT REGARDLESS DOES WHAT ITS INTENDED FOR #####
### ALSO TIP, IF THE MODEL PRODUCES AN ERROR CLAIMING THE MEAN  ###
### REQUIRES A DATA POINT, THEN JUST RE-RUN IT. I NOTICED THIS  ###
### OCCURS WHEN YOU FORCE CLOSE THE TERMINAL SO JUST RE-RUN AND ###
################# YOU SHOULD BE GOOD TO GO :) #####################
###################################################################


###################################################################
################ PROMPTING THE USERS FOR INFO #####################

print("===================== AMAZON RANDOM TRUCK MODEL ===================== \n")


total_cost_list = []

avg_waiting_times = []
avg_resc_util = []

server_capacity = 1

while (server_capacity != 3):

    # inputting my own server capacity as 1 for now and increments by 1 to display both plots for one then two facilities

    for test in range (10000):
        # my server name
        server_name = "Amazon Repair Facility"

        # creating my simpy environment
        enviornment = simpy.Environment()

        if server_capacity <= 0:
            raise ValueError("Please enter a number that is not negative or zero")

        # setting the server capacity as a my resource capacity 
        storeQueue = simpy.Resource(enviornment, capacity=server_capacity) 

        # asking user for an entity name
        entity_name = "Truck"

        # setting the number of customers to 20
        num_of_customers = 20
        if num_of_customers <= 0:
            raise ValueError("You can't have negative entities dummy, please try again :).")

        # creating an empty list to store my customers in there
        customers = []

        # looping through and adding them into my list
        for i in range(1, num_of_customers+1):
            customers.append(i)

        # creating an empty list for inter_arrival and service times
        inter_arrival = [] 
        service = []

        # setting the probability of service to 50 percent
        probability_of_service = .50
        last_arrival = 0

        # initializing and setting values to my facility / downtime costs
        facility_cost = 2500
        downtime_cost = 5000

        for x in range(num_of_customers):
            # this creates a uniformed distribution with a 50% chance of a service occuring
            if random.uniform(0, 1) <= probability_of_service:
                inter_arrival.append(x - last_arrival)
                last_arrival = x
                # each trucks that does require service will have a service time halved of a random dice rolled
                service.append(random.uniform(0.5, 3))
        

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


            # print('%s arriving at %s' % (entity_name, round(environment.now,3)))
            with storeQueue.request() as request:
                yield request

                queue = len(storeQueue.queue)
                min_queue = min(min_queue, queue)
                max_queue = max(max_queue, queue)


                # calculates waiting times
                waiting_time = environment.now - arrival_time
                # print('%s waiting time %s' % (entity_name, round(waiting_time,3)))


                # calculates when entity starts to be served and when it leaves

                # print('%s starting to be served at %s' % (entity_name, round(environment.now,3)))
                yield environment.timeout(service_time)
                # print('%s leaving at %s' % (entity_name, round(environment.now,3)))

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

        for h in range(len(inter_arrival)):
            arrival_time += inter_arrival[h]
            service_time = service[h]
            enviornment.process(queueMethod(enviornment, '%s %d:' % (entity_name, h), storeQueue, arrival_time, service_time))


        enviornment.run()


        total_cost = round(enviornment.now * (facility_cost * server_capacity) + downtime_cost * sum(waiting_times + service), 2)
        total_cost_list.append(total_cost)
        avg_waiting_times.append(round(statistics.mean(waiting_times), 2))

        # equation for resource utilization
        resource_utilization = round((enviornment.now - idle_time) / enviornment.now, 2)
        # because resource utilization cannot exceed more than 100 percent
        if resource_utilization > 1.00:
            resource_utilization = 1.00
        avg_resc_util.append(resource_utilization)

        # this calculates the total time in my queue
        total_waiting = sum(waiting_times)

        # print("\n===================STATISTICAL DATA===================")
        # print ("Average Waiting Time in %s: %3.1f minutes" % (server_name, statistics.mean(waiting_times)))
        # print ("Variance of Waiting Time in %s: %3.1f minutes" % (server_name, statistics.variance(waiting_times)))
        # print("Maximum Queue:", max_queue)
        # print("Minimum Queue:", min_queue)
        # print("Total Waiting Time in Queue: %3.1f minutes" % total_waiting)
        # print("Total Idle Time of %s: %3.1f minutes" % (server_name, idle_time))

        # # calculating resource utilization and rounding it up 2 decimal points
        # resource_utilization = (((enviornment.now - idle_time)/ enviornment.now) * 100)
        # print("Resource Utilization:", round(resource_utilization,2), "%")
        # print("======================================================")

    # creating numpy arrays of my lists
    total_cost_graph = np.array(total_cost_list)

    avg_waiting_times_graph = np.array(avg_waiting_times)

    avg_resc_util_graph = np.array(avg_resc_util)

    color1 = "blue"
    color2 = "red"
    color3 = "mediumpurple"

    ######## GRAPHS FOR TOTAL COSTS PDF / CDF ########
    print("Mean of Total Cost = {:.4f}".format(np.mean(total_cost_graph)))
    print("Standard Deviation of Total Cost = {:.4f}\n".format(np.std(total_cost_graph)))
    plt.title("Total Cost of " + str(server_capacity) + " Truck Repair Facility PDF")
    plt.xlabel("Amount in Dollars")
    plt.ylabel("Frequency")
    num_bins = 8
    plt.hist (total_cost_graph, num_bins, rwidth=.95, color = color1)
    plt.show()

    plt.cla() #clear axes
    plt.title("Total Cost of " + str(server_capacity) + " Truck Repair Facility CDF")
    plt.xlabel("Amount in Dollars")
    plt.ylabel("Cumulative Probability")
    num_bins = 8
    counts, bin_edges = np.histogram (total_cost_graph, bins=num_bins)
    cdf = np.cumsum (counts)
    #plt.xticks(np.arange(30, 68, step=2))
    plt.plot (bin_edges[1:], cdf/cdf[-1])
    plt.show()
    ######################################################

    ######## GRAPHS FOR AVERAGE WAITING TIMES PDF / CDF ########
    print("Mean of Waiting Times for Truck Repair = {:.4f}".format(np.mean(avg_waiting_times_graph)))
    print("Standard Deviation of Waiting Times for Truck Repair = {:.4f}\n".format(np.std(avg_waiting_times_graph)))
    plt.title("Waiting Times for " + str(server_capacity) +" Truck Repair Facility PDF")
    plt.xlabel("Time in Days")
    plt.ylabel("Frequency")
    num_bins = 8
    plt.hist (avg_waiting_times_graph, num_bins, rwidth=.95, color = color2)
    plt.show()

    plt.cla() #clear axes
    plt.title("Waiting Times for " + str(server_capacity) +" Truck Repair Facility CDF")
    plt.xlabel("Time in Days")
    plt.ylabel("Cumulative Probability")
    num_bins = 8
    counts, bin_edges = np.histogram (avg_waiting_times_graph, bins=num_bins)
    cdf = np.cumsum (counts)
    #plt.xticks(np.arange(30, 68, step=2))
    plt.plot (bin_edges[1:], cdf/cdf[-1])
    plt.show()
    ######################################################


    ######## GRAPHS FOR AVERAGE RESOURCE UTILIZATION PDF / CDF ########
    print("Mean of Resource Utilization for " + str(server_capacity) + " Truck Repair Facility = {:.3f}".format(np.mean(avg_resc_util_graph)))
    print("Standard Deviation of Resource Utilization for " + str(server_capacity) + " Truck Repair Facility = {:.3f}\n".format(np.std(avg_resc_util_graph)))
    plt.title("Resource Utilization for " + str(server_capacity) +" Truck Repair Facility PDF")
    plt.xlabel("Amount in %")
    plt.ylabel("Frequency")
    num_bins = 8
    plt.hist (avg_resc_util_graph, num_bins, rwidth=.95, color = color3)
    plt.show()

    plt.cla() #clear axes
    plt.title("Resource Utilization for " + str(server_capacity) + " Truck Repair Facility CDF")
    plt.xlabel("Amount in %")
    plt.ylabel("Cumulative Probability")
    num_bins = 8
    counts, bin_edges = np.histogram (avg_resc_util_graph, bins=num_bins)
    cdf = np.cumsum (counts)
    #plt.xticks(np.arange(30, 68, step=2))
    plt.plot (bin_edges[1:], cdf/cdf[-1])
    plt.show()
    ######################################################

    if server_capacity != 2:
        print("======== NOW PROCESSING A MODEL FOR TWO FACILITIES ========\n")
        # clearing my data so I can graph / plot everything again
        total_cost_list.clear()
        avg_waiting_times.clear()
        avg_resc_util.clear()

    server_capacity += 1


 
