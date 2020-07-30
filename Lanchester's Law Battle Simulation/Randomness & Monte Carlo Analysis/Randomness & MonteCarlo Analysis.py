# CS558 Bashier Dahman HW6 Part 1 #

import random
import matplotlib.pyplot as plt 
import numpy as np

# Telling the user the program is beginning #
print("\n======CONTINOUS BATTLE SIMULATION BASED ON LANCHESTER'S LAW======")

print("=========Factoring in Randomness / Monte Carlo Analysis=========\n")

##########################################
# RUNNING THE SIMULATION 10,000 TIMES #
##########################################

overall_time = []
num_of_troops_end = []

for i in range(10000):
    # prompting the user for input
    # asking the user for the amount of troops 'x' side will have
    x_troops = 1000

    # if the input is negative throw exception
    if x_troops < 0:
        raise ValueError("Please enter a number that is not negative")

    # creating a random uniform distribution of the alpha variable between 0.75 - 0.85
    alpha = random.uniform(0.75,0.85)

    # if it's not in the correct bounds throw exception
    if (alpha > 1 or alpha < 0):
        raise ValueError("Please enter a number between the corrected bounds")

    # prompting the user for the amount of troops 'y' side will have
    y_troops = 800

    # if the input is negative throw exception
    if y_troops < 0:
        raise ValueError("Please enter a number that is not negative")

    # creating a random uniform distribution of the beta variable between 0.85 - 0.95
    beta = random.uniform(0.85,0.95)

    # if it's not in the correct bounds throw exception
    if (beta > 1 or beta < 0):
        raise ValueError("Please enter a number between the corrected bounds")


    ########################################################################
    ######################### HOMEWORK 3 PART ##############################

    # NOW PROMPTING THE USER FOR REINFORCEMENT EVENTS FOR X SIDE#
    numOfEvents_X = int(random.uniform(1,3))

    # user must input a value between 0 and 3 
    if (numOfEvents_X < 0 or numOfEvents_X > 3) :
        raise ValueError("Please enter a number that is between 0 and 3")

    # PROMPTING THE USER FOR REINFORCEMENT EVENTS FOR Y SIDE #
    numOfEvents_Y = int(random.uniform(1,3))

    # user must input a value between 0 and 3 
    if (numOfEvents_Y < 0 or numOfEvents_Y > 3) :
        raise ValueError("Please enter a number that is between 0 and 3")

    # PROMPTING THE USER FOR THE PERCENT LEVEL THE REINFORCEMENTS ARRIVE FOR X TROOPS #

    percentLevel_X = random.uniform(0.10,0.80)

    # if it's not in the correct bounds throw exception
    if (percentLevel_X > 0.80 or percentLevel_X < 0.10):
        raise ValueError("Please enter a number between the corrected bounds")

    # PROMPTING THE USER FOR THE PERCENT LEVEL THE REINFORCEMENTS ARRIVE FOR Y TROOPS #

    percentLevel_Y = random.uniform(0.10,0.80)

    # if it's not in the correct bounds throw exception
    if (percentLevel_Y > 0.80 or percentLevel_Y < 0.10):
        raise ValueError("Please enter a number between the corrected bounds")

    # PROMPTING THE USER FOR THE SIZE OF 'X' REINFORCEMENTS #

    sizeOfReinforcements_X = random.uniform(0.10,0.50)

    # if it's not in the correct bounds throw exception
    if (sizeOfReinforcements_X > 0.50 or sizeOfReinforcements_X < 0.10):
        raise ValueError("Please enter a number between the corrected bounds")

    # PROMPTING THE USER FOR THE SIZE OF 'Y' REINFORCEMENTS #

    sizeOfReinforcements_Y = random.uniform(0.10,0.50)

    # if it's not in the correct bounds throw exception
    if (sizeOfReinforcements_Y > 0.50 or sizeOfReinforcements_Y < 0.10):
        raise ValueError("Please enter a number between the corrected bounds")

    # Prompting the user for the alpha coefficient for the 'X' troops reinforcements #

    alpha_reinforcements = random.uniform(0.75,0.85)

    # if it's not in the correct bounds throw exception
    if (alpha_reinforcements > 1 or alpha_reinforcements < 0):
        raise ValueError("Please enter a number between the corrected bounds")

    # prompting the user for the beta coefficient for the 'Y' troop reinforcements #

    beta_reinforcements = random.uniform(0.85,0.95)

    # if it's not in the correct bounds throw exception
    if (beta_reinforcements > 1 or beta_reinforcements < 0):
        raise ValueError("Please enter a number between the corrected bounds")


    ##############################################################################
    ##############################################################################



    # initializing the original time to zero
    time = 0

    # this is the maximum time the battle can occur, no battle should get this far realisticly 
    userTime = 20

    # verifying the user's inputted time is not equal to zero or negative
    if userTime <= 0:
        raise ValueError("Invalid time frame, please run program once again and enter only "
                        "positive numbers (not including 0)")

    # now I ask the user what they would like their timestep (dx/dt) to be in days
    timeStep = .01

    #making sure their time step is correct so they don't go back in time
    if timeStep <= 0:
        raise ValueError("Not a valid time step, please retry with only positive numbers!")

    # Creating lists so I can graph my values and keep track of my X troops, Y troops, and Time
    x_list = []
    y_list = []
    timeList = []


    x_amount_reinforcements = x_troops * sizeOfReinforcements_X
    # calculating at what rate will I add reinforcements
    x_reinforcements_time = x_troops * percentLevel_X
    # calculating at what rate will I add reinforcements
    y_reinforcements_time = y_troops * percentLevel_Y
    y_amount_reinforcements = y_troops * sizeOfReinforcements_Y


    # print( "  TIME-X TROOPS-Y TROOPS ")
    # Using Euler's Method of integration to calculate the remaining troops from each side
    while time < userTime:
        time = time + timeStep
        # my differential equation's given by off the lethality of firing
        x = -(beta * y_troops)
        y = -(alpha * x_troops)
        x_Reinforce_lethal = -(beta_reinforcements * y_troops)
        y_Reinforce_lethal = -(alpha_reinforcements * y_troops)

        # as long as the troops aren't dead continue on with the firing
        if (x_troops > 0 and y_troops > 0):
            x_troops = x_troops + (x*timeStep)
            y_troops = y_troops + (y*timeStep)

        # inserting my values into the list's so I can plot them

        # this will factor in the reinforcemenets and add them to my list 
        # if number of reinforcement events !=0 , add reinforcements 
            if numOfEvents_X != 0:

                if (x_troops <= x_reinforcements_time):
                    # as soon as I hit less than that rate, add some reinforcements 
                    x_amount_reinforcements = x_amount_reinforcements + (x_Reinforce_lethal * timeStep)
                    x_troops += x_amount_reinforcements
                    # calculating at what rate will I add reinforcements
                    x_reinforcements_time = x_troops * percentLevel_X

                    #decrement # of 'X' reinforcement events, as I processed it already 
                    numOfEvents_X -= 1

        # this will factor in the reinforcemenets and add them to my list 
        # if number of reinforcement events !=0 , add reinforcements 
            if numOfEvents_Y != 0:

                if (y_troops <= y_reinforcements_time):
                    # as soon as I hit less than that rate, add some reinforcements 
                    y_amount_reinforcements = y_amount_reinforcements + (y_Reinforce_lethal * timeStep)
                    y_troops += y_amount_reinforcements
                    y_reinforcements_time = y_troops * percentLevel_Y

                    #decrement # of 'X' reinforcement events, as I processed it already 
                    numOfEvents_Y -= 1
            

        x_list.append(x_troops)
        y_list.append(y_troops)
        timeList.append(time)

        # if either side dies first notify the user that they're continously
        # killing dead bodies at this point
        if (x_troops <= 0):
            overall_time.append(time)
            num_of_troops_end.append(y_troops)
            break
        #     print ("X troops eliminated")
        #     x_troops = x_troops*-1

        if (y_troops <= 0):
            overall_time.append(time)
            num_of_troops_end.append(x_troops)
            break
        #     print("Y troops eliminated")
        #     y_troops = y_troops*-1

        # printing the values of time and troops in case the user doesn't want to
        # look at the graph    
        # print ("%6.2f %6.0f %6.0f" % (time, x_troops, y_troops))


    # # Plotting my values
    # plt.plot(timeList, x_list, label = 'X troops')
    # plt.plot(timeList, y_list, label = 'Y Troops')

    # # labeling my x-axis and y-axis
    # plt.xlabel('Time')
    # plt.ylabel('Number of Survivors')

    # # titling my graph
    # plt.title("Lanchester's Law")

    # # This allows me to plot a grid on my graph
    # plt.grid(True)
    # # showing a legend and the graph
    # plt.legend()
    # # plt.show()


time_graph = np.array(overall_time)

final_troops = np.array(num_of_troops_end)

color1 = "blue"
color2 = "red"

######## GRAPHS FOR BATTLE DURATION PDF / CDF ########
print("Mean of Battle Duration = {:.4f}".format(np.mean(time_graph)))
print("Standard Deviation of Battle Duration = {:.4f}\n".format(np.std(time_graph)))
plt.title("Battle Durations PDF")
plt.xlabel("Battle Time (Days)")
plt.ylabel("Frequency")
num_bins = 7
plt.hist (time_graph, num_bins, rwidth=.95, color = color1)
plt.show()

plt.cla() #clear axes
plt.title("Battle Durations CDF")
plt.xlabel("Battle Time (Days)")
plt.ylabel("Cumulative Probability")
num_bins = 7
counts, bin_edges = np.histogram (time_graph, bins=num_bins)
cdf = np.cumsum (counts)
# plt.xticks(np.arange(30, 68, step=2))
plt.plot (bin_edges[1:], cdf/cdf[-1])
plt.show()
######################################################

######## GRAPHS FOR NUM OF TROOPS PDF / CDF ########
print("Mean of Number of Troops Remaining = {:.4f}".format(np.mean(final_troops)))
print("Standard Deviation of Number of Troops Remaining = {:.4f}".format(np.std(final_troops)))
plt.title("Number of Troops Remaining PDF")
plt.xlabel("Amount of Troops")
plt.ylabel("Frequency")
num_bins = 7
plt.hist (final_troops, num_bins, rwidth=.95, color = color2)
plt.show()

plt.cla() #clear axes
plt.title("Number of Troops Remaining CDF")
plt.xlabel("Amount of Troops")
plt.ylabel("Cumulative Probability")
num_bins = 7
counts, bin_edges = np.histogram (final_troops, bins=num_bins)
cdf = np.cumsum (counts)
# plt.xticks(np.arange(30, 68, step=2))
plt.plot (bin_edges[1:], cdf/cdf[-1])
plt.show()
######################################################

