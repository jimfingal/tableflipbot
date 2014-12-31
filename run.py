from multiprocessing import Process
import logging

import redis

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import tableflipbot.config as config
from tableflipbot.followerflipper import FollowFlipper
from tableflipbot.trendflipper import flip_trends

def run_followflipper():
    auth = OAuthHandler(config.consumer_key,config. consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    flipper = FollowFlipper(api=API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True))
    stream = Stream(auth, flipper)
    logging.info("Attempting to connect the stream.")
    stream.userstream(_with='user')


def run_trendflipper():
    auth = OAuthHandler(config.consumer_key,config. consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    redis_client = redis.from_url(config.redis_url)
    flip_trends(api, redis_client)



if __name__ == "__main__":

    log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    #run_followflipper(config)

    run_trendflipper()

    '''
    stream_proc = Process(target=run_stream_from_config, args=(config,))
    image_proc = Process(target=run_image_processor_from_config, args=(config,))

    stream_proc.start()
    image_proc.start()

    stream_proc.join()
    image_proc.join()
    '''