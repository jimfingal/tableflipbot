from tweepy.streaming import StreamListener
from flipper import get_flipped_string
import logging
from .config import app_screen_name

def valid_flip_target(string_to_flip, source_user):
    return string_to_flip and source_user.lower() != app_screen_name and \
                string_to_flip.lower() != app_screen_name

class FollowFlipper(StreamListener):

    def on_event(self, status):

        try:
            string_to_flip = None
            source_user = ""

            if status.event ==  "list_member_added":
                logging.info("Got list member added event")
                string_to_flip = status._json["target_object"]["name"]
                source_user = status._json["source"]["screen_name"]
            elif status.event ==  "follow":
                logging.info("Got Follow event event")
                string_to_flip = status._json["source"]["screen_name"]
                source_user = string_to_flip

            if valid_flip_target(string_to_flip, source_user):           

                logging.info("Flipping: %s" % string_to_flip)
                flipped = get_flipped_string(string_to_flip.decode('utf-8'))

                logging.info("Flipped text (%s) to: %s" % (string_to_flip, flipped.decode('utf-8')))

                status_out = ". @" + source_user + " ::\n" + flipped.decode('utf-8')

                self.api.update_status(status_out)
            else:
                logging.info("Not flipping invalid %s" % string_to_flip)

        except Exception as e:
            logging.exception(e)