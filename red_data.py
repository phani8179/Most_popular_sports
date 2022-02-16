import requests
import pandas as pd
import datetime
from datetime import datetime

import pymongo
import requests
my_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_data_base = my_client["test"]
my_collection = my_data_base["redditvotes"]

# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        data={}
        data['subreddit']= post['data']['subreddit']
        data['title']= post['data']['title']
        data['selftext']= post['data']['selftext']
        data['upvote_ratio']= post['data']['upvote_ratio']
        data['ups']= post['data']['ups']
        data['downs']= post['data']['downs']
        data['score']= post['data']['score']
        data['link_flair_css_class']= post['data']['link_flair_css_class']
        data['created_utc']= datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ')
        data['id']= post['data']['id']
        data['kind']= post['kind']
        my_collection.insert_one(data)
        df = df.append(data,ignore_index=True)

    return df

# authenticate API
client_auth = requests.auth.HTTPBasicAuth('G1jA-xG7EzhMUnv7oT5rgQ', 'UEslAD7QJQ5yxrCNmAMN-m_E9fehvQ')
data = {
    'grant_type': 'password',
    'username': 'Phanisai2921',
    'password': 'phani123'
}
headers = {'User-Agent': 'phanisai2921'}

# send authentication request for OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)
# extract token from response and format correctly
token = f"bearer {res.json()['access_token']}"
# update API headers with authorization (bearer token)
headers['Authorization'] = token

# initialize dataframe and parameters for pulling data in loop
data = pd.DataFrame()
params = {'limit': 1000}

# loop through 10 times (returning 1K posts)
for i in range(3):
    # make request
    res = requests.get("https://oauth.reddit.com/r/soccer/new",
                       headers=headers,
                       params=params)

    # get dataframe from response
    new_df = df_from_response(res)
    # take the final row (oldest entry)
    row = new_df.iloc[len(new_df)-1]
    # create fullname
    fullname = row['kind'] + '_' + row['id']
    # add/update fullname in params
    params['after'] = fullname
    
    # append new_df to data
    data = data.append(new_df, ignore_index=True)
print(data)