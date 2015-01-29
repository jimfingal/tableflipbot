from flipper import get_flipped_string
import logging
from .config import app_screen_name

from botutils.stream import RawListener
from botutils.models import SimpleTweet

def valid_flip_target(string_to_flip, source_user):
    return string_to_flip and \
            source_user.lower() != app_screen_name and \
            string_to_flip.lower() != app_screen_name

def get_flipped_status(string_to_flip, source_user):

    logging.info("Flipping: %s" % string_to_flip)
    flipped = get_flipped_string(string_to_flip.decode('utf-8'))

    logging.info("Flipped text (%s) to: %s" % (string_to_flip, flipped.decode('utf-8')))

    status_out = ". @" + source_user + " ::\n" + flipped.decode('utf-8')
    return status_out[:140]


class FollowFlipper(RawListener):

    def on_status(self, raw_status):

        logging.info(raw_status)
        
        status = SimpleTweet(raw_status)
        source_user = status.sender_screen_name

        string_to_flip = status.text
    
        if app_screen_name in string_to_flip:
            index_after_mention = string_to_flip.index(app_screen_name) + len(app_screen_name)
            string_to_flip = string_to_flip[index_after_mention:]
                
        self.update_flipped_status(string_to_flip, source_user)


    def on_event(self, event):

        logging.info(event)

        string_to_flip = None
        source_user = ""

        if event['event'] ==  "list_member_added":
            logging.info("Got list member added event")
            string_to_flip = event["target_object"]["name"]
            source_user = event["source"]["screen_name"]
        elif event['event'] ==  "follow":
            logging.info("Got Follow event event")
            string_to_flip = event["source"]["screen_name"]
            source_user = event["source"]["screen_name"]

        self.update_flipped_status(string_to_flip, source_user)
 

    def update_flipped_status(self, string_to_flip, source_user):

        try:
            if valid_flip_target(string_to_flip, source_user):           
                status_out = get_flipped_status(string_to_flip, source_user)
                self.api.update_status(status_out)
            else:
                logging.info("Not flipping invalid %s" % string_to_flip)
        except Exception as e:
            logging.exception(e)