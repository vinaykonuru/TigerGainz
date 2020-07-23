import pandas
import pandas as pd
import fuzzymatcher as fm

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
        {"id":0, "netID": inputNetID, "name": [input1], "days": d, "duration": [input3], "workout_type": w, "time_zone": [input5],
         "group_size": [input6]})

    return user_frame  # this is the object we get from the function


def getKeysByValue(dictOfElements, valueToFind):  # function finds keys(names) from attributes (parameters)
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[0] == valueToFind:
            return item[1]


def dict_creator(key, value):  # makes dictionary from two lists containing the list of keys and list of values
    dictionary = {}
    for item in key:
        dictionary[item] = value[key.index(item)]
    return dictionary

def matcher(Dfrq, Dfuser):
    #MATCHING OCCURS HERE
    left_on = right_on = ["id", "days", "duration", "workout_type", "time_zone", "group_size"]

    matched_results = fm.fuzzy_left_join(Dfuser, Dfrq, left_on, right_on, left_id_col="days",
                                         right_id_col="days")

    # dropping irrelevant columns and displaying relevant info of the matched person
    matched_results = matched_results.drop(columns=["__id_left", "__id_right","id_left", "days_left", "duration_left",
                                                    'workout_type_left', "time_zone_left", "group_size_left"])


    #COLUMNS OF ALL DATA
    list_col = matched_results.columns.tolist()
    list_col = list_col[1:]
    # code that renames matched_results with better colummn labels\
    label_dict = dict_creator(list_col, left_on)


    #our first matched result
    matched_results1 = matched_results.rename(columns=label_dict)

    rel_val = int(matched_results1.iloc[0,1])

    list_id = Dfrq["id"].tolist()

    for id in list_id:
        if id == rel_val:
            id_index = list_id.index(id)

    Dfrq = Dfrq.drop(id_index)
    Dfrq = Dfrq.reset_index(drop=True)

    return matched_results1, Dfrq

def get_matches(user_data_list,requestsList):
    id_name_dict={}
    for row in requestsList:
        netID_name=(row['netID'],row['name'])
        id_name_dict[row['id']]=netID_name
    # id_name_dict{row.id}
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

    # list of all the names in Dfrq -- This will be very useful later on

    names = Dfrq.pop('name').tolist()
    netID_dict = Dfrq.pop('netID').tolist()
    pictures= Dfrq.pop('profile_picture').tolist()
    # Our dataframes, when using the matching algorithm, should not use the names as a parameter for matching.
    # We can store these names in a temp file: lists.

    user_name = Dfuser.pop("name")
    user_netID = Dfuser.pop("netID")
    Dfrq=Dfrq.drop(columns=['rescollege','major','user_id','year'])
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

    reference_NETID = dict_creator(netID_dict, parameter_list)


    #getting our 3 match results:
    match_result, Dfrq = matcher(Dfrq, Dfuser)
    match_result1, Dfrq = matcher(Dfrq, Dfuser)
    match_result2, Dfrq = matcher(Dfrq, Dfuser)

    match_df = pd.concat([match_result, match_result1, match_result2], ignore_index=True)

    #determining threshold
    max=0.06989700043360188
    threshold=max/4
    for x in range(0, len(match_df)):
        if match_df.iloc[x][
            "best_match_score"] < -50:  # the threshold for the best match score can be changed later after we test
            matched_results = match_df.drop(match_df.index[x])

    # If no one meets the threshold, then we append the user data back into the dataframe
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


        list_names = []
        list_netID = []
        #for each matched row, find the correct netID and name by matching with id and add it to matched row
        for parameters in list_params:
            names_id_associated = getKeysByValue(id_name_dict, parameters[5])
            list_names.append(names_id_associated[1])
            list_netID.append(names_id_associated[0])

        match_df.insert(0, "netID", list_netID)  # line of code adds the name into the matched results df
        match_df.insert(1, "names", list_names)  # line of code adds the name into the matched_results df
        match_df["days"] = match_df["days"].astype(
            object)  # columns that will eventually store lists must have a different datatype --> "objects"
        match_df['workout_type'] = match_df["workout_type"].astype(object)


        # unstringing days and type of workouts

        updated_days = []
        updated_work_type = []

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
            entry[2]=entry[2]/max*100

    return matched_people
