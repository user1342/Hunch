# A detector class must have a 'get_score' function that returns a number..
import datetime
import time

import Core_ConfigInterpreter as cc

from geopy.geocoders import Nominatim
import urllib.request, json

import Core_NLPAnalyser as ca

'''
A Class used to calculate a liklihood based off known locations. 

                        Text Contains location
                            |               |
                            No              Yes
                            v               v 
                            0           known location for crime
                                            |           |
                                            No          Yes
                                            v           V
                                            0           
                                                What is the sentiment
                                                |               |
                                            Positive        Negative
                                                v               v
                                                1               2
'''


class Location_Detection:
    # sets the profiler object to be the default analyser set in the Core_NLPAnalyser file
    core_nlp = ca.Core_NLPAnalyser()
    profiler = core_nlp.create_analyser()

    # A dictionary that is used for the level of liklihood
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

    # A method used to find if any individuals or organisations have been mentioned in the sample text.
    def get_score(self, text):

        self.text_to_profile = text

        ret_val = self.scores["LOW"]  # This is set to low as the individual has not reference a location.

        json_response = self.profiler.construct_detect_command("detect-entities", self.text_to_profile)

        list_of_entities = ["LOCATION"]

        dictionary_of_items = {}
        items_to_return = {}
        list_of_keywords = []

        for key in json_response:
            value = json_response[key]

            for attribute in value:
                Text = attribute['Text']
                Type = attribute['Type']

                dictionary_of_items[Type] = Text
            # Checks if the text has a tag for Person or Organisation if not returns as none
            for item in dictionary_of_items:
                if item in list_of_entities:

                    # Sets the location to the location triggered by the NLP analyser
                    location = dictionary_of_items[item]
                    geolocator = Nominatim(user_agent="Hunch")
                    location = geolocator.geocode(location)

                    # The UK police api will return an error if it fails to find a location and so we catch the response.
                    try:
                        # Checks in UK Police API
                        request_url = "https://data.police.uk/api/crimes-at-location?lat={0}&lng={1}".format(
                            location.latitude, location.longitude)

                        # Requests the url and loads it as a json
                        with urllib.request.urlopen(request_url) as url:
                            data = json.loads(url.read().decode())
                            current_year = time.strftime("%Y")

                            # Checks if any crimes were returned
                            if data:
                                # Loops through the crimes in the data
                                for key in data:

                                    # Checks if the crime has occured in the past 2 years
                                    if (int(key["month"].split("-")[0]) > int(current_year) - 2):
                                        # Crime occured at location within the past 2 years
                                        ret_val, sentiment = self._get_sentiment()

                                        items_to_return["Type"] = item
                                        items_to_return["Keyword"] = dictionary_of_items[item]
                                        items_to_return["Time"] = datetime.datetime.now()
                                        items_to_return["Text"] = self.text_to_profile
                                        items_to_return["sentiment"] = sentiment
                                        list_of_keywords.append(items_to_return)
                            else:
                                # No crimes picked up for the specified location
                                ret_val = self.scores["LOW"]

                    except:
                        # A location that we cant check (e.g. not in the UK)
                        ret_val, sentiment = self._get_sentiment()

                        items_to_return["Type"] = item
                        items_to_return["Keyword"] = dictionary_of_items[item]
                        items_to_return["Time"] = datetime.datetime.now()
                        items_to_return["Text"] = self.text_to_profile
                        items_to_return["sentiment"] = sentiment
                        list_of_keywords.append(items_to_return)

        # Creates a dictionary to return containing the likelihood and additional ifnormation like tags
        return_dictionary = {}
        return_dictionary["likelihood"] = ret_val
        return_dictionary["extra"] = list_of_keywords

        return return_dictionary
