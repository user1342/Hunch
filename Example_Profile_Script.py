import os

import Core_Aggregator
import Core_Individual
import Core_Display

#Loops through the json folder and creates an individual to profile based off each file.

if __name__ == '__main__':
    json_file_directory =r"Json_Files"

    list_of_profiled_individuals = []

    for filename in os.listdir(json_file_directory):

        my_aggrigator = Core_Aggregator.WebsiteToCrawl()
        full_path = os.path.join(json_file_directory, filename)
        my_aggrigator.read_from_json_file(full_path)
        print("Created Aggrigator for  "+my_aggrigator.name + ": " + str(my_aggrigator.website_names) + " and " + str(my_aggrigator.handles))

        my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data())
        my_individual.impact = my_aggrigator.impact
        my_individual.name = my_aggrigator.name #my_individual.generate_name()
        print("\nBeginning profiling " + my_individual.name+"'s "+ str(len(my_individual._text_to_be_profiled)) + " samples.")

        name = my_individual.name
        results = my_individual.profile()
        likelihood = results["likelihood"]
        impact = my_individual.impact
        risk = likelihood * impact
        print("Risk "+str(risk)+"| Impact "+str(impact)+"| Likelihood "+str(likelihood))

        list_of_profiled_individuals.append({"name":name,"risk":risk,"likelihood":likelihood,"impact":impact})

    Core_Display.create_website(list_of_profiled_individuals).generate_page()