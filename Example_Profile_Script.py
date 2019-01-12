import os

import Core_Aggregator
import Core_Individual

#Loops through the json folder and creates an individual to profile based off each file.
json_file_directory =r"Json_Files"
for filename in os.listdir(json_file_directory):

    ######################
    ## Build Aggregator ##
    ######################
    # Takes a list of wbebsites and handles from a json file and takes data from those websites for those users.
    my_aggrigator = Core_Aggregator.WebsiteToCrawl()
    full_path = os.path.join(json_file_directory,filename)
    my_aggrigator.read_from_json_file(full_path)

    print("Created aggrigator for: " + str(my_aggrigator.handles) + " and " + str(my_aggrigator.website_names))
    #my_aggrigator.add_to_handles_list("_JamesStevenson")
    #my_aggrigator.add_to_website_list("twitter")
    data_from_individual = my_aggrigator.aggregate_data()
    print("Completed aggrigating data sources for individual " + my_aggrigator.name)

    ######################
    ## Build Individual ##
    ######################
    # Takes the previously sampled text and uses it to profile the indivdual with the detectors
    my_individual = Core_Individual.Individual()
    my_individual.name = my_aggrigator.name
    #my_individual.generate_name()
    # my_individual.add_text_to_be_profiled("Today has been a great day at IBM")
    for text in data_from_individual:
        my_individual.add_text_to_be_profiled(text)
    print("Starting profiling ", len(my_individual._text_to_be_profiled), "samples.")
    score = my_individual.profile()

    print("The individual " + my_individual.name + " has the liklihood of " + str(score))
