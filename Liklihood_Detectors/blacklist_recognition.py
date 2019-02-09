import datetime
import re
import requests

import Core_ConfigInterpreter as cc
import Core_NLPAnalyser as ca

# This class is uses entity recognition to detect when a blacklisted word is used in a given piece of text.
# This class does not return a likelihood and instead returns an extra of when blacklisted words are used.
class Blacklist_Recognition:
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

    # A method used to find when a blacklist item is mentioned in a given piece of text.
    def get_score(self, text):

        self.text_to_profile = text

        items_to_return = {}
        list_of_keywords = []

        # Loops through the blacklist file appending its values to a list
        blacklist_file = open(r"C:\Users\User\Desktop\Hunch\Liklihood_Detectors\blacklist_recognition_file.txt", "r")
        list_of_blacklist_items = []
        for line in blacklist_file:
            list_of_blacklist_items.append(line)

        for blacklisted_item in list_of_blacklist_items:
            if blacklisted_item.lower().strip() in str(self.text_to_profile).lower().strip():
                items_to_return["Type"] = "BLACKLISTED"
                items_to_return["Keyword"] = blacklisted_item
                items_to_return["Time"] = datetime.datetime.now()
                items_to_return["Text"] = self.text_to_profile
                items_to_return["sentiment"] = self._get_sentiment()[1] #This sets the sentiment of the text (e.g. positive), even though an impact isn't created.
                list_of_keywords.append(items_to_return)


        # Creates a dictionary to return containing the likelihood and additional ifnormation like tags
        return_dictionary = {}
        return_dictionary["extra"] = list_of_keywords

        return return_dictionary