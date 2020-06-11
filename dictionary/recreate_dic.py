import json

raw_data_frame = json.load(open('data.json', 'r'))
formatted_df = {key.lower(): raw_data_frame[key] for key in raw_data_frame}

if 'delhi' in formatted_df.keys():
    print(formatted_df['delhi'])