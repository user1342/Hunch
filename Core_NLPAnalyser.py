from NLP_Analysers import Aws_NLPAnalyser as AWSComprehend

'''
This class is used to set a default analyser for all detection files to use
'''


class Core_NLPAnalyser:
    # Returns an analyser object
    def create_analyser(self):
        analyser = AWSComprehend.AWSComprehend()
        return analyser
