import os
import CORE_Collector
import CORE_Individual
import CORE_Display

# Loops through the json folder and creates an individual to profile based off each file.
import CORE_Logger

if __name__ == '__main__':
    json_file_directory = r"Json_Files"

    list_of_profiled_individuals = []

    for filename in os.listdir(json_file_directory):
        my_aggrigator = CORE_Collector.WebsiteToCrawl()
        full_path = os.path.join(json_file_directory, filename)
        my_aggrigator.read_from_json_file(full_path)
        CORE_Logger.log("Created Aggrigator for  " + my_aggrigator.name + ": " + str(my_aggrigator.list_of_dictionary_sources))

        my_individual = CORE_Individual.Individual(my_aggrigator.aggregate_data())
        my_individual.impact = my_aggrigator.impact
        my_individual.name = my_aggrigator.name  # my_individual.generate_name()
        CORE_Logger.log("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        results = my_individual.profile()
        CORE_Logger.log("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
            results["likelihood"]))

        list_of_profiled_individuals.append(results)

    CORE_Display.create_website(list_of_profiled_individuals).generate_page()
