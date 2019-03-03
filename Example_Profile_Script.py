import os
import CORE_Collector
import CORE_Individual
import CORE_Display
import CORE_Logger

# Loops through the json folder and creates an individual to profile based off each file.
if __name__ == '__main__':
    json_file_directory = r"Json_Files"

    list_of_profiled_individuals = []

    for subdir, dirs, files in os.walk(json_file_directory):
        for filename in files:
            if filename.endswith(".json"):
                my_collector = CORE_Collector.WebsiteToCrawl()
                full_path = os.path.join(subdir, filename)

                my_collector.read_from_json_file(full_path)

                CORE_Logger.log("Profiling JSON file: " + full_path)
                CORE_Logger.log("Created Collector for  " + my_collector.name + ": " + str(my_collector.list_of_dictionary_sources))

                my_individual = CORE_Individual.Individual(my_collector.aggregate_data())
                my_individual.impact = my_collector.impact
                my_individual.name = my_collector.name  # my_individual.generate_name()
                CORE_Logger.log("Beginning profiling " + my_individual.name + "'s " + str(
                    len(my_individual._text_to_be_profiled)) + " samples.")

                results = my_individual.profile()
                CORE_Logger.log("Risk " + str(results["risk"]) + "| Impact " + str(results["impact"]) + "| Likelihood " + str(
                    results["likelihood"]))

                list_of_profiled_individuals.append(results)

    CORE_Display.create_website(list_of_profiled_individuals).generate_page()
