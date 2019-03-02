import random
import string
from Liklihood_Detectors import List_Of_Detectors

import Core_ConfigInterpreter as cc
import Core_Logger

'''
A class that is used to build a knowledge base on a likelihood.
'''
class Individual:

    # The constructor, setting class variables for each individual
    def __init__(self, text=[], name=None, impact=cc.Config().get_default_impact("core_config.json")):
        # A score of this individuals liklihood
        self._liklihood = None
        # Name of the individual
        self.name = name
        # A list used to hold the text that will be profiled
        self._text_to_be_profiled = []

        self.add_text_to_be_profiled(text)

        # Sets the impact of the individual, default is 1
        self.impact = impact

    def get_liklihood(self):
        assert self._liklihood is not None, " Liklihood has not been set."
        return self._liklihood

    # A method used to add text to the aformentioned list
    def add_text_to_be_profiled(self, text):

        if type(text) is list:
            self._text_to_be_profiled.extend(text)
        else:
            self._text_to_be_profiled.append(text)

    # A method used to remove text from the aformentioned list
    def remove_from__text_to_be_profiled(self, text):
        self._text_to_be_profiled.remove(text)

    # A method that generates a psudo random name for the individual
    def generate_name(self, length=9):
        new_name = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        Core_Logger.log("New name set to: " + new_name)
        self.name = new_name

    # Uses the detectors to calculate a risk score for the individual
    def profile(self):
        # The below was removed so that we don't crash during a run.
        #assert self._text_to_be_profiled, "List of text to be profiled is empty"

        list_of_detectors = List_Of_Detectors.list_of_detectors

        total_scores = []
        total = 0

        list_of_extra_info = []
        # Loops through all of the detectors

        # I have no idea why this tmp is needed (maybe a pointer problem) but everything breaks without it.
        tmp_text = self._text_to_be_profiled

        #Sets a list to be equal to the detectors set in the config.
        list_of_detectors_in_config = cc.Config().get_list_of_in_use_detectors("core_config.json")
        for detector in list_of_detectors:
            #Only runs the detectors that are set in the config
            if detector.detector_name in list_of_detectors_in_config:
                Core_Logger.log(detector.detector_name.capitalize() + " detector run ")
                # Removes null items in list
                self._text_to_be_profiled = filter(None, self._text_to_be_profiled)

                self._text_to_be_profiled = tmp_text
                # Loops through the list of text to be profiled, profiling each, and then calculating an average
                for text in self._text_to_be_profiled:
                    if text:
                        dictionary_of_scan_results = detector.get_score(text)
                        list_of_extra_info.append(dictionary_of_scan_results)

                        # Checks if the likelihood field exists and if so uses it towards the total.
                        if "likelihood" in dictionary_of_scan_results.keys():
                            total_scores.append(dictionary_of_scan_results["likelihood"])
            else:
                Core_Logger.log(detector.detector_name.capitalize() + " detector not run ")

        for number in total_scores:
            total = total + number

        if total > 0:
            average = total / len(total_scores)
            self._liklihood = average
        else:
            self._liklihood = 0

        #Checks if the likelihood for an individual exists as this will define if any tweets were profiled.
        if self._liklihood:
            assert self.impact, "No impact set to the individual."
            assert self._liklihood, "No likelihood set for the individual."
            assert self.name, "No name set for the individual."

            # Adds items to a dictionary so that they can be returned to the main script
            # The round function sets the decimal place to 2.
            dictionary_for_individual = {}
            dictionary_for_individual["likelihood"] = round(self._liklihood, 2)
            dictionary_for_individual["impact"] = round(self.impact, 2)
            dictionary_for_individual["extra"] = list_of_extra_info
            dictionary_for_individual["name"] = self.name
            dictionary_for_individual["risk"] = round(self.impact * self._liklihood, 2)
        else:
            dictionary_for_individual = {}
            dictionary_for_individual["likelihood"] = None
            dictionary_for_individual["impact"] = None
            dictionary_for_individual["extra"] = list_of_extra_info
            dictionary_for_individual["name"] = self.name
            dictionary_for_individual["risk"] = None

        return dictionary_for_individual
