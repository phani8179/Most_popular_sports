import matplotlib
matplotlib.use('Agg')
import requests
import pandas as pd
import datetime
from datetime import datetime
from flask import Flask,render_template,request
import pymongo
import requests
from database import *
import matplotlib.pyplot as plt
from io import StringIO,BytesIO
import base64
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json

app = Flask(__name__)
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/reddit_subscribers')
def reddit_subs():
    sub_data=get_reddit_subscribers()
    labels = sub_data.keys()
    values = sub_data.values()
    return render_template('line.html', title=' total subscribers from reddit for all sports', max=max(values),
                               labels=sub_data.keys(),
                               values=sub_data.values())
    """
    x, y = zip(*sub_data)
    plt.bar(x,y)
    plt.xlabel('sport')
    plt.ylabel('subscribers')
    plt.savefig('img.png')
    return render_template('subscribers.html', name = 'new_plot', url ='/Users/saiphanindramutya/Desktop/Data_science/img.png')
    """

@app.route('/data_by_date', methods=['GET', 'POST'])
def date_wise_data():
    if request.method == 'POST':
        source = request.form['source']
        from_date = request.form['from']
        to_date = request.form['to']
        if len(from_date) == 0 or len(to_date) == 0:
            error = 'Please enter start and end dates'
            return render_template('date.html', error=error)
        else:
            if str(source) == 'reddit':
                upvote,score=get_reddit_votes(from_date,to_date)
                labels = upvote.keys()
                values = upvote.values()
                return render_template('line.html', title=' average upvote ratio from reddit by date', max=max(values),
                               labels=upvote.keys(),
                               values=upvote.values())
            if str(source) == 'twitter':
                date_values=get_twitter_data(from_date,to_date)
                labels = []
                values=[]
                for i in date_values:
                    labels.append(i['_id'])
                for j in date_values:
                    values.append(j['count'])
                return render_template('line.html', title=' tweets count date by date', max=max(values),
                               labels=labels,
                               values=values)
    return render_template('date.html')

if __name__ == '__main__':
    app.run(debug=True)