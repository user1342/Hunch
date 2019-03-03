# Sampling data from a user and source
The purpose of data source collectors is to sample data from a user account from a specific source or set of sources - for example sampling Jane Does data from twitter, reddit, and Instagram.


## 1 - The Template
Each collector needs specific elements of code so that it can function with the same functionality as any other..

### 1.1 The 'pull' function
All collectors need a 'pull' function in their class. This is the entry point for the class and is what will be called to aggregate data from sources. This function takes the paramiter of a username. A source does not need to be specified as each collector should be unique to a source (e.g. a twitter collector, an instagram collector, etc).
```python
def pull(self, username):
```

The pull function also returns a list of data aggrigated from the source and the user. When doing this you should use the character limit and return amount specified in the users configuration file. The character limit defines the max size for each string of text. The return amount defines the amount of strings returned. 
```python
import Core_ConfigInterpreter as cc
character_limit = cc.Config().get_aggrigat_character_limit("core_config.json")
return_amount = cc.Config().get_default_aggregations("core_config.json")
```

The data returned is a list of strings returned from the source and user that looks as follows:
```python
['The absolute worst. Thank God we filmed it. @fuegobox #chocochallenge https://t.co/7wFHtYvuXh', 'Head on over to my instagram stories at @kristenanniebell if youd like to see one of the most painful and embarrass… https://t.co/7GJlZd7mjR', 'RT @SarahKSilverman: Our government is doing this to humans.  This is non partisan issue. We have to join together to stop this. We are pun…', 'This is torture for these kids. I am so ashamed. https://t.co/nHHvbiroW3', 'I second this emotion. PLEASE @sagaftra, get us something better. @ExpressScripts /acreedo is very hard to use. https://t.co/egAXVUbklM']
```

## 2 - The List Of Collectors
All collectors to be used should be listed in the 'list_of_collectors.py' file. This file contains a dictionary with the key being the name of the collector (e.g. twitter) and the collectors class. See an example below:

```python
from Data_Source_Collectors import Instagram_Collector as ia

#This shows the collectors that exist and can be used
dictionary_of_collectors = {"instagram":ia.Instagram_Collector()}
```

## 3 - The Hunch Configuration
The final step is where the user will need to add the collectors name into their configuration file, this is so that Hunch knows to run your collector (This name should be the same as what was specified in the dictonary above). An example:
 
```json
{
    "config": {
    "default_analyser": "comprehend",
    "collectors": ["twitter","reddit","instagram","tumblr","http"],
    "detectors": ["blacklist","goal","location","relationship","url"],
```
