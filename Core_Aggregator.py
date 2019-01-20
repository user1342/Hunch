import json

'''
A class used to define which aggregation sources will be used to gather text from individuals
as well as what handles / account names will be gathered. 
'''
class WebsiteToCrawl:

    # The default constructor
    def __init__(self, list_of_dict_sources = [],new_name="", new_impact =0):
        self.list_of_text = []
        self.name = ""
        self.impact = 0
        self.list_of_dictionary_sources = []

        self.list_of_dictionary_sources = list_of_dict_sources
        self.name = new_name
        self.impact = new_impact

    #This is used to add items to the handles list and make sure that there are no duplicates
    def add_to_handles_list(self, handles):

        #Checks if its not a list and if so makes it a list of 1
        if type(handles) is not list:
            handles = [handles]

        try:
            self.handles.extend(handles)
        except:
            self.handles.append(handles)
        self.handles = list(set(self.handles))

    #This file takes a file location as an input and reads that file as json and adds the contents to the necessary fields.
    def read_from_json_file(self, file_path):

        with open(file_path) as json_file:
            json_input = json.load(json_file)

            for key in json_input:
                value = json_input[key]

                for attribute in value:
                    nested_value = value[attribute]

                    if attribute == "sources":
                        for source in nested_value:
                            self.list_of_dictionary_sources.append({source:nested_value[source]})
                    elif attribute == "handles":
                        self.add_to_handles_list(nested_value)
                    elif attribute == "name":
                        self.name = nested_value
                    elif attribute == "impact":
                        self.impact = nested_value
                    else:
                        raise Exception("Json in incorrect form for profiling.")


    # This function checks what websites have been requested to profile users and what
    # user accounts are to be profiled on the websites.
    def aggregate_data(self):
        assert self.list_of_dictionary_sources is not None, " No sources listed"

        #Loops through the sources using the defined handle for each defined website
        for source_dictionary in self.list_of_dictionary_sources:
            for key in source_dictionary:

                #Sets a user variable to be equal to the entry for the key, of which will be the source website.
                user = source_dictionary[key]

                #Checks what website the key is specifiying to use and then profiled that website using the individual user requested.
                if key == "twitter":
                    from Data_Source_Aggregators import Twitter_Aggrigator as tw

                    aggrigator = tw.Twitter_Aggrigator()

                    response = aggrigator.pull_from_twitter(user)
                    try:
                        self.list_of_text.extend(response)
                    except:
                        self.list_of_text.append(response)

                elif key == "reddit":
                    from Data_Source_Aggregators import Reddit_Aggrigator as ra

                    aggrigator = ra.Reddit_Aggrigator()

                    response = aggrigator.pull_from_reddit(user)

                    try:
                        self.list_of_text.extend(response)
                    except:
                        self.list_of_text.append(response)

                elif "http" in key:
                    from Data_Source_Aggregators import Generic_Aggrigator as ga

                    aggrigator = ga.Generic_Aggrigator()

                    response = aggrigator.scrape_website(key,user)

                    try:
                        self.list_of_text.extend(response)
                    except:
                        self.list_of_text.append(response)

                else:
                    raise Exception("Unknown Website " + key)

        return self.list_of_text
