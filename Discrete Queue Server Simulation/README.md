## Discrete Event Program Generalized to Cover a Queue-Server Simulation with Extensions
### User may input a Server Name, Server Capacity, Entity Name, Inter-Arrival Time between Entities, Service Times, and an Entity Attribute. The program shall also compute statistics of minimum / maximum queue length, total idle time for the resource, resource utilization percentage, total queue time, average waiting time in queue, and the waiting time variance.

This program should work regardless of the input that's inserted (unless negative or improper input). The .png of MyOwnTestCase is an image of a test case I ran of a Vons store, with 3 cashier's open. 8 customers come in with [0.2, 0.2, 0.2, 0.1, 2.0, 1.2, 0.4, 0.3] respective inter-arrival times, and with [3.0, 0.5, 1.5, 4.0, 0.2, 2.6, 3.7, 6.1] respective service times. I did this test case so we can visualize how stores are nowadays, especially with all this craze of the Corona Virus that's going to kill us all. The customer's arrive quickly one after the other always utilizing the resources.

It will continously prompt the user for input for the amount of customer's they choose. It might be a little less annoying if you choose a smaller number :). BUT should work with any length.

The entity attribute I chose was allowing the user to choose the customer's weight.They're not to be simulated but just related to the customer. I figured if the user wanted, they can correspond heavier people with purchasing more and having a longer service time. Not trying to be offensive in any way whatsoever, it's just what I thought of.
