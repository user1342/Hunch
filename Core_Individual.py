import random

'''
A class that is used to build a knowledge base on a likelihood.
'''
class Individual:

    #The constructor, setting class variables for each individual
    def __init__(self, text = []):
        # A score of this individuals liklihood
        self._liklihood = None
        # Name of the individual
        self.name = ""
        # A list used to hold the text that will be profiled
        self._text_to_be_profiled = []

        self.add_text_to_be_profiled(text)

        self.impact = None



    def get_liklihood(self):
        assert self._liklihood is not None, " Liklihood has not been set."
        return self._liklihood

    #A method used to add text to the aformentioned list
    def add_text_to_be_profiled(self,text):

        if type(text) is list:
            self._text_to_be_profiled.extend(text)
        else:
            self._text_to_be_profiled.append(text)

    #A method used to remove text from the aformentioned list
    def remove_from__text_to_be_profiled(self,text):
        self._text_to_be_profiled.remove(text)

    # A method that generates a psudo random name for the individual
    def generate_name(self, filename = "Core_wordfile", words_in_name = 3):
        list_of_words = []

        file = open(filename, "r")
        for line in file:
            list_of_words.append(line.strip("\n"))

        for iterator in range(words_in_name):
            random_number = random.randint(0, len(list_of_words))
            self.name = self.name + list_of_words[random_number-1]+"//"

    #Uses the detectors to calculate a risk score for the individual
    def profile(self):
        assert self._text_to_be_profiled, "List of text to be profiled is empty"

        list_of_detectors = []

        # Adds the Relationship Detector to be used when profiling
        from Liklihood_Detectors import Relationship_Detection as rd
        relationship_profile = rd.Relationship_Detection()
        list_of_detectors.append(relationship_profile)

        # Adds the goal detector to be used when profiling
        from Liklihood_Detectors import Goal_Detection as gd
        goal_profile = gd.Goal_Detection()
        list_of_detectors.append(goal_profile)

        total_scores = []
        total = 0

        list_of_extra_info = []
        # Loops through all of the detectors
        for detector in list_of_detectors:

            #Removes null items in list
            self._text_to_be_profiled = filter(None, self._text_to_be_profiled)

            #Loops through the list of text to be profiled, profiling each, and then calculating an average
            for text in self._text_to_be_profiled:

                dictionary_of_scan_results = detector.get_score(text)
                list_of_extra_info.append(dictionary_of_scan_results)
                total_scores.append(dictionary_of_scan_results["likelihood"])


        for number in total_scores:
            total = total + number
        average = total / len(total_scores)
        self._liklihood = average


        dictionary_for_individual = {}
        dictionary_for_individual["likelihood"] = self._liklihood
        dictionary_for_individual["extra"]=list_of_extra_info
        return dictionary_for_individual

