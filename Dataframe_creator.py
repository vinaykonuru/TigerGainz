import pandas as pd
from fuzzywuzzy import fuzz
from statistics import mean

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

#importing data
df = pd.read_csv('data.csv')
df1 = pd.read_csv("data.csv")

names = df.loc[:,'name'].tolist()
net_id = df.loc[:, "netID"].tolist()
id_list = df.loc[:, "id"].tolist()

name_netID = []


for entry in range(len(names)):
    h = (names[entry], net_id[entry])
    name_netID.append(h)

id_name_dict = dict_creator(id_list, name_netID)
user_data_list = df.iloc[0, :].tolist()


#dataframe of requests
pd.set_option("display.max_rows", None, "display.max_columns", None)

requestsdf=df

inputdays = "[Tuesday, Wednesday, Thursday]"
inputworkouttype = "[Lifting]"

Dfuser = pd.DataFrame({"days": [inputdays], "duration": user_data_list[6], "workout_type": [inputworkouttype], "time_zone": user_data_list[8]})
Dfrq = requestsdf


Dfrq1 = Dfrq.drop(columns = ['name', 'id','netID','rescollege','major','year','user_id', "group_size"])


#Mock priorities dictionary
priorities = {"days": 2, "duration": 1, "time_zone": 3}



#The following code loopes through the request database and makes sure that all potential candidates for matches at least
#have the same workout
reference_ranker = {1: 100, 2:60, 3:50}

workout = Dfuser.iloc[0]["workout_type"]

matching_df_request = pd.DataFrame({})
Dfrq_row_list = []

for index_row in range(len(Dfrq1)):
    if fuzz.ratio(workout, Dfrq1.iloc[index_row]["workout_type"]) == 100:
        row = Dfrq1.iloc[index_row]
        matching_df_request = matching_df_request.append(row) #this is the dataframe that we will be comparting with Dfuser to find the
                                                                #actualy matches
        Dfrq_row_list.append(index_row)

matching_df_request["Dfrq_index"] = Dfrq_row_list


if len(matching_df_request) > 0:
    matching_df = matching_df_request.drop("workout_type", axis=1) #we no longer need to have workouts as a parameter since we already made sure
                                                                     #users had the same workout.
else:
    print("return to home screen")

matching_df_user = Dfuser.drop("workout_type", axis=1)
matching_df_request = matching_df_request.drop("workout_type", axis=1)
column_labels = matching_df_request.columns.tolist()

ListOfMatches = []
for row in range(len(matching_df_request)):
    list_best_match_vals = []
    for column in range(len(column_labels)-1):
        if column_labels[column] == "days":
            rel_val = fuzz.partial_token_sort_ratio(matching_df_request.iloc[row][column], matching_df_user.iloc[0][column])
            ranker = priorities.get(column_labels[column])
            cut_off = reference_ranker.get(ranker)

            if rel_val >= cut_off:
                list_best_match_vals.append(rel_val)
            else:
                break
        else:
            rel_val = fuzz.ratio(matching_df_request.iloc[row][column], matching_df_user.iloc[0][column])
            ranker = priorities.get(column_labels[column])
            cut_off = reference_ranker.get(ranker)

            if rel_val >= cut_off:
                list_best_match_vals.append(rel_val)
            else:
                break

    if len(list_best_match_vals) == len(column_labels) - 1:
        average = mean(list_best_match_vals)
        list_best_match_vals.append(average)
        Dfrq_index = matching_df_request.iloc[row]["Dfrq_index"]
        list_best_match_vals.append(Dfrq_index)
        ListOfMatches.append(list_best_match_vals)

#ListOfMatches is a nested list containing


n = 0
while n < len(ListOfMatches): #will stop the loop when we have looped through n-1 times
    n += 1 #counter that ensures we are below n
    for i in list(range(len(ListOfMatches) - 1)): #for every index value in list of index values
      if ListOfMatches[i][-2] < ListOfMatches[i+1][-2]: #Conditional statement that compares if i and its adjacent value
        ListOfMatches[i], ListOfMatches[i+1] = ListOfMatches[i+1], ListOfMatches[i] #swaps if adjacent value is smaller


row_index = []
for entry in ListOfMatches:
    val = entry[-1]
    row_index.append(val)

presentation_list = []
for index in row_index:
    row = Dfrq.iloc[index].tolist()
    presentation_list.append(row)

print(presentation_list)




