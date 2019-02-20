import os
from NLP_Analysers import Aws_NLPAnalyser as AWSComprehend
import json

'''
A class used to check default settings for Hunch as well as settings from a defined config file.
'''
class Config:

    #Default constructor
    def __init__(self):

        # Maybe instead of the dictionary add mini functions for each. The just have them call the dictionary
        self._dictionary_of_config_paramiters = {
            "default_analyser": AWSComprehend.AWSComprehend(),
            "score_high": 10,
            "score_medium": 5,
            "score_low": 0,
            "default_impact": 1,
            "default_aggregations": 10,
            "character_limit":250,

            "reddit_client_id": None,
            "reddit_client_secret" : None,
            "reddit_username" : None,
            "reddit_password" : None,
            "reddit_user_agent" : "Hunch",

            "twitter_consumer_key" : None,
            "twitter_consumer_secret" : None,
            "twitter_access_token" : None,
            "twitter_access_token_secret" : None,

            "blacklisted_strings": []
        }

    #The below functions are used to get api information, such as Twitter and Reddit API keys

    def get_twitter_consumer_key (self, config = None):
        return self._read_paramiter("twitter_consumer_key", config)

    def get_twitter_consumer_secret (self, config = None):
        return self._read_paramiter("twitter_consumer_secret", config)

    def get_twitter_access_token (self, config = None):
        return self._read_paramiter("twitter_access_token", config)

    def get_twitter_access_token_secret (self, config = None):
        return self._read_paramiter("twitter_access_token_secret", config)

    def get_reddit_client_id (self, config = None):
        return self._read_paramiter("reddit_client_id", config)

    def get_reddit_client_secret (self, config = None):
        return self._read_paramiter("reddit_client_secret", config)

    def get_reddit_username (self, config = None):
        return self._read_paramiter("reddit_username", config)

    def get_reddit_password (self, config = None):
        return self._read_paramiter("reddit_password", config)

    def get_reddit_user_agent (self, config = None):
        return self._read_paramiter("reddit_user_agent", config)

    #This is used to retrieve the default amount of items of text that should be aggregate from an aggregator
    def get_default_aggregations (self, config = None):
        return self._read_paramiter("default_aggregations", config)

    #This is used to retrieve credentials used to log into the display
    def get_default_credentials (self, config = None):
        return self._read_paramiter("default_credentials", config)

    #This returns a list of the aggregators that are to be used
    def get_list_of_in_use_aggregators (self, config = None):
        return self._read_paramiter("aggregators", config)

    #This returns a list of the detectors that are to be used.
    def get_list_of_in_use_detectors (self, config = None):
        return self._read_paramiter("detectors", config)

    # This function is used to retrive the default analyser
    def get_default_analyser(self, config = None):
        ret_val = self._read_paramiter("default_analyser", config)

        #Checks if the string comprehend was returned from the json file and if so substitutes it for the correct analyser
        if ret_val == "comprehend":
            ret_val = AWSComprehend.AWSComprehend()

        return ret_val

    #The below functions are used to return a score for low, medium, and high likelihoods.
    def get_score_high(self, config = None):
        return self._read_paramiter("score_high", config)

    def get_score_medium(self, config = None):
        return self._read_paramiter("score_medium", config)

    def get_score_low(self, config = None):
        return self._read_paramiter("score_low", config)

    #This returns the value that should be set for the impact if one isnt set
    def get_default_impact(self, config = None):
        return self._read_paramiter("default_impact", config)

    # A list of strings that are used in the blacklist detector
    def get_blacklisted_strings(self, config = None):
        return self._read_paramiter("blacklisted_strings", config)

    #A limit (characters) on how bit each string from an aggrigator can be.
    def get_aggrigat_character_limit(self, config = None):
        return self._read_paramiter("character_limit", config)

    #Returns the whole config.
    def get_whole_config(self, config_file_location):
        if config_file_location is not None and os.path.isfile(config_file_location) is True:
            with open(config_file_location, 'r') as config_file:
                contents = config_file.read()
            ret_val = contents
        else:
            ret_val = None

        return ret_val


    #Takes a paramiter that should be in the config dictionary
    def _read_paramiter (self, paramiter = None, config_file_location = None):
        assert paramiter, "No paramiter given to Config Interpreter"
        paramiter = paramiter.lower()

        if config_file_location is None or os.path.isfile(config_file_location) is False:
            #print("No file given or file given incorrect, defaulting to default config.")
            ret_val = self._read_default_paramiter(paramiter)
        else:
            ret_val = self._read_from_file(paramiter,config_file_location)

        return ret_val

    #This is called if a valid file for a config is given
    def _read_from_file(self, paramiter, config_file_location):

        try:
            with open(config_file_location) as json_file:
                data = json.load(json_file)
                ret_val = data["config"][paramiter]

        except:
            raise Exception ("Failed to load JSON.")

        return ret_val

    #This is called if no valid config file is given and the defaults are required
    def _read_default_paramiter(self, paramiter):
        return self._dictionary_of_config_paramiters[paramiter]

    # Re qrites a specific paramiter in the config file
    def set_paramiter_in_config_in_file(self, config_file_path, paramiter, value):

        with open(config_file_path, 'r+') as json_file:
            data = json.load(json_file)

            data["config"][paramiter] = value
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

    # Take a string or json and re writes the entire config file
    def set_config_file(self, json_for_file, config_file_path):
        json_for_file = json.loads(json_for_file)
        with open(config_file_path, 'w') as json_file:

            json.dump(json_for_file, json_file, indent=4)
            json_file.truncate()