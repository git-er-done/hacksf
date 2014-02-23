

import requests
from requests_oauthlib import OAuth1Session


def search_tweets_geo(term, lat, long, radius, count=100):
    API = "https://api.twitter.com/1.1/search/tweets.json"

    geocode = str(lat) + "," + str(long) + "," + str(radius) + "mi"

    max_results = 100
    search_params = {'q': term,
                     'geocode': geocode,
                     'count': max_results,
                     'result_type': "recent"}

    twitter = OAuth1Session(
        client_key='FtxbhtTGgBWg1dDzfA3Dxw',
        client_secret='Wm3GLrkel1n21vZKvcnKcGuYBxdD1lWluH4w6AkgDRE',
        resource_owner_key='18033637-Rvs7qFxX01OCGeI7LqaI1jkKTLyhz0vWPGSs6fDcV',
        resource_owner_secret='cwjTb107QJv5ci85NRWYKENFFLp4APNHmzsxj5YnlAZj1')

    found = 0
    good_tweets = []

    results = (twitter.get(API, params= search_params )).json()
    nCalls = 1

#    print "just got " + str(len(results['statuses'])) + " more results "

    min_id = float("inf")

    for tweet in results['statuses']:

        if (tweet['id'] < min_id):
            min_id = tweet['id']

        loc = tweet['coordinates']
        if (loc != None):
            if (loc['type']=='Point'):
                found = found + 1
                good_tweets.append({'user': tweet['user']['screen_name'],
                                    'text': tweet['text'],
                                    'geo': loc['coordinates']})

    maxed_out = len(results['statuses']) < max_results

    while (found<count) and (not maxed_out) and nCalls<10:

        search_params['max_id'] = min_id
        print "found " + str(found) + " matches."

        print "performing another api call..."

        results = (twitter.get(API, params=search_params)).json()
        nCalls += 1

        #print "just got " + str(len(results['statuses'])) + " more results "
        maxed_out = len(results['statuses']) < max_results

        for tweet in results['statuses']:

            if (tweet['id'] < min_id):
                min_id = tweet['id']

            loc = tweet['coordinates']
            if (loc != None):
                if (loc['type']=='Point'):
                    found+=1
                    good_tweets.append({'user': tweet['user']['screen_name'],
                                        'text': tweet['text'],
                                        'geo': loc['coordinates']})
        #print min_id

    print str(nCalls) + " calls made to the Twitter API"
    return good_tweets



def search_tweets(term, count=100):
    API = "https://api.twitter.com/1.1/search/tweets.json"
    twitter = OAuth1Session(
        client_key='FtxbhtTGgBWg1dDzfA3Dxw',
        client_secret='Wm3GLrkel1n21vZKvcnKcGuYBxdD1lWluH4w6AkgDRE',
        resource_owner_key='18033637-Rvs7qFxX01OCGeI7LqaI1jkKTLyhz0vWPGSs6fDcV',
        resource_owner_secret='cwjTb107QJv5ci85NRWYKENFFLp4APNHmzsxj5YnlAZj1')
    r = twitter.get(API, params={'q': term, 'count': count})
    return r.json()

def get_tweets_by_user(screen_name, count=200):
    API = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    twitter = OAuth1Session(
        client_key='FtxbhtTGgBWg1dDzfA3Dxw',
        client_secret='Wm3GLrkel1n21vZKvcnKcGuYBxdD1lWluH4w6AkgDRE',
        resource_owner_key='18033637-Rvs7qFxX01OCGeI7LqaI1jkKTLyhz0vWPGSs6fDcV',
        resource_owner_secret='cwjTb107QJv5ci85NRWYKENFFLp4APNHmzsxj5YnlAZj1')
    r = twitter.get(API, params={'screen_name': screen_name, 'count': count})
    return r.json()
