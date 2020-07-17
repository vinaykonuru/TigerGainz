import pandas as pd
import fuzzymatcher as fm



#FUNCTIONS

def Df_creator(input1, input2, input3, input4, input5, input6): #Process information and stores strings as numbers
    day_lister = input2 #will ensure the days is always in a list datatype

    workout_lister = input4 #will ensure the workouts are in a list datatype

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
    d =str(day_lister)




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
    w =str(workout_lister)



    #This is the basic framework of user database (row)
    user_frame = pd.DataFrame({"Name" : [input1], "Day_Av": d, "Duration": input3, "Type_Workout": w, "Time_z": [input5], "No_Ppl": [input6]})
    '''
    user_frame["Day_Av"] = user_frame["Day_Av"].astype(object) #columns that will eventually stoe lists must have a different datatype --> "objects"
    user_frame['Type_Workout'] = user_frame["Type_Workout"].astype(object)
    user_frame.at[0, "Day_Av"] = day_lister #replacing placeholder values with sorted lists created above
    user_frame.at[0, "Type_Workout"] = workout_lister
    '''

    return user_frame #this is the object we get from the function



def getKeysByValue(dictOfElements, valueToFind): #function finds keys(names) from attributes (parameters)
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


def dict_creator(key, value): #makes dictionary from two lists containing the list of keys and list of values
    dictionary = {}
    for item in key:
        dictionary[item] = value[key.index(item)]
    return dictionary



#Test of function that creates user dataframe

input1 = "Charlie"
input2 = ["Tuesday", "Wednesday", "Friday"]
input3 = "hour"
input4 = ["Abs","Upper Body", "Lower Body"]
input5 = "Eastern"
input6 = 3          #all these inputs are temporary variables. Ideally, the GUI will stores these values as variables

Dfuser = Df_creator(input1, input2, input3, input4, input5, input6)

#To makesure that the rest of the code executes, I created a mock request dataframe

names = ["Charles", "Vincent", "Diana", "Ben", "Vinay", "Eugene", "Princeton_Dude", "Mike Hawk"]
days = [["Tuesday", "Monday", "Friday"], ["Friday", "Saturday", "Sunday"], ["Friday", "Saturday","Sunday"],
        ["Monday", 'Wednesday', "Friday"], ["Tuesday", "Wednesday", "Friday"], ["Monday", "Tuesday", "Wednesday", 'Thursday',"Friday"],
        ["Monday", "Thursday"], ["Sunday", "Friday", 'Monday']]
duration = ["hour", "hour", "hour", "hour and a half", "two hours", "5 hours", "hour", "half an hour"]
type1 = [["Cardio", "Abs", "Lower Body", "Upperbody"], ["Cardio"], ["Abs"], ["Abs", "Cardio"], ["Lower Body", "Upper Body"],
        ["Abs"], ["Abs", "Upper Body", "Lower Body", "Cardio"], ["Upper Body"]]
time = ["Eastern", "Western", "Mountain", "Western", "Eastern", "Western", "Eastern", "Central"]
no_ppl = [2, 2, 2, 3, 4, 2, 3, 4]

columns = ["Name", "Day_Av", "Duration", "Type_Workout", "Time_z", "No_Ppl"]

Dfrq = pd.DataFrame(columns=columns) #this is the dataframe of people still waiting for a match.

for i in range(0, len(names)):
    output = Df_creator(names[i], days[i], duration[i], type1[i], time[i], no_ppl[i])
    Dfrq = Dfrq.append(output, ignore_index=True)

Dfrq.to_csv("mock_dataframe")


# Script that takes inputs as variables and appends value to dataframe.


length_checker = list(Dfrq["Name"])

if len(length_checker) < 1: #if there is no one in the Dfrq, then we add the Dfuser into Dfrq
    Dfrq = Dfrq.append(Dfuser, ignore_index=True)

else:

    #we are going to make a dictionary where the key is the name of user and the value is the other info

    user_dict = Dfuser.to_dict()

    #Same thing but for the request dataframe

    request_dict = Dfrq.to_dict()

    #Our dataframes, when using the matching algorithm, should not use the names as a parameter for matching.
    #We can store these names in a temp file: lists.

    user_name = Dfuser.pop("Name")
    Dfrq_names = Dfrq.pop("Name")


    #Line of code that actually matches the user with the people still in request dataframe. Outputs a new dataframe of matched people

    left_on = right_on = ["Day_Av", "Duration", "Type_Workout", "Time_z", "No_Ppl"]

    matched_results = fm.fuzzy_left_join(Dfuser, Dfrq, left_on, right_on, left_id_col="Day_Av", right_id_col="Day_Av")

    pd.set_option("display.max_rows", None, "display.max_columns", None) #line of code that allows me to see the full dataframe

    #dropping irrelevant columns and displaying relevant info of the matched person

    matched_results = matched_results.drop(columns=["__id_left", "__id_right", "Day_Av_left", "Duration_left",
                                                 'Type_Workout_left', "Time_z_left", "No_Ppl_left"])
    list_col = matched_results.columns.tolist()
    list_col = list_col[1:]

    name_dict = dict_creator(list_col, left_on)
    matched_results = matched_results.rename(columns=name_dict)

    















#print(Dfuser)
#print(Dfrq)








