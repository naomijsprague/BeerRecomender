"""
@author: naomi
"""
import requests
from pymongo import MongoClient
from time import sleep
import sys

client = MongoClient()

untappd_user_ratings = client.untappd.ratings

def add_user_ratings(beer_id): #writes to mongo database 
    api = 'https://api.untappd.com/v4/beer/checkins/' + str(beer_id) + '?client_id=MYKEYGOESHERE&client_secret=MYSECRETGOESHERE'
    beer = requests.get(api)
    if beer.ok == False:
        sleep(120)
    guinness = beer.json()
    entry_list = []
    sleep(30) 
    for n in range(25):
        entry_list.append(guinness['response']['checkins']['items'][n]['user']['user_name'])
    for user in entry_list:
        user_beers = {}
        user_name = str(user)
        try:
            user_api_call = 'https://api.untappd.com/v4/user/beers/'+ user_name + '?client_id=MYKEYGOESHERE&client_secret=MYSECRETGOESHERE'
        except Keyboardinterrupt:
            raise
        except:
            print sys.exc_info()[0]
            pass
        sleep(30) 
        user_beer_test = requests.get(user_api_call).json()
        beer_rating_by_user = []
        for n in range(len(user_beer_test['response']['beers']['items'])):
            beer = user_beer_test['response']['beers']['items'][n]['beer']['bid']
            output = user_beer_test['response']['beers']['items'][n]['rating_score']
            beer_rating_by_user.append((str(beer),output))
        new_post = dict(beer_rating_by_user)
        user_beers[user] = new_posts
        print user_beers
        untappd_user_ratings.insert_one(user_beers)

beer_list = [223, 3784, 3811, 3834, 3916, 3942, 4133, 4463, 4467, 4511, 4879,  5210, 5848,  5849, 6274, 6277, 6767, 7146, 7174, 7182, 7203, 7535, 8576, 10759, 10887, 11894, 19855, 24589, 81446, 115170, 150619, 311058, 365698, 388193, 389551, 405035, 470642, 493638, 528918, 557943, 565650, 646626, 690934, 728589, 733099, 922078, 946091, 1029547, 1031081, 1126495]

for beer_id in beer_list:
    try: 
        add_user_ratings(beer_id)
    except Keyboardinterrupt:
        raise
    except:
        print sys.exc_info()[0]
