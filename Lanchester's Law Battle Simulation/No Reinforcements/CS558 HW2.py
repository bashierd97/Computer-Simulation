# CS558 Bashier Dahman HW2 #


import matplotlib.pyplot as plt 

# Telling the user the program is beginning #
print("\n======CONTINOUS BATTLE SIMULATION BASED ON LANCHESTER'S LAW======\n")

##########################################
# PROMPTING THE USERS FOR ALL THE VALUES #
##########################################


# prompting the user for input
# asking the user for the amount of troops 'x' side will have
x_troops = (int(input("How many troops would you like the 'X' side to have? \n")))

# if the input is negative throw exception
if x_troops < 0:
    raise ValueError("Please enter a number that is not negative")

# asking the user for the alpha coefficient for the x troops
print("\nWhat would you like the lethality coefficient (alpha) to be for the X troops? ")
alpha = (float(input("Please enter a decimal number between 0 and 1: \n")))

# if it's not in the correct bounds throw exception
if (alpha > 1 or alpha < 0):
    raise ValueError("Please enter a number between the corrected bounds")

# prompting the user for the amount of troops 'y' side will have
y_troops = (int(input("\nHow many troops would you like the 'Y' side to have? \n")))

# if the input is negative throw exception
if y_troops < 0:
    raise ValueError("Please enter a number that is not negative")

# prompting the user for the beta coefficient for the y troops
print("\nWhat would you like the lethality coefficient (beta) to be for the Y troops? ")
beta = (float(input("Please enter a decimal number between 0 and 1: \n")))

# if it's not in the correct bounds throw exception
if (beta > 1 or beta < 0):
    raise ValueError("Please enter a number between the corrected bounds")


# Displaying what the user has inputted so far so they
# can check if everything looks good
print("============INITIAL SETUP FOR BATTLE===============")
print('Initial X Troops: ' + str(x_troops))
print('Initial Y Troops: ' + str(y_troops))
print("Lethality Coefficient for 'X' Troops: " + str(alpha))
print("Lethality Coefficient for 'Y' Troops: " + str(beta))
print("===================================================\n")

# initializing the original time to zero
time = 0
# now I prompt the user for the amount of time they would like
# this battle to occur for
userTime = (int(input("Please input a time frame you would like these troops to battle for (in days): \n")))

# verifying the user's inputted time is not equal to zero or negative
if userTime <= 0:
    raise ValueError("Invalid time frame, please run program once again and enter only "
                     "positive numbers (not including 0)")

# now I ask the user what they would like their timestep (dx/dt) to be in days
timeStep = (float(input("Now please enter a time step (time interval) that you would like "
                        "to increment by (in days): \n")))

#making sure their time step is correct so they don't go back in time
if timeStep <= 0:
    raise ValueError("Not a valid time step, please retry with only positive numbers!")

# Creating lists so I can graph my values and keep track of my X troops, Y troops, and Time
x_list = []
y_list = []
timeList = []

print( "  TIME-X TROOPS-Y TROOPS ")
# Using Euler's Method of integration to calculate the remaining troops from each side
while time < userTime:
    time = time + timeStep
    # my differential equation's given by off the lethality of firing
    x = -(beta * y_troops)
    y = -(alpha * x_troops)
    # as long as the troops aren't dead continue on with the firing
    if (x_troops > 0 and y_troops > 0):
        x_troops = x_troops + (x*timeStep)
        y_troops = y_troops + (y*timeStep)

    #inserting my values into the list's so I can plot them
    x_list.append(x_troops)
    y_list.append(y_troops)
    timeList.append(time)

    # if either side dies first notify the user that they're continously
    # killing dead bodies at this point
    if (x_troops <= 0):
        print ("X troops eliminated")
        x_troops = x_troops*-1

    if (y_troops <= 0):
        print("Y troops eliminated")
        y_troops = y_troops*-1

    # printing the values of time and troops in case the user doesn't want to
    # look at the graph    
    print ("%6.2f %6.0f %6.0f" % (time, x_troops, y_troops))


# Plotting my values
plt.plot(timeList, x_list, label = 'X troops')
plt.plot(timeList, y_list, label = 'Y Troops')

# labeling my x-axis and y-axis
plt.xlabel('Time')
plt.ylabel('Number of Survivors')

# titling my graph
plt.title("Lanchester's Law")

# This allows me to plot a grid on my graph
plt.grid(True)
# showing a legend and the graph
plt.legend()
plt.show()


