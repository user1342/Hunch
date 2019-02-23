import json
import Core_ConfigInterpreter as cc
from Data_Source_Aggregators import List_Of_Aggregators

'''
A class used to define which aggregation sources will be used to gather text from individuals
as well as what handles / account names will be gathered. 
'''


class WebsiteToCrawl:

    # The default constructor
    def __init__(self, list_of_dict_sources=[], new_name="", new_impact= cc.Config().get_default_impact("core_config.json")):
        self.list_of_text = []
        self.name = ""
        self.impact = 0
        self.list_of_dictionary_sources = []

        self.list_of_dictionary_sources = list_of_dict_sources
        self.name = new_name
        self.impact = new_impact

    # This file takes a file location as an input and reads that file as json and adds the contents to the necessary fields.
    def read_from_json_file(self, file_path):

        # This resets the variable for every time a json file is read.
        # This shouldn't be necessary, i'm sure there is something i'm missing.
        self.list_of_dictionary_sources = []
        self.name = []
        self.impact = []

        with open(file_path) as json_file:
            json_input = json.load(json_file)

            for key in json_input:
                value = json_input[key]

                for attribute in value:
                    nested_value = value[attribute]

                    if attribute == "sources":
                        for source in nested_value:
                            self.list_of_dictionary_sources.append(source)
                    elif attribute == "name":
                        self.name = nested_value
                    elif attribute == "impact":
                        self.impact = nested_value
                    else:
                        raise Exception("Json in incorrect form for profiling. " + json_file.name)

    # This function checks what websites have been requested to profile users and what
    # user accounts are to be profiled on the websites.
    def aggregate_data(self):
        assert self.list_of_dictionary_sources is not None, " No sources listed"

        # Loops through the sources using the defined handle for each defined website
        for source_dictionary in self.list_of_dictionary_sources:
            for key in source_dictionary:

                # Sets a user variable to be equal to the entry for the key, of which will be the source website.
                user = source_dictionary[key]

                # Sets a list of aggrigators set in the config
                config_set_aggrigator = cc.Config().get_list_of_in_use_aggregators("core_config.json")
                #Checks if the key is in that list
                if key in config_set_aggrigator:
                    #Checks the website key against the dictionary of aggregators
                    ditionary_of_aggregators = List_Of_Aggregators.dictionary_of_aggrigators

                    try:
                        #Checks the key (e.g. instagram) is in the dictionary and if so sets the value as the aggrigator
                        aggrigator = ditionary_of_aggregators[key]
                        response = aggrigator.pull(user)

                        try:
                            self.list_of_text.extend(response)
                        except:
                            self.list_of_text.append(response)

                    except:
                        raise Exception("Unknown Source " + key)

                else:
                    if cc.Config().get_verbose("core_config.json"): print(user+"'s source " + key + " not set in config")

        return self.list_of_text
