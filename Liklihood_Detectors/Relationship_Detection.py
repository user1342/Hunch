#A detector class must have a 'get_score' function that returns a number..
import datetime

import Core_NLPAnalyser as ca

'''
A Class used to calculate a liklihood based off known relationships. 

                        Text Contains Relationships
                            |               |
                            No              Yes
                            v               v 
                            0           Text contains a 
                                        negative sentiment?
                                            |           |
                                            No          Yes
                                            v           V
                                            0           2

'''
class Relationship_Detection:
    #sets the profiler object to be the default analyser set in the Core_NLPAnalyser file
    core_nlp = ca.Core_NLPAnalyser()
    profiler = core_nlp.create_analyser()

    #A dictionary that is used for the level of liklihood
    scores = {"HIGH": 10, "MEDIUM": 5, "LOW": 0, "NONE": 0}

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
            retval = self.scores["LOW"]

        return retval, sentiment

    # A method used to find if any individuals or organisations have been mentioned in the sample text.
    def get_score(self, text):

        self.text_to_profile = text

        ret_val = self.scores["MEDIUM"] #This is set to medium as the individual has no reference to close relationships (in the text).

        json_response = self.profiler.construct_detect_command("detect-entities", self.text_to_profile)

        list_of_entities = ["PERSON","ORGANIZATION"]

        dictionary_of_items = {}
        items_to_return = {}
        list_of_keywords = []

        for key in json_response:
            value = json_response[key]

            for attribute in value:
                Text = attribute['Text']
                Type = attribute['Type']

                dictionary_of_items[Type] = Text
            #Checks if the text has a tag for Person or Organisation if not returns as none
            for item in dictionary_of_items:
                if item in list_of_entities:
                    ret_val, sentiment = self._get_sentiment()

                    items_to_return["Type"] = item
                    items_to_return["Keyword"] = dictionary_of_items[item]
                    items_to_return["Time"] = datetime.datetime.now()
                    items_to_return["Text"] = self.text_to_profile
                    items_to_return["sentiment"] = sentiment
                    list_of_keywords.append(items_to_return)

                    break

        #Creates a dictionary to return containing the likelihood and additional ifnormation like tags
        return_dictionary = {}
        return_dictionary["likelihood"] = ret_val
        return_dictionary["extra"] = list_of_keywords


        return return_dictionary