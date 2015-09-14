import requests
from pymongo import MongoClient
from time import sleep
import sys

client = MongoClient()

untappd_user_ratings = client.untappd.ratings

def add_user_ratings(beer_id): #writes to mongo database 
    api = 'https://api.untappd.com/v4/beer/checkins/' + str(beer_id) + '?client_id=B5AEEFAFFDABD21BCEBDB738CED1A245DC895C0F&client_secret=E7192DF6F9FBCC6BA901FE38F98D84B3346B79ED'
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
            user_api_call = 'https://api.untappd.com/v4/user/beers/'+ user_name + '?client_id=B5AEEFAFFDABD21BCEBDB738CED1A245DC895C0F&client_secret=E7192DF6F9FBCC6BA901FE38F98D84B3346B79ED&limit=50'
        except KeyboardInterrupt:
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
        user_beers[user] = new_post
    print user_beers
        untappd_user_ratings.insert_one(user_beers)

beer_list = [223, 3784, 3811, 3834, 3916, 3942, 4133, 4463, 4467, 4511, 4879,  5210, 5848,  5849, 6274, 6277, 6767, 7146, 7174, 7182, 7203, 7535, 8576, 10759, 10887, 11894, 19855, 24589, 81446, 115170, 150619, 311058, 365698, 388193, 389551, 405035, 470642, 493638, 528918, 557943, 565650, 646626, 690934, 728589, 733099, 922078, 946091, 1029547, 1031081, 1126495]
second_beer_list = [5382, 162311, 673549, 5775, 18311, 933141, 1065366, 557976, 293529, 1138202, 3995, 95386, 384798, 384799, 367398, 931114, 1096875, 5037, 61743, 348850, 6451, 249402, 943135, 316, 1128510, 319, 1123265, 1046722, 733509, 3898, 168268, 472782, 57171, 15188, 419534, 1164887, 739673, 890075, 1182941, 14435, 392679, 2025, 39071, 5999, 323826, 1118452, 1067255, 1063032, 184553, 393471]

for beer_id in second_beer_list:
    try: 
        add_user_ratings(beer_id)
    except KeyboardInterrupt:
        raise
    except:
        print sys.exc_info()[0]

