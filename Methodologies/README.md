# Profiling The Likelihood from a given piece of text
The purpose of a liklihood methodology is to take a given piece of text and implement a methadology that will return a likelihood as well as additional information - for example a methodology that looks at how often someone referes to close relationships will use NLP to recognise when a relationship is mentioned and base a likelihood off that. The below documents the three step process for creating a Hunch Likelihood Methodology.

## 1 - Follow The Template
A methodology will take the form of a python file in the "Likelihood_Methodologies" folder. Inside of this file will be a class that contains five main parts, these are stated below.

### 1.1 - The Name Variable
Your methodology class must include a name, this is what will be used inside of the config so that the user can define that they want to run your methodology. Best practice is to have this variable at the top of your methodology's class such as:

```python
methodology_name = "blacklist"
```
### 1.2 - The get_score Function
All liklihood Methodologies must have a 'get_score' function. While not all liklihood Methodologies need to return a likihood score, detailed in the 'returning a liklihood score' section it is important that all Methodologies have this function inside of their class. This function is the entry point for all Methodologies. This function takes a 'text' paramiter, this is the text that is to be profiled. For example:

```python
def get_score(self, text):
```
### 1.3 - Setting a Likelihood
If you are planning on returning a likelihood then your methodology will need to use the priorities set in the configuration file. This stops every methodology from using their own priority system. To do this decide what would depict a high, medium, and low likelihood and use the code below to set the individuals likelihood.

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
One of the strengths of Hunch is it's integration with Natural Language Processing (NLP) - for example a relationship methodology would use NLP entity recogniion to identify when a relationship was mentioned, or a location methodology would use NLP to identify when locations were mentioned. Not all Methodologies are required to use NLP, however, if they do you should use the Core_NLPAnalyser.py file. For example:

 ```python
 import Core_NLPAnalyser as ca
 
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
All Methodologies must return a JSON string. This JSON response has two main entities. The first of these being the likelihood, which should have been previously set, and secondly the 'extra' field. The extra field contains information that will be displayed to the user. This including the actual 'text' that was profiled, the 'keyword' in the text that flagged the liklihood increasing, the time and date, the 'type' or category of the methodology, and the 'sentiment' of the text. Neither the 'likelihood' or the 'extra' fields are mandatory.

```json
{"extra": [{"Keyword": "Mars",
            "Text": "Calling all marshmallows— come visit me on the set of Veronica Mars and get an inside look into Mars...",
            "Time": "2019",
            "Type": "LOCATION",
            "sentiment": "neutral"}],
 "likelihood": 5}
 ```

## 2 -The List Of Methodologies
Once you have created your likelihood methodology you will need to add it to the 'List_Of_Methodologies.py', this can be done by importing your methodology in the file and then adding it to the list of Methodologies. For example

 ```python
from Liklihood_Methodologies import Relationship_Detection as rd
from Liklihood_Methodologies import Goal_Detection as gd
from Liklihood_Methodologies import Location_Detection as ld
from Liklihood_Methodologies import url_recognition as ur
from Liklihood_Methodologies import blacklist_recognition as br

list_of_Methodologies = [rd.Relationship_Detection(),
                     gd.Goal_Detection(),
                     ld.Location_Detection(),
                     ur.Url_Recognition(),
                     br.Blacklist_Recognition()]
 ```
 
 ## 3 - The Hunch Configuration
 The final step is where the user will need to add the Methodologies name into their configuration file, this is so that Hunch knows to run your methodology. An example:
 
 ```json
 {
  "config": {
    "default_analyser": "comprehend",
    "collectors": ["twitter","reddit","instagram","tumblr","http"],
    "Methodologies": ["blacklist","goal","location","relationship","url"],
 ```
