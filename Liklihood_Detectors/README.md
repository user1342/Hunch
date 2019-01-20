# Profiling The Likelihood from a given piece of text
The purpose of a liklihood detector is to take a given piece of text and implement a methadology that will return a likelihood. 

## When creating a new likelihood detector
When creating a new likelihood detector you will need to edit the code in [Core_Individual.py](https://github.com/user1342/Hunch/blob/master/Core_Individual.py). This file primarily defines all of the information relating to a specific individual. This including the name provided, all text to be profiled and their impact. 
To append a likelihood detector you will need to add a piece of code that functions similar to the below

```python
  # Adds the goal detector to be used when profiling
  from Liklihood_Detectors import Location_Detection as ld
  location_profile = ld.Location_Detection()
  list_of_detectors.append(location_profile)
```

After this code has been ammended to the Core Individual file when run it will be run when detecting the likelihood of all individuals that are being profiled.


Next you will need to create your  [likelihood detector](https://github.com/user1342/Hunch/tree/master/Liklihood_Detectors). This detector must have a public **.get_score** function. This function must take a string. This string will be a **string** that is affiliated to the individual being profiled. The new class will then have to profile that text and return a dictionary meeting the below framework:

```json
{"extra": [{"Keyword": "Mars",
            "Text": "Calling all marshmallows— come visit me on the set of Veronica Mars and get an inside look into Mars...",
            "Time": "2019",
            "Type": "LOCATION",
            "sentiment": "neutral"}],
 "likelihood": 5}
 ```
 
 Please look at how other likelihood detectors are written for a better feel of how the above is returned. 

 ## Using NLP
 Most likelihood detectors will want to use Natural Language Processing on the provided text to produce a likelihood. To do this instead of calling a NLP Analyser directly please use the [Core NLP Analyser]( https://github.com/user1342/Hunch/blob/master/Core_NLPAnalyser.py). This makes sure that all items of text use the same analyser for each run. To do this use code similar to the following.
 
 ```python
core_nlp = ca.Core_NLPAnalyser()
profiler = core_nlp.create_analyser()
json_response = self.profiler.construct_detect_command("detect-entities", self.text_to_profile)
```
