import re
import tweepy

'''
A class used to gather tweets from a specified user
'''
class Twitter_Aggrigator:
    consumer_key = #Add this field
    consumer_secret = #Add this field
    access_token = #Add this field
    access_token_secret = #Add this field
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # The constructor
    def __init__(self):
        self.list_of_tweets = []

    #Takes the last amount of tweets from a users twitter account
    def pull_from_twitter(self, username, number_of_tweets_timeout = 10):

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

            if tweet_count > number_of_tweets_timeout:
                break

        return self.list_of_tweets