import json

'''
A class used to define which aggregation sources will be used to gather text from individuals
as well as what handles / account names will be gathered. 
'''
class WebsiteToCrawl:

    # The default constructor
    def __init__(self):
        self.website_names = []

        self.handles = []

        self.list_of_text = []

        self.name = ""

        self.impact = 0

    #This is used to add items to the website list and make sure that there are no duplicates
    def add_to_website_list(self, website):

        #Checks if its not a list and if so makes it a list of 1
        if type(website) is not list:
            website = [website]

        try:
            self.website_names.extend(website)
        except:
            self.website_names.append(website)
        self.website_names = list(set(self.website_names))

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

                    if attribute == "websites":
                        self.add_to_website_list(nested_value)
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
        assert self.website_names is not None, " No websites listed"
        assert self.list_of_text is not None, "No hndles listed"

        #Loops through the requested websites
        for website in self.website_names:
            website = website.lower()

            #Checks what aggrigator to use based on the website chosen
            if website == "twitter":
                from Data_Source_Aggregators import Twitter_Aggrigator as tw

                aggrigator = tw.Twitter_Aggrigator()

                #Loops through each of the handles for each of the websites
                for user in self.handles:
                    response = aggrigator.pull_from_twitter(user)
                    try:
                        self.list_of_text.extend(response)
                    except:
                        self.list_of_text.append(response)

            elif website == "reddit":
                pass

            else:
                raise Exception("Unknown Website " + website)

        return self.list_of_text
