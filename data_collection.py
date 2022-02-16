import datetime
from datetime import datetime

import pymongo
import requests

## this  script is used to collect the reddit data
# The subreddits are extracted from reddit
#search the for comments from the subreddits pulled and save this data in the database

my_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_data_base = my_client["test"]
my_collection = my_data_base["redditnew"]

client_secret = "UEslAD7QJQ5yxrCNmAMN-m_E9fehvQ"

client_id = "G1jA-xG7EzhMUnv7oT5rgQ"
user_agent = "phanisai2921"
username = "Phanisai2921"
password = "phani123"

base_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': username, 'password': password}
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
api_url = 'https://oauth.reddit.com'
headers = {}
red_data=[]

bearer_response = requests.post(base_url + 'api/v1/access_token',
                                    data=data,
                                    headers={'user-agent': 'phanisai2921'},
                                    auth=auth)
print(bearer_response)
if bearer_response.status_code == 200:
    bearer_details = bearer_response.json()
    print(bearer_details)
    token = 'bearer ' + bearer_details['access_token']
    headers['Authorization'] = token
    headers['User-Agent'] = user_agent
    response = requests.get(api_url + '/api/v1/me', headers=headers)
    print(response)
if response.status_code == 200:
    filters = ('worldcup', 'F1', 'racing', 'cycling' ,'football', 'soccer','NBA','baseball', 'basketball', 'cricket', 'rugby', 'americanfootball', 'copaamerica', 'fifa', 'championsleague')
    payload = {'q':filters,'limit':1000,'sort':'relevance' or 'new' or 'trending','type':'sr'}
    subreddit_response = requests.get(api_url + '/search/',
                                      headers=headers, params=payload)
                                      
    subreddit_response=subreddit_response.json()
    print(subreddit_response)
    for i in subreddit_response['data']['children']:
        sub_res=i['data']
        dat={}
        dat['subscribers']=sub_res['subscribers']
        dat['title']=sub_res['title']
        dat['description']=sub_res['public_description']
        dat['id']=sub_res['id']
        dat['created']=datetime.fromtimestamp(sub_res['created_utc']).strftime("%Y-%m-%d %H:%M:%S")
        my_collection.insert_one(dat)
        red_data.append(dat)
    print(red_data)

