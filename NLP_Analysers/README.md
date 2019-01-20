# Entity Recognition and Sentiment Analysis using NLP
The NLP Analysers are the backbone of this tool. These classes use natural langauge processing to perform entity recognition and sentiment analysis on given items of text. The [Core_NLPAnalyser.py](https://github.com/user1342/Hunch/blob/master/Core_NLPAnalyser.py) stands as a gateway for the likelihood detector classes to use the natural langauge processing functionality. This means that the same NLP Analyser is used across individuals and websites for each run. This means that the specific analyser to be used is set in the Core_NLPAnalyser.py file. 

When making a new NLP Analyser it must take in a **string of text as a paramiter** and must return a json response matching the below (for entity recognition):

```json
{"Entities": [{"BeginOffset": 3,
               "EndOffset": 14,
               "Score": 0.9824379682540894,
               "Text": "@jenstatsky",
               "Type": "PERSON"}]}
```
