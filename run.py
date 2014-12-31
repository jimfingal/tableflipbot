from multiprocessing import Process
import logging

import redis

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

from tableflipbot.followerflipper import FollowFlipper
from tableflipbot.trendflipper import flip_trends

def run_followflipper(config):
    auth = OAuthHandler(config.consumer_key,config. consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    flipper = FollowFlipper(api=API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True))
    stream = Stream(auth, flipper)
    logging.info("Attempting to connect the stream.")
    stream.userstream(_with='user')


def run_trendflipper(config):
    auth = OAuthHandler(config.consumer_key,config. consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    redis_client = redis.from_url(config.redis_url)
    flip_trends(api, redis_client)



if __name__ == "__main__":

    import tableflipbot.config as config

    log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    procs = []
    procs.append(Process(target=run_followflipper, args=(config,)))
    procs.append(Process(target=run_trendflipper, args=(config,)))

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
