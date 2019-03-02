import Core_ConfigInterpreter as cc
from NLP_Analysers import Aws_NLPAnalyser



list_of_analysers = [Aws_NLPAnalyser.AWSComprehend()]

'''
This class is used to set a default analyser for all detection files to use
'''
class Core_NLPAnalyser:

    # Returns an analyser object
    def create_analyser(self):
        ret_val = None
        config_analyser = cc.Config().get_default_analyser("core_config.json")

        for analyser in list_of_analysers:
            if config_analyser == analyser.analyser_name:
                ret_val = analyser

        return ret_val
