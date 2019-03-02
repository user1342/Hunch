import Core_Aggregator
import Core_Display
import Core_Individual
import Core_ConfigInterpreter as cc
import Core_Logger

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
        my_aggrigator = Core_Aggregator.WebsiteToCrawl(list_of_dictionarys_to_aggregate, name, impact)

        Core_Logger.log(
            "\n\nCreated Aggrigator for  " + my_aggrigator.name + ": " + str(my_aggrigator.list_of_dictionary_sources))

        my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data())
        my_individual.impact = my_aggrigator.impact
        my_individual.name = my_aggrigator.name  # my_individual.generate_name()
        Core_Logger.log("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        results = my_individual.profile()
        Core_Logger.log("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
            results["likelihood"]))

        self.list_of_profiled_individuals.append(results)

    # This function takes all of the lists of individuals to profile that have been created using the profile function and displays them in the web views
    def display_webpage(self):
        assert len(self.list_of_profiled_individuals) > 0, "List of indivduals empty"

        Core_Display.create_website(self.list_of_profiled_individuals).generate_page()
