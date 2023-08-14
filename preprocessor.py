import pandas as pd
import re
def preprocess(data):
    msg_pattern = '^\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'
    data_time_pattern = '^\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm]'

    # Initialize empty lists to store data and messages
    messages_list = []
    current_entry = []
    date_time = []
    line_arr = data.split('\n')
    # Iterate through lines and process data
    for line in line_arr:
        line = line.strip()
        if re.match(msg_pattern, line):
            msg = re.split(msg_pattern, line)
            dt = re.findall(data_time_pattern, line)
            date_time.append(dt[0])
            messages_list.append(msg[1])
        else:
            current_entry.append(line)

    # converting to pandas dataframe
    df = pd.DataFrame({'messages': messages_list, 'date_time': date_time})

    def timestamp_converter(datetime_string):
        cleaned_datetime_str = re.sub(r'[^\x00-\x7F]+', '', datetime_string)
        return pd.to_datetime(cleaned_datetime_str)

    df['date_time'] = df['date_time'].map(timestamp_converter)

    users = []
    messages = []
    for msg in df['messages']:
        # print(msg)
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages

    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day

    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    return  df
