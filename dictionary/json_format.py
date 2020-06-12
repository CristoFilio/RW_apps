import json

data_frame = json.load(open('data.json','r'))
formatted_data=[]
#data frame is a dictionary containing keys/words and values/definitions
for key in data_frame:
    for value in data_frame[key]:
        formatted_data.append({'word':key,'definition':value})

with open('mysql_dict.json', 'w') as file:
    json.dump(formatted_data,file)