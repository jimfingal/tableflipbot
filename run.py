from multiprocessing import Process
import logging

import redis

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

from tableflipbot.followerflipper import FollowFlipper
from tableflipbot.trendflipper import flip_trends
from tableflipbot.oxford_wod_flipper import flip_word_of_day

import tableflipbot.config as config

from botutils.stream import run_user_stream

def get_auth(config):
    auth = OAuthHandler(config.consumer_key,config. consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    return auth 

def get_api(auth):
    return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def run_followflipper(config):

    auth = get_auth(config)
    api = get_api(auth)

    flipper = FollowFlipper(api=api)

    '''
    run_user_stream(config.consumer_key, 
                    config.consumer_secret,
                    config.access_token,
                    config.access_token_secret, 
                    flipper)
    '''

    stream = Stream(auth, flipper)

    logging.info("Attempting to connect the stream.")

    stream.userstream(_with='user')

    logging.info("Exiting from stream....")
    

def run_trendflipper(config):

    auth = get_auth(config)
    api = get_api(auth)    
    redis_client = redis.from_url(config.redis_url)

    flip_trends(api, redis_client, config.redis_col)

def run_oedflipper(config):

    auth = get_auth(config)
    api = get_api(auth)
    redis_client = redis.from_url(config.redis_url)

    flip_word_of_day(api, redis_client, config.redis_col)


if __name__ == "__main__":

    log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    procs = []
    procs.append(Process(target=run_followflipper, args=(config,)))
    #procs.append(Process(target=run_trendflipper, args=(config,)))
    procs.append(Process(target=run_oedflipper, args=(config,)))

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()