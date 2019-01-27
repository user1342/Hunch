import Core_ConfigInterpreter as cc


'''
This class is used to set a default analyser for all detection files to use
'''


class Core_NLPAnalyser:
    # Returns an analyser object
    def create_analyser(self):
        analyser = cc.Config().get_default_analyser("core_config.json")
        return analyser
