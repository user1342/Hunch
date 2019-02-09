import datetime
import re
import requests

import Core_ConfigInterpreter as cc
import Core_NLPAnalyser as ca

# This class is uses entity recognition to detect when a url is used in a given piece of text.
# This class does not return a likelihood and instead returns an extra of when urls are used.
class Url_Recognition:
    # sets the profiler object to be the default analyser set in the Core_NLPAnalyser file
    core_nlp = ca.Core_NLPAnalyser()
    profiler = core_nlp.create_analyser()

    scores = {"HIGH": cc.Config().get_score_high("core_config.json"),
              "MEDIUM": cc.Config().get_score_medium("core_config.json"),
              "LOW": cc.Config().get_score_low("core_config.json")
              }

    # The constructor, setting class variables
    def __init__(self):
        self.text_to_profile = ""

    # A method to retrive the sentiment for the profiled text
    def _get_sentiment(self):
        json_response = self.profiler.construct_detect_command("detect-sentiment", self.text_to_profile)
        sentiment = json_response["Sentiment"].lower()

        # Sets a higher liklihood on the more negative the text is.
        if sentiment == "negative":
            retval = self.scores["HIGH"]
        elif sentiment == "neurural" or sentiment == "mixed":
            retval = self.scores["MEDIUM"]
        else:
            retval = self.scores["MEDIUM"]

        return retval, sentiment

    # A method used to find when a url is mentioned in a given piece of text.
    def get_score(self, text):

        self.text_to_profile = text

        items_to_return = {}
        list_of_keywords = []
        regex = re.search(r'(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', self.text_to_profile)
        if regex:

            # Gets the url behind any shortlinks
            url = regex.group(0)
            url = requests.get(url)
            url = url.url

            #Checks if the url is for twitter as these are normally links to the tweets.
            if str(url).startswith("https://twitter.com") == False:
                items_to_return["Type"] = "URL"
                items_to_return["Keyword"] = url
                items_to_return["Time"] = datetime.datetime.now()
                items_to_return["Text"] = self.text_to_profile
                items_to_return["sentiment"] = self._get_sentiment()[1] #This sets the sentiment of the text (e.g. positive), even though an impact isn't created.
                list_of_keywords.append(items_to_return)


        # Creates a dictionary to return containing the likelihood and additional ifnormation like tags
        return_dictionary = {}
        return_dictionary["extra"] = list_of_keywords

        return return_dictionary