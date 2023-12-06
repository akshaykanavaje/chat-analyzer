# this function converts your data into required dataframe

import re
import pandas as pd

def preprocess(data):
    # TO SPLIT THE MESSAGES FROM DATE-TIME
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]

    # now we will store date-time into another dataframe
    date1 = re.findall(pattern, data)
    cleaned_list = [s.replace('\u202f', '') for s in date1]
    date = cleaned_list

    # convert date column into date time format
    df = pd.DataFrame({"user_msg": messages, "date": date})
    df["date"] = pd.to_datetime(df["date"], format='%m/%d/%y, %I:%M%p - ')

    # separate user and message
    messages = []
    users = []

    for message in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_msg'], inplace=True)



    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df