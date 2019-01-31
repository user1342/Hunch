import Core_Aggregator
import Core_Display
import Core_Individual

class lazy_profile:

    def __init__(self):
        self.list_of_profiled_individuals = []

    def profile (self, list_of_dictionarys_to_aggregate, name, impact):

        my_aggrigator = Core_Aggregator.WebsiteToCrawl(list_of_dictionarys_to_aggregate, name, impact)

        print(
            "\n\nCreated Aggrigator for  " + my_aggrigator.name + ": " + str(my_aggrigator.list_of_dictionary_sources))

        my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data())
        my_individual.impact = my_aggrigator.impact
        my_individual.name = my_aggrigator.name  # my_individual.generate_name()
        print("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        results = my_individual.profile()
        print("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
            results["likelihood"]))

        self.list_of_profiled_individuals.append(results)

    def display_webpage(self):
        assert len(self.list_of_profiled_individuals) > 0, "List of indivduals empty"

        Core_Display.create_website(self.list_of_profiled_individuals).generate_page()

