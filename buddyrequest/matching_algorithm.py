import pandas as pd
from fuzzywuzzy import fuzz
from statistics import mean
import pytz_convert as pc

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

def set_comparision(user_set, request_set):
    max_length = 0
    similarities = 0

    if (user_set & request_set):
        if len(user_set) >= len(request_set):
            max_length = len(user_set)

        else:
            max_length = len(request_set)

    if(max_length == 0): # if there are no similarities
        similarities = 0
        return similarities
    for user_row in user_set:
        for req_row in request_set:
            if(user_row == req_row):
                similarities = similarities + 1
    percent_match = similarities / max_length * 100
    return percent_match

def get_matches(user_data_list, requests_list):


    pd.set_option("display.max_rows", None, "display.max_columns", None) # makes printing out of large dataframes easier

    #############################################STEP 1: DATAFRAME CREATION#############################################
    requestsdf = pd.DataFrame(requests_list) # converts requests list into a dataframe

    # gets relevant information from requests dataframe
    names = requestsdf.loc[:,'name'].tolist()
    net_id = requestsdf.loc[:, "netID"].tolist()
    id_list = requestsdf.loc[:, "id"].tolist()

    # creating a list of tuples containing the name and netID of each entry in the request database
    name_netID = []

    for entry in range(len(names)):
        h = (names[entry], net_id[entry])
        name_netID.append(h)


    preferences = user_data_list[0] # is a list of how the user ranks each of the workout matching factors
    user_days = user_data_list[1]
    user_duration = user_data_list[2]
    user_workout = user_data_list[3]
    user_time_zone = user_data_list[4]
    user_intensity = user_data_list[5]
    user_location = user_data_list[6]
    Dfuser = pd.DataFrame({"days": user_days, "duration": user_duration, "workout_type": user_workout,
                           "time_zone": user_time_zone,"intensity": user_intensity,"location": user_location })


    Dfrq = requestsdf.drop(columns = ['name', 'id','netID','rescollege','major','year','user_id','partner_id','created','updated'])


    #Mock priorities dictionary [PLACE HOLDER]
    priorities = {"days":preferences[1] ,"duration": preferences[2], "time_zone":preferences[0]}
    reference_ranker = {0: 50.0, 1: 30.0, 2: 10.0}

    '''At the end of step 1, two dataframes are created. Dfrq: a dataframe for all existing users already in the database
    and Dfuser: a dataframe with one row that contains all the matching preferences of the user trying to make a match.
    '''

    ################################################STEP 2: MATCHING###################################################

    # following code guarantees that all workout users will have the same workout type regardless of other preferences


    matching_df_request = pd.DataFrame({}) # creating a new empty dataframe for people that have the same workout type
    Dfrq_row_list = [] # empty list for  all the index of the user in the request database

    # for loop guarantees match has same type of workout and adds users with the same workout to matching_df_request
    workout_common_percentage = [] #a list of how well people match based solely on workout type

    for index_row in range(len(Dfrq)):
        request_workout = Dfrq.iloc[index_row]["workout_type"]
        request_location = Dfrq.iloc[index_row]["location"]

        # confirm that location is the same:
        if user_location == request_location:

            # confirm if at least one workout is met

            set_user_workout = set(user_workout.strip('][\'').split(','))
            set_request_workout = set(request_workout.strip('][\'').split(','))
            percentage = set_comparision(set_user_workout, set_request_workout)

            if percentage > 0:

                workout_common_percentage.append(percentage)
                row = Dfrq.iloc[index_row]
                matching_df_request = matching_df_request.append(row) #this is the dataframe that we will be comparing with Dfuser to find the
                                                                    #actualy matches
                Dfrq_row_list.append(index_row) # appends that user's row index to Dfrq_row_list

    matching_df_request["Dfrq_index"] = Dfrq_row_list

    if len(matching_df_request) > 0: # if we have users in the new dataframe we can drop workouts as a matching parameter
                                    # since we already matched based on workouts.

        matching_df_user = Dfuser.drop("workout_type", axis=1)
        matching_df_user = Dfuser.drop("location", axis=1)
        matching_df_request = matching_df_request.drop("workout_type", axis=1)
        matching_df_request = matching_df_request.drop("location", axis=1)
        column_labels = matching_df_request.columns.tolist()


    else: # break and return a blank array back to views
        blankarray=[]
        return blankarray

    '''
    Following code matches of the rest of the parameters. Using a double for loop, it goes through every column (workout factor) of
    every row (user in the matching dataframe) and compares each factor to the entry in the user dataframe. Regardless of
    matching parameter here are a few variables to keep in mind:

    rel_val = how good a match is for that specific parameter. e.g. a rel_val of 100 in "days" would indicate a perfect match
              for days.

    ranker = the priority that user gives to that factor. e.g ranker = 1 for days would indicate the user trying to match
    gives weights days the most important.

    For every rank there is a set cut_off for the minimum best match score for the
    respective workout factor. This cut_off is stored in a dictionary.
    '''
    print(matching_df_user)
    ListOfMatches = [] # array where all suitable matches will be appended to later
    for row in range(len(matching_df_request)):
        list_best_match_vals = [] # for every user we generate an array
        for column in range(len(column_labels)):
            if column_labels[column] == "days":
                request_days = matching_df_request.iloc[row][column]
                # rel_val = fuzz.partial_token_sort_ratio(request_days, matching_df_user.iloc[0][column])
                set_user_days = set(user_days)
                set_rq_days = set(request_days.strip('][\'').replace(' ','').replace('\'','').split(','))
                rel_val = set_comparision(set_user_days, set_rq_days)
                ranker = priorities.get(column_labels[column])
                cut_off = reference_ranker.get(ranker)

                weighted_average = (cut_off / 100) * rel_val
                if rel_val >= cut_off: # if minimum score is not met, we discard the prospective match completely
                    list_best_match_vals.append(weighted_average)
                else:
                    break

            elif column_labels[column] == "duration":
                ranker = priorities.get(column_labels[column]) #gets the priority of duration
                window = (ranker)*(30.0) #calculates a window of acceptable time e.g. 60 minutes can still be matched with 90 mins
                rq_duration = matching_df_request.iloc[row][column]
                delta =  abs(user_duration - rq_duration)
                if delta <= window:
                    rel_val = (window - delta) / window * 100
                    cut_off = reference_ranker.get(ranker)

                    weighted_average = (cut_off / 100) * rel_val
                    list_best_match_vals.append(weighted_average)

                else:
                    break

            elif column_labels[column] == "time_zone":
                ranker = priorities.get(column_labels[column])  # gets the priority of time zone --> also determines the window of error allowed for time zone
                                                                   # e.g. a person who ranks timezone as their #1 priority would match with ppl +/- 1 hour
                window = ranker
                request_time_zone = matching_df_request.iloc[row][column]

                #convert to integer utc time
                user_utc_shift = int(pc.convert_tz_abbrev_to_tz_offset(user_time_zone))/100
                request_utc_shift = int(pc.convert_tz_abbrev_to_tz_offset(request_time_zone))/100

                delta = abs(user_utc_shift - request_utc_shift)
                if delta <= window:
                    rel_val = (window - delta) / window * 100
                    cut_off = reference_ranker.get(ranker)

                    weighted_average = (cut_off / 100) * rel_val
                    list_best_match_vals.append(weighted_average)

                else:
                    break

            # else:
            #     print(matching_df_user)
            #     print(column)
            #     print(row)
            #     print(len(column_labels))
            #     rel_val = fuzz.partial_ratio(matching_df_request.iloc[row][column],
            #                                             matching_df_user.iloc[0][column])
            #     cut_off = 0
            #     weighted_average = (cut_off / 100) * rel_val
            #     if rel_val >= cut_off:  # if minimum score is not met, we discard the prospective match completely
            #         list_best_match_vals.append(weighted_average)
            #     else:
            #         break
        print('here')
        if len(list_best_match_vals) == 3: #if every single column managed to pass the cut_off val
            Dfrq_index = matching_df_request.iloc[row]["Dfrq_index"]
            workout_percentage = workout_common_percentage[Dfrq_index]
            average = (mean(list_best_match_vals) + workout_percentage)/2
            list_best_match_vals.append(average)
            list_best_match_vals.append(Dfrq_index)
            ListOfMatches.append(list_best_match_vals) #last element of each sublist is the index of that row in the database

        #ListOfMatches is a nested list containing

    n = 0
    while n < len(ListOfMatches): #will stop the loop when we have looped through n-1 times
        n += 1 #counter that ensures we are below n
        for i in list(range(len(ListOfMatches) - 1)): #for every index value in list of index values
          if ListOfMatches[i][-2] < ListOfMatches[i+1][-2]: #Conditional statement that compares if i and its adjacent value
                                                            #-2 ensures that the sorting is based on the final weighted average
                                                            #for each row
            ListOfMatches[i], ListOfMatches[i+1] = ListOfMatches[i+1], ListOfMatches[i] #swaps if adjacent value is smaller


    row_index = []
    for entry in ListOfMatches:
        val = entry[-1]
        row_index.append(val)

    presentation_list = []
    for index in row_index:
        row = Dfrq.iloc[index].tolist()
        presentation_list.append(row)

    return presentation_list
