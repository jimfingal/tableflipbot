import re
import time
import logging

from flipper import get_flipped_string

SLEEP_INTERVAL = 60 * 60 # Once an hour
#SLEEP_INTERVAL = 10

REDIS_COL = 'flipped'


def get_trend_terms(api):
    """Calls the Twitter API and parses out trend names"""
    trends = api.trends_place(id=1)
    trend_words = map(lambda trend: trend['name'],  trends[0]["trends"])
    return trend_words

def get_flipped_trends(api):
    """Returns a flipped trend, and the hashtag to use"""

    trend_terms = get_trend_terms(api)

    for trend in trend_terms:
        try:
            flipped_str = get_flipped_string(unicode(trend).decode('utf-8'))
            hashtag = re.sub('\W+', '', trend).lower()

            yield (flipped_str, hashtag,)
        except UnicodeEncodeError:
            pass


def flip_trends(api, redis_client):

    while True:

        for flipped_trend, hashtag in get_flipped_trends(api):

            if not redis_client.sismember(REDIS_COL, hashtag):
                tweet = "%s  #%s" % (flipped_trend.decode('utf-8'), hashtag.decode('utf-8'))
                api.update_status(tweet)
                redis_client.sadd(REDIS_COL, hashtag)
                break
            else:
                logging.info("%s has already been flipped, skipping" % hashtag)
                continue

        time.sleep(SLEEP_INTERVAL)
