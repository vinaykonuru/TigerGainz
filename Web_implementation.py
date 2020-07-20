from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest
import pandas
import pandas as pd
import fuzzymatcher as fm
import csv

#FUNCTIONS

def Df_creator(inputNetID, input1, input2, input3, input4, input5, input6):  # Process information and stores strings as numbers
    day_lister = input2  # will ensure the days is always in a list datatype

    workout_lister = input4  # will ensure the workouts are in a list datatype

    for i in range(0, len(day_lister)):  # this loop basically turns the days of the week into a numerical value
        # Output should be a list of numbers that correspond with the day of the week
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
    day_lister.sort()  # Ensures that list will be in order
    d = str(day_lister)

    for j in range(0, len(workout_lister)):  # Same logic as above

        if workout_lister[j] == "Abs":
            workout_lister[j] = 1
        elif workout_lister[j] == "Upper Body":
            workout_lister[j] = 2
        elif workout_lister[j] == "Cardio":
            workout_lister[j] = 3
        else:
            workout_lister[j] = 4
    workout_lister.sort()  # Ensures that list will be in order
    w = str(workout_lister)

    # This is the basic framework of user database (row)
    user_frame = pd.DataFrame(
        {"NetID": inputNetID, "Name": [input1], "Day_Av": d, "Duration": [input3], "Type_Workout": w, "Time_z": [input5],
         "No_Ppl": [input6]})

    return user_frame  # this is the object we get from the function


def getKeysByValue(dictOfElements, valueToFind):  # function finds keys(names) from attributes (parameters)
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


def dict_creator(key, value):  # makes dictionary from two lists containing the list of keys and list of values
    dictionary = {}
    for item in key:
        dictionary[item] = value[key.index(item)]
    return dictionary

def home(request):
    return render(request,'home.html')

@login_required(login_url='/accounts/signup')
def find(request):
    return render(request,'find.html')

@login_required(login_url='/accounts/signup')
def waiting(request):
    if request.method=='POST':
        #get data about USER
        userdatadf=pandas.read_csv('WorkoutBuddy\studentdata.csv',index_col=('netID'))
        netID=request.user.username
        userdata=userdatadf.loc[netID]
        name=userdata['name']
        major=userdata['major']
        year=userdata['year']
        rescollege=userdata['residentialcollege']
        days=request.POST.getlist('day')
        duration=request.POST['duration']
        workout_type=request.POST['workout_type']
        time_zone=request.POST['time_zone']
        group_size=request.POST['group_size']

        #list of data
        user_data_list=[netID,days,duration,workout_type,time_zone,group_size]

        user_data_list_df=pandas.DataFrame(user_data_list)
        #list of requests in dataframe
        requestsList=list(BuddyRequest.objects.all().values())
        #dataframe of requests
        requestsdf=pandas.DataFrame(requestsList)

        #COMPARISION BETWEEN USER DATA AND REQUESTS ENTERED HERE

        inputnetID = user_data_list[0]
        input1 = user_data_list[1]
        input2 = user_data_list[2]
        input3 = user_data_list[3]
        input4 = user_data_list[4]
        input5 = user_data_list[5]
        input6 = user_data_list[6] # all these inputs are temporary variables. Ideally, the GUI will stores these values as variables

        Dfuser = Df_creator(inputnetID,input1, input2, input3, input4, input5,
                            input6)  # takes all user data and creates a dataframe of one row for that user.

        # reading in csv file and converting it into a dataframe. The code doesn't need to read in a csv file specifically, but as long as the final product after line
        # 91 is a dataframe, the algo will work.

        Dfrq = requestsdf

        # Script that takes inputs as variables and appends value to dataframe.

        if len(Dfrq) < 1:  # if there is no one in the Dfrq, then we add the Dfuser back into database. The code under this if statement only works for csv.
            req = BuddyRequest(name=name, major=major, year=year, rescollege=rescollege, days=days, duration=duration,
                               workout_type=workout_type, time_zone=time_zone, group_size=group_size, user=request.user)
            req.save()
            return render(request, 'waiting.html')

        else:

            # list of all the names in Dfrq -- This will be very useful later on

            names = Dfrq.iloc[:, 1].tolist()
            netID = Dfrq.iloc[:, "Vinay, list whatever index the netID is stored as"].tolist()

            # Our dataframes, when using the matching algorithm, should not use the names as a parameter for matching.
            # We can store these names in a temp file: lists.

            user_name = Dfuser.pop("Name")
            user_netID = Dfuser.pop("NetID")
            Dfrq_names = Dfrq.pop("Name")


            # creatinga dictionary, "reference", that contains the names as keys and other parameters as values.
            # We can use these values later to reference names.

            parameter_list = []

            for x in range(0, len(Dfrq)):
                entry = []
                for i in range(0, len(Dfrq.columns)):
                    list_of_vals = Dfrq.iloc[:, i].tolist()
                    v = list_of_vals[x]
                    entry.append(v)
                parameter_list.append(entry)

            reference = dict_creator(names, parameter_list)

            # creating dictionary, "reference_NETID", that contains the netID as keys and other parameters as values.
            #Note that this dictionary does not include the names of the user or request df.

            reference_NETID = dict_creator(netID, parameter_list)



            # Line of code that actually matches the user with the people still in request dataframe. Outputs a new dataframe of matched people

            left_on = right_on = ["Day_Av", "Duration", "Type_Workout", "Time_z", "No_Ppl"]
            matched_results = fm.fuzzy_left_join(Dfuser, Dfrq, left_on, right_on, left_id_col="Day_Av",
                                                 right_id_col="Day_Av")

            # for easier viewing
            pd.set_option("display.max_rows", None, "display.max_columns",
                          None)  # line of code that allows me to see the full dataframe

            # dropping irrelevant columns and displaying relevant info of the matched person

            matched_results = matched_results.drop(columns=["__id_left", "__id_right", "Day_Av_left", "Duration_left",
                                                            'Type_Workout_left', "Time_z_left", "No_Ppl_left"])

            list_col = matched_results.columns.tolist()
            list_col = list_col[1:]

            # code that renames matched_results with better colummn labels
            label_dict = dict_creator(list_col, left_on)
            matched_results = matched_results.rename(columns=label_dict)

            # this loop gets rid of values that do not meet a certain threshold
            for x in range(0, len(matched_results)):
                if matched_results.iloc[x][
                    "best_match_score"] < .05:  # the threshold for the best match score can be changed later after we test
                    matched_results = matched_results.drop(matched_results.index[x])

            # If no one meets the threshold, then we append the user data back into the dataframe

            if len(matched_results) == 0:
                req = BuddyRequest(name=name, major=major, year=year, rescollege=rescollege, days=days,
                                   duration=duration,
                                   workout_type=workout_type, time_zone=time_zone, group_size=group_size,
                                   user=request.user)
                req.save()
                return render(request, 'waiting.html')

            else:  # this is assuming we have valid matches in the dataframe
                # After matching, this loop extracts the top three matches and gets all the parameters
                validator = []

                for x in range(0, len(matched_results)):  # loop ensures we have the top three entries
                    if len(validator) < 3:
                        entry = []
                        for i in range(1, len(matched_results.columns)):
                            list_of_vals = matched_results.iloc[:, i].tolist()
                            v = list_of_vals[x]
                            entry.append(v)
                        validator.append(entry)

                list_names = []
                list_netID = []

                for parameters in validator:
                    names_associated = getKeysByValue(reference, parameters)
                    list_names.append(names_associated)

                    netID_associated = getKeysByValue(reference_NETID, parameters)
                    list_netID.append(netID_associated)



                matched_results.insert(0, "Names", list_names)  # line of code adds the name into the matched_results df
                matched_results.inster(1, "NetID", list_netID)  # line of code adds the name into the matched results df

                matched_results["Day_Av"] = matched_results["Day_Av"].astype(
                    object)  # columns that will eventually stoe lists must have a different datatype --> "objects"
                matched_results['Type_Workout'] = matched_results["Type_Workout"].astype(object)

                # unstringing days and type of workouts

                updated_day = []
                updated_work_type = []

                for day in matched_results.loc[:, "Day_Av"]:
                    day = day.strip('][').split(', ')

                    for i in range(0, len(day)):
                        if day[i] == "1":
                            day[i] = "Monday"
                        elif day[i] == "2":
                            day[i] = "Tuesday"
                        elif day[i] == "3":
                            day[i] = "Wednesday"
                        elif day[i] == "4":
                            day[i] = "Thursday"
                        elif day[i] == "5":
                            day[i] = "Friday"
                        elif day[i] == "6":
                            day[i] = "Saturday"
                        else:
                            day[i] = "Sunday"

                    updated_day.append(day)

                for work in matched_results.loc[:, "Type_Workout"]:
                    work = work.strip('][').split(', ')

                    for j in range(0, len(work)):
                        if work[j] == "1":
                            work[j] = "Abs"
                        elif work[j] == "2":
                            work[j] = "Upper Body"
                        elif work[j] == "3":
                            work[j] = "Cardio"
                        else:
                            work[j] = "Lower Body"

                    updated_work_type.append(work)

                for index in range(0, len(matched_results)):
                    matched_results.at[index, "Day_Av"] = updated_day[
                        index]  # replacing placeholder values with sorted lists created above
                    matched_results.at[index, "Type_Workout"] = updated_work_type[index]

                # matched results is the final dataframe that includes the person the user matches with

                matchedName=name
                matchedRequest=BuddyRequest.objects.filter(name=matchedName)
                return render(request,'waiting.html',{'matched_person_name':matchedName})



@login_required(login_url='/accounts/signup')
def about(request):
    return render(request,'about.html')
