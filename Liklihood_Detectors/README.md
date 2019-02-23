# Profiling The Likelihood from a given piece of text
The purpose of a liklihood detector is to take a given piece of text and implement a methadology that will return a likelihood as well as additional information - for example a detector that looks at how often someone referes to close relationships will use NLP to recognise when a relationship is mentioned and base a likelihood off that. The below documents the three step process for creating a Hunch Likelihood Detector. 

## 1 - Follow The Template
A detector will take the form of a python file in the "Likelihood_Detectors" folder. Inside of this file will be a class that contains five main parts, these are stated below.

### 1.1 - The Name Variable
Your detector class must include a name, this is what will be used inside of the config so that the user can define that they want to run your detector. Best practice is to have this variable at the top of your detector's class such as:

```python
detector_name = "blacklist"
```
### 1.2 - The get_score Function
All liklihood detectors must have a 'get_score' function. While not all liklihood detectors need to return a likihood score, detailed in the 'returning a liklihood score' section it is important that all detectors have this function inside of their class. This function is the entry point for all detectors. This function takes a 'text' paramiter, this is the text that is to be profiled. For example:

```python
def get_score(self, text):
```
### 1.3 - Setting a Likelihood
If you are planning on returning a likelihood then your detector will need to use the priorities set in the configuration file. This stops every detector from using their own priority system. To do this decide what would depict a high, medium, and low likelihood and use the code below to set the individuals likelihood. 

```python
    import Core_ConfigInterpreter as cc

    scores = {"HIGH": cc.Config().get_score_high("core_config.json"),
              "MEDIUM": cc.Config().get_score_medium("core_config.json"),
              "LOW": cc.Config().get_score_low("core_config.json")
              }
              
    liklihood = scores["HIGH"]
    liklihood = scores["MEDIUM"]
    liklihood = scores["LOW"]
```
### 1.4 - Natural Language Processing
One of the strengths of Hunch is it's integration with Natural Language Processing (NLP) - for example a relationship detector would use NLP entity recogniion to identify when a relationship was mentioned, or a location detector would use NLP to identify when locations were mentioned. Not all detectors are required to use NLP, however, if they do you should use the Core_NLPAnalyser.py file. For example:

 ```python
core_nlp = ca.Core_NLPAnalyser()
profiler = core_nlp.create_analyser()
json_response = self.profiler.construct_detect_command("detect-entities", self.text_to_profile)
```
The two options for the construct_detect_command are "detect-sentiment", and "detect-entities". This core_nlp analyser is set up so that multiple analysers can be created. Currently there is only an AWS Comprehend analyser and so the functions depict that. 

"detect-entities" returns a json string of which looks as follows:
 ```json
{"Entities": [{"Text": "@jenstatsky",
               "Type": "PERSON"}]}
```

While "detect-sentiment" returns:
 ```json
{  
   "Sentiment":"NEGATIVE"
}
```

### 1.5 - Returning a JSON Response
All Detectors must return a JSON string. This JSON response has two main entities. The first of these being the likelihood, which should have been previously set, and secondly the 'extra' field. The extra field contains information that will be displayed to the user. This including the actual 'text' that was profiled, the 'keyword' in the text that flagged the liklihood increasing, the time and date, the 'type' or category of the detector, and the sentiment of the text. Neither the 'likelihood' or the 'extra' fields are mandatory.

```json
{"extra": [{"Keyword": "Mars",
            "Text": "Calling all marshmallows— come visit me on the set of Veronica Mars and get an inside look into Mars...",
            "Time": "2019",
            "Type": "LOCATION",
            "sentiment": "neutral"}],
 "likelihood": 5}
 ```

## 2 -The List Of Detectors
Once you have created your likelihood detector you will need to add it to the 'List_Of_Detectors.py', this can be done by importing your detector in the file and then adding it to the list of detectors. For example

 ```python
from Liklihood_Detectors import Relationship_Detection as rd
from Liklihood_Detectors import Goal_Detection as gd
from Liklihood_Detectors import Location_Detection as ld
from Liklihood_Detectors import url_recognition as ur
from Liklihood_Detectors import blacklist_recognition as br

list_of_detectors = [rd.Relationship_Detection(),
                     gd.Goal_Detection(),
                     ld.Location_Detection(),
                     ur.Url_Recognition(),
                     br.Blacklist_Recognition()]
 ```
 
 ## 3 - The Hunch Configuration
 The final step is where the user will need to add the detectors name into their configuration file, this is so that Hunch knows to run your detector. An example:
 
 ```json
 {
  "config": {
    "default_analyser": "comprehend",
    "aggregators": ["twitter","reddit","instagram","tumblr","http"],
    "detectors": ["blacklist","goal","location","relationship","url"],
 ```
