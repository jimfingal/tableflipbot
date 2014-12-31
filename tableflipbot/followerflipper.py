from tweepy.streaming import StreamListener
from flipper import get_flipped_string
import logging

class FollowFlipper(StreamListener):

    def on_event(self, status):

        try:
            string_to_flip = ""
            source_user = ""

            if status.event ==  "list_member_added":
                string_to_flip = status._json["target_object"]["name"]
                source_user = status._json["source"]["screen_name"]
            elif status.event ==   "follow":
                string_to_flip = status._json["source"]["screen_name"]
                source_user = string_to_flip

            if string_to_flip:
                print "Flipping: %s" % string_to_flip
                flipped = get_flipped_string(string_to_flip.decode('utf-8'))

                print "Flipped text (%s) to: %s" % (string_to_flip, flipped.decode('utf-8'))

                status_out = ". @" + source_user + " ::\n" + flipped.decode('utf-8')

                self.api.update_status(status_out)
        except Exception as e:
            logging.exception(e)