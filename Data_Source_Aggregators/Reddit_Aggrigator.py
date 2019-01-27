import re
import praw

import Core_ConfigInterpreter as cc

'''
A class used to gather information from the reddit API.
'''
class Reddit_Aggrigator:
    reddit_api = praw.Reddit(client_id=cc.Config().get_reddit_client_id("core_config.json"),
                             client_secret=cc.Config().get_reddit_client_secret("core_config.json"),
                             username=cc.Config().get_reddit_username("core_config.json"),
                             password=cc.Config().get_reddit_password("core_config.json"),
                             user_agent=cc.Config().get_reddit_user_agent("core_config.json"))

    # The constructor
    def __init__(self):
        self.list_of_comments = []

    # A method used to specify the user that's comments will be gathered.
    def pull_from_reddit(self, username =""):
        user = self.reddit_api.redditor(username)

        for comment in user.comments.new():
            comment = re.sub('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', comment.body)
            comment = re.sub('\\n\\n.+', '',comment)

            self.list_of_comments.append(comment)

        return self.list_of_comments[1:cc.Config().get_default_aggregations("core_config.json")+1]