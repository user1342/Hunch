import re
import praw #This requires installing the praw plugin

'''
A class used to gather information from the reddit API.
'''
class Reddit_Aggrigator:
    reddit_api = praw.Reddit(client_id='*', client_secret='*',
                             username='*', password='*',
                             user_agent='*')

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

        return self.list_of_comments[2:12]