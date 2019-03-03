import re
import praw

import CORE_ConfigInterpreter as cc

'''
A class used to gather information from the reddit API.
'''
class Reddit_Collector:
    reddit_api = praw.Reddit(client_id=cc.Config().get_reddit_client_id("core_config.json"),
                             client_secret=cc.Config().get_reddit_client_secret("core_config.json"),
                             username=cc.Config().get_reddit_username("core_config.json"),
                             password=cc.Config().get_reddit_password("core_config.json"),
                             user_agent=cc.Config().get_reddit_user_agent("core_config.json"))

    # A method used to specify the user that's comments will be gathered.
    def pull(self, username =""):
        list_of_comments = []
        user = self.reddit_api.redditor(username)

        for comment in user.comments.new():
            #comment = re.sub('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', comment.body)
            comment = re.sub('\\n\\n.+', '',comment.body)

            character_limit = cc.Config().get_aggrigat_character_limit("core_config.json")
            list_of_comments.append(comment[0:character_limit])

        return list_of_comments[1:cc.Config().get_default_aggregations("core_config.json")+1]