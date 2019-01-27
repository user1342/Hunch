import re
import tweepy

import Core_ConfigInterpreter as cc

'''
A class used to gather tweets from a specified user
'''


class Twitter_Aggrigator:
    consumer_key = cc.Config().get_twitter_consumer_key("core_config.json")
    consumer_secret = cc.Config().get_twitter_consumer_secret("core_config.json")
    access_token = cc.Config().get_twitter_access_token("core_config.json")
    access_token_secret = cc.Config().get_twitter_access_token_secret("core_config.json")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # The constructor
    def __init__(self):
        self.list_of_tweets = []

    # Takes the last amount of tweets from a users twitter account
    def pull_from_twitter(self, username, number_of_tweets_timeout= cc.Config().get_default_aggregations("core_config.json")):

        item = self.api.get_user(username)

        '''
        print("name: " + item.name)
        print("screen_name: " + item.screen_name)
        print("description: " + item.description)
        print("statuses_count: " + str(item.statuses_count))
        print("friends_count: " + str(item.friends_count))
        print("followers_count: " + str(item.followers_count))
        tweets = item.statuses_count
        account_age_days = delta.days
        account_created_date = item.created_at
        '''

        tweet_count = 0

        for status in tweepy.Cursor(self.api.user_timeline, id=username).items():
            tweet_count += 1
            tweet = status.text
            tweet = re.sub('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', tweet)

            self.list_of_tweets.append(tweet)

            if tweet_count >= number_of_tweets_timeout:
                break

        return self.list_of_tweets
