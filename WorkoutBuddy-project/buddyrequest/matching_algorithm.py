import pandas
import pandas as pd
import fuzzymatcher as fm
from buddyrequest.models import BuddyRequest

def Df_creator(inputDays, inputDuration,inputWorkoutType,inputTimeZone,inputGroupSize):  # Process information and stores strings as numbers
    day_lister = inputDays  # will ensure the days is always in a list datatype
    workout_lister = inputWorkoutType  # will ensure the workouts are in a list datatype
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

        if workout_lister[j] == "Running":
            workout_lister[j] = 1
        elif workout_lister[j] == "Lifting":
            workout_lister[j] = 2
        elif workout_lister[j] == "Biking":
            workout_lister[j] = 3
        else:
            workout_lister[j] = 4 #Swimming
    workout_lister.sort()  # Ensures that list will be in order
    w = str(workout_lister)

    # This is the basic framework of user database (row)
    #id 0 temporary for comparision with dataframe that has id based on addition to database
    user_frame = pd.DataFrame(
        {"days": d, "duration": [inputDuration], "workout_type": w, "time_zone": [inputTimeZone], "group_size": [inputGroupSize]})

    return user_frame  # this is the object we get from the function


def Keys_from_values(dict,value):
    for item in dict.values():
        if item == value:
            value_list = list(dict.values())
            indexer = value_list.index(value)
            key_list = list(dict.keys())
            ret_val = key_list[indexer]

    return ret_val


def dict_creator(key, value):  # makes dictionary from two lists containing the list of keys and list of values
    dictionary = {}
    for item in key:
        dictionary[item] = value[key.index(item)]
    return dictionary

def matcher(Dfrq, Dfuser):
    # MATCHING OCCURS HERE
    left_on = right_on = ["days", "duration", "workout_type", "time_zone", "group_size"]
    matched_results = fm.fuzzy_left_join(Dfuser, Dfrq, left_on, right_on, left_id_col="days",
                                         right_id_col="days")



    # dropping irrelevant columns and displaying relevant info of the matched person
    matched_results = matched_results.drop(
        columns=["__id_left", "__id_right", "days_left", "duration_left",
                 'workout_type_left', "time_zone_left", "group_size_left"])



    # COLUMNS OF ALL DATA
    list_col = matched_results.columns.tolist()
    list_col = list_col[1:]

    # code that renames matched_results with better colummn labels\
    label_dict = dict_creator(list_col, left_on)


    # our first matched result
    matched_results1 = matched_results.rename(columns=label_dict)
    list_Dfrq = Dfrq.values.tolist()
    del list_Dfrq[0] # remove first element

    Dfrq = pd.DataFrame(list_Dfrq, columns=left_on)
    top_matched_row=matched_results1[0:1]
    return  top_matched_row, Dfrq

def get_matches(user_data_list,requestsList):
    #dataframe of requests
    Dfrq=pandas.DataFrame(requestsList)

    #COMPARISION BETWEEN USER DATA AND REQUESTS ENTERED HERE
    inputDays = user_data_list[6]
    inputDuration = user_data_list[7]
    inputWorkoutType = user_data_list[8]
    inputTimeZone = user_data_list[9]
    inputGroupSize = user_data_list[10] # all these inputs are temporary variables. Ideally, the GUI will stores these values as variables
    Dfuser = Df_creator(inputDays, inputDuration,inputWorkoutType,inputTimeZone,inputGroupSize)

    #will return Dfuser_return but use Dfuser_comparision to compare to Dfrq
                          # takes all user data and creates a dataframe of one row for that user.
    # reading in csv file and converting it into a dataframe. The code doesn't need to read in a csv file specifically, but as long as the final product after line
    # 91 is a dataframe, the algo will work.
    # Script that takes inputs as variables and appends value to dataframe.

    # list of all the names in Dfrq -- This will be very useful later on
    print(Dfrq)
    people_ID_list = Dfrq.pop("id").tolist()
    # names_rq = Dfrq.pop('name').tolist()
    # netID_rq = Dfrq.pop('netID').tolist()
    # pictures_rq= Dfrq.pop('profile_picture').tolist()
    excess_values_list=[]
    for entry in Dfrq.values.tolist():
        excess_entries=[entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[11]]
        excess_values_list.append(excess_entries)
    Dfrq=Dfrq.drop(columns=['netID','name','rescollege','major','year','profile_picture','user_id'])


    # Our dataframes, when using the matching algorithm, should not use the names as a parameter for matching.
    # We can store these names in a temp file: lists.
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

    reference_parameters = dict_creator(people_ID_list, parameter_list)
    reference_excess = dict_creator(people_ID_list, excess_values_list)


    #getting our 3 match results:
    match_result, Dfrq = matcher(Dfrq, Dfuser)
    if len(Dfrq) >= 1:
        match_result1, Dfrq = matcher(Dfrq, Dfuser)
        if len(Dfrq) >= 1:
            match_result2, Dfrq = matcher(Dfrq, Dfuser)
            match_df = pd.concat([match_result, match_result1, match_result2], ignore_index=True)
        else:
            match_df = pd.concat([match_result, match_result1], ignore_index=True)
    else:
        match_df = pd.concat([match_result], ignore_index=True)

    #determining threshold
    max=0.06989700043360188
    threshold=max/4
    x=0
    while x < len(match_df):
        if match_df.iloc[x][
            "best_match_score"] < -50:  # the threshold for the best match score can be changed later after we test
            match_df = match_df.drop(match_df.index[x])
        else:
            x+=1
    # If no one meets the threshold, then we append the user data back into the dataframe
    matched_people=[]
    if len(match_df) == 0:
        print("terrible matches")

    else:  # this is assuming we have valid matches in the dataframe
        # After matching, this loop extracts the top three matches and gets all the parameters

        list_params = []

            # loop ensures we have the top 3 ENTRIES
        for x in range(0, len(match_df)):
                entry = []
                for i in range(1, len(match_df.columns)):
                    list_of_vals = match_df.iloc[:, i].tolist()
                    v = list_of_vals[x]
                    entry.append(v)
                list_params.append(entry)

        list_people_id=[]
        list_netID = []
        list_names = []
        list_major=[]
        list_year=[]
        list_rescollege=[]
        list_profile_picture=[]
        list_user_id=[]
        #for each matched row, find the correct netID and name by matching with id and add it to matched row
        #for each matched row, find the correct netID and name by matching with id and add it to matched row

        for parameters in list_params:
            id = Keys_from_values(reference_parameters, parameters)
            list_people_id.append(id)

        for id in list_people_id:
            excess_list = reference_excess[id]
            list_netID.append(excess_list[0])
            list_names.append(excess_list[1])
            list_major.append(excess_list[2])
            list_year.append(excess_list[3])
            list_rescollege.append(excess_list[4])
            list_profile_picture.append(excess_list[5])
            list_user_id.append(excess_list[6])

        match_df.insert(0, "netID", list_netID)  # line of code adds the name into the matched results df
        match_df.insert(1, "names", list_names)  # line of code adds the name into the matched_results df
        match_df.insert(2, "major", list_major)  # line of code adds the name into the matched_results df
        match_df.insert(3, "year", list_year)  # line of code adds the name into the matched results df
        match_df.insert(4, "rescollege", list_rescollege)  # line of code adds the name into the matched_results df
        match_df.insert(5, "profile_picture", list_profile_picture)  # line of code adds the name into the matched_results df
        match_df.insert(6, 'user_id', list_user_id)
        match_df["days"] = match_df["days"].astype(object)  # columns that will eventually store lists must have a different datatype --> "objects"
        match_df['workout_type'] = match_df["workout_type"].astype(object)

        # unstringing days and type of workouts

        updated_days = []

        for days in match_df.loc[:, "days"]:
            #days is in string format of list
            days=days.strip('[]').split(',')
            day_temp=[]
            for day in days:
                day=day.strip()
                if day == "1":
                    day_temp.append('Monday')
                elif day == "2":
                    day_temp.append('Tuesday')
                elif day == "3":
                    day_temp.append('Wednesday')
                elif day == "4":
                    day_temp.append('Thursday')
                elif day == "5":
                    day_temp.append('Friday')
                elif day == "6":
                    day_temp.append('Saturday')
                else:
                    day_temp.append('Sunday')
            updated_days.append(day_temp)

        updated_work_type = []

        for work in match_df.loc[:, "workout_type"]:
            work = work.strip('][').split(', ')
            work_temp=[]
            for type in work:
                type=type.strip()
                if type == "1":
                    work_temp.append("Running")
                elif type == "2":
                    work_temp.append("Lifting")
                elif type == "3":
                    work_temp.append("Biking")
                else:
                    work_temp.append("Swimming")
            updated_work_type.append(work)

        for index in range(0, len(match_df)):
            match_df.at[index, "workout_type"] = updated_work_type[index]
            match_df.at[index, "days"] = updated_days[index]
        # matched results is the final dataframe that includes the person the user matches with
        matched_people=match_df.values.tolist()
        # change match scores to percentages
        for entry in matched_people:
            entry[7]=entry[7]/max*100
    return matched_people
