import pandas as pd



#Functions

def Df_creator(input1, input2, input3, input4, input5, input6): #This is the function that creates the user dataframe. It stores some long string values as integers.
    day_lister = input2 #renamed varibable just so its easer to keep track of

    workout_lister = input4 #renamed variable just so its easier to keep track of


    for i in range(0,len(day_lister)): #this loop basically turns the days of the week into a numerical value
                                     #Output should be a list of numbers that correspond with the day of the week
        if day_lister[i] == "Monday":
            day_lister[i] = 1
        elif day_lister[i] == "Tuesday":
            day_lister[i] = 2
        elif day_lister[i] == "Wednesday":
            day_lister[i] = 3
        elif day_lister[i] == "Thursday":
            day_lister[i] = 4
        elif day_lister[i] == "Friday":
            day_lister[i] = 5
        elif day_lister[i] == "Saturday":
            day_lister[i] = 6
        else:
            day_lister[i] = 7
    day_lister.sort() #Ensures that list will be in order


    for j in range(0, len(workout_lister)): #Same logic as above

        if workout_lister[j] == "Abs":
            workout_lister[j] = 1
        elif workout_lister[j] == "Upper Body":
            workout_lister[j] = 2
        elif workout_lister[j] == "Cardio":
            workout_lister[j] = 3
        else:
            workout_lister[j] = 4
    workout_lister.sort() #Ensures that list will be in order


    #This is the basic framework of user database (row)
    user_frame = pd.DataFrame({"Name" : [input1], "Day_Av": 0, "Duration": input3, "Type_Workout": 0, "Time_z": [input5], "No_Ppl": [input6]})

    user_frame["Day_Av"] = user_frame["Day_Av"].astype(object) #columns that will eventually stoe lists must have a different datatype --> "objects"
    user_frame['Type_Workout'] = user_frame["Type_Workout"].astype(object)
    user_frame.at[0, "Day_Av"] = day_lister #replacing placeholder values with sorted lists created above
    user_frame.at[0, "Type_Workout"] = workout_lister

    return user_frame

   #this is the object we get from the function

#Test of function that creates user dataframe

input1 = "Charlie"
input2 = ["Tuesday", "Wednesday", "Friday"]
input3 = "hour"
input4 = ["Abs","Upper Body", "Lower Body"]
input5 = "Eastern"
input6 = 3          #all these inputs are temporary variables. Ideally, the GUI will stores these values as variables

Dfuser = Df_creator(input1, input2, input3, input4, input5, input6)


# Code that would ideally execute the matching algorithm or, if their is no one in the Dfrq, append the user into Dfrq

columns = ["Name", "Day_Av", "Duration", "Type_Workout", "Time_z", "No_Ppl"]

Dfrq = pd.DataFrame(columns=columns) #this is the dataframe of people still waiting for a match

length_checker = list(Dfrq["Name"])

if len(length_checker) < 1: #if there is no one in the Dfrq, then we add the Dfuser into Dfrq
    Dfrq = Dfrq.append(Dfuser, ignore_index=True)
else:
    print("placeholder")
    #run matching script
        #if matching probability is below a certain threshold, we can append the Dfuser into the main dataframe.


print(Dfuser)
print(Dfrq)









