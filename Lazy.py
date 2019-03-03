import json
import os

import CORE_Collector
import CORE_Display
import CORE_Individual
import CORE_Logger

'''
This class has been created as a more user friendly version of the hunch scripts. 
This allows for the exact same functioanlity, however, is used differently. 
'''
class lazy_profile:

    # The Constructor function
    def __init__(self):
        self.list_of_profiled_individuals = []

    # This function takes in a list of dictionaries to aggregate, a name, and an impact,
    def profile(self, list_of_dictionarys_to_aggregate, name, impact):
        my_collector = CORE_Collector.WebsiteToCrawl(list_of_dictionarys_to_aggregate, name, impact)

        CORE_Logger.log(
            "\n\nCreated Collector for  " + my_collector.name + ": " + str(my_collector.list_of_dictionary_sources))

        my_individual = CORE_Individual.Individual(my_collector.aggregate_data())
        my_individual.impact = my_collector.impact
        my_individual.name = my_collector.name  # my_individual.generate_name()
        CORE_Logger.log("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        results = my_individual.profile()
        CORE_Logger.log("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
            results["likelihood"]))

        self.list_of_profiled_individuals.append(results)

    # A function that will create a temp file to profile a given piece of json
    def profile_json_string(self,json_file_folder,json_to_profile):

        individual_name = json_to_profile["individual"]["name"]
        full_path = os.path.join(json_file_folder, individual_name+".json")

        CORE_Logger.log("Making temp JSON file at: "+full_path)

        new_json_file = open(full_path, "w")
        json.dump(json_to_profile,new_json_file)
        new_json_file.close()

        my_collector = CORE_Collector.WebsiteToCrawl()
        my_collector.read_from_json_file(full_path)

        my_individual = CORE_Individual.Individual(my_collector.aggregate_data(), my_collector.name, my_collector.impact)

        CORE_Logger.log("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        results = my_individual.profile()
        CORE_Logger.log("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
            results["likelihood"]))

        os.remove(full_path)
        CORE_Logger.log("Deleted temp JSON file at: " + full_path)

        self.list_of_profiled_individuals.append(results)
        return results


    # This function takes all of the lists of individuals to profile that have been created using the profile function and displays them in the web views
    def display_webpage(self):
        assert len(self.list_of_profiled_individuals) > 0, "List of indivduals empty"

        CORE_Display.create_website(self.list_of_profiled_individuals).generate_page()
