# Entity Recognition and Sentiment Analysis using NLP
The NLP Analysers are the backbone of this tool. These classes use natural langauge processing to perform entity recognition and sentiment analysis on given items of text. The [Core_NLPAnalyser.py](https://github.com/user1342/Hunch/blob/master/Core_NLPAnalyser.py) stands as a gateway for the likelihood detector classes to use the natural langauge processing functionality. This means that the same NLP Analyser is used across individuals and websites for each run. In turn this analyser is set in the users configuration. Currently there is only one NLP analyser and this is the AWS Comprehend analyser.  

## 1 - The Template
When creating an NLP Analyser there are several pieces that you will need to add to your code to conform with the other NLP Analysers. 

### 1.1 - The Entry Point
For the NLP_Analysers the function 'construct_detect_command' is the entry point for the analyser. This takes in two paramiters, the text to be profiled and what type of profiling is to be performed, currently the only two types are "detect-sentiment", and "detect-entities", your 'construct_detect_command' function should take this input and profile the text accordingly. 

```python
def construct_detect_command(self, task, text):
```

### 1.2 - Returning a JSON response
The 'construct_detect_command' should return a JSON response if it has detected any entities or with the sentiment of the text. The returned entities is based off the [AWS Comprehend Entities List](https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html).     
     
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

## 2 - List Of Analysers
Next you will need to both import your analyser and add it to the list_of_analysers in the 'Core_NLPAnalysers.py' file. 

```python
from NLP_Analysers import Aws_NLPAnalyser

list_of_analysers = [Aws_NLPAnalyser.AWSComprehend()]
```

## 3 - The Configuration
 The final step is where the user will need to add the default_analyser name into their configuration file, this is so that Hunch knows to run the specific analyser. An example:
 
 ```json
 {
  "config": {
    "default_analyser": "comprehend",
    "aggregators": ["twitter","reddit","instagram","tumblr","http"],
    "detectors": ["blacklist","goal","location","relationship","url"],
 ```
        
