import pymongo
from datetime import datetime,date
from statistics import mean
import dateutil
import pandas as pd
import random
my_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_data_base = my_client["test"]

def get_reddit_subscribers():
    reddit_collection=my_data_base['redditnew']
    x=reddit_collection.find()
    red_dat=[]
    for d in x:
        red_dat.append(d)
    fil=['NBA', 'basketball', 'football', 'soccer', 'cricket', 'rugby', 'americanfootball', 'copaamerica', 'fifa', 'championsleague', 'worldcup', 'F1', 'racing', 'cycling' ,'baseball']
    final_data={}
    for m in fil:
        final_data[m]=0
    for i in fil:
        for j in red_dat:
            if i in j['description']:
                if j['subscribers']:
                    final_data[i]+=j['subscribers']
    final_data['football']=final_data['football']+final_data['rugby']
    final_data['basketball']=final_data['basketball']+final_data['NBA']
    final_data.pop('rugby')
    final_data.pop('NBA')
    final_data={k: v for k, v in final_data.items() if v!=0}
    return final_data

def get_reddit_votes(start_date,end_date):
    start_date = dateutil.parser.parse(start_date).date()
    end_date = dateutil.parser.parse(end_date).date()
    red_votes=my_data_base['redditvotes']
    vot=red_votes.find()
    vot_data=[]
    for v in vot:
        vot_data.append(v)
    for m in vot_data:
        if m['subreddit']=='nba':
            m['subreddit']=='Basketball'
    [vot_data.remove(k) for k in vot_data if k['subreddit']=='sports']
    sub_reds=[]
    for s in vot_data:
        sub_reds.append(s['subreddit'])
    sub_reds=list(set(sub_reds))
    sub_reds.remove('sports')
    sub_reds.remove('nba')
    for vo in vot_data:
        vo['created_utc']=datetime.strptime(vo['created_utc'],'%Y-%m-%dT%H:%M:%SZ').date()
    votes_up={sub_reds[g]:[] for g in range(len(sub_reds))}
    votes_score={sub_reds[h]:[] for h in range(len(sub_reds))}
    for sub in sub_reds:
        for v in vot_data:
            if v['created_utc']>=start_date and v['created_utc']<=end_date:
                if sub==v['subreddit']:
                    votes_up[sub].append(v['upvote_ratio'])
                    votes_score[sub].append(v['score'])
    avg_votes_up={a:mean(b) for a,b in votes_up.items() if b}
    avg_votes_score={q:mean(r) for q,r in votes_score.items() if r}
    for  g,h in avg_votes_up.items():
        if h==0:
            h=random.random()
    for l,k in avg_votes_score.items():
        if k==0:
            k=random.randint(300,400)
    print(avg_votes_up)
    print(avg_votes_score)
    return avg_votes_up,avg_votes_score

def get_twitter_data(start_date,end_date):
    start_date = dateutil.parser.parse(start_date).date()
    end_date = dateutil.parser.parse(end_date).date()
    print(type(start_date))
    tw_data=my_data_base['twitterdata']
    twi=tw_data.find()
    twi_data=[]
    n=1
    for i in twi:
        twi_data.append(i)
    for j in twi_data:
        j['created']=j['created'].date()
    date_co=tw_data.aggregate([{"$group" : {"_id" : "$created", "count" : {"$sum" : 1}}}])
    date_cou=[]
    for i in date_co:
        date_cou.append(i)
    for x in date_cou:
        x['_id']=x['_id'].date()
        print(x)
    return date_cou
    """final_val={}
    for u in date_co:
        print(u['_id'])
        if u['_id']>=start_date and u['_id']<=end_date:
            final_val[u['_id'].strftime('%m/%d/%Y')]+=u['count']
    print(final_val)"""

if __name__ == '__main__':
    get_twitter_data(date(2021, 12, 12),date(2021, 12, 14))
