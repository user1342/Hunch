# How Data Source Aggregation Works

Data source aggregators are used to gather information from a specific website on a specific individual. For example all of the information from the user 'Jane Doe' on Reddit.

The Hunch Core Aggregator class manages what aggregators are used depending on it's input. For example the below aggregator will profile the 'realdonaldtrump' account on Twitter. 

```python
import Core_Aggregator

my_aggrigator = Core_Aggregator.WebsiteToCrawl([{"twitter":"realdonaldtrump"}],"realdonaldtrump")

```

When the [Core Aggregation class](https://github.com/user1342/Hunch/blob/master/Core_Aggregator.py) is run it compares the specified website against a series of known aggregators, these being listed below. When a new aggregator is created it needs to be added to this series of IF statments.

```python
if key == "twitter":
    #Run Twitter aggregator

elif key == "reddit":
    #Run Reddit aggregator

elif "http" in key:
    #Run HTTP aggregator
else:
    raise Exception("Unknown Website " + key)
```

Inside each of these IF statments a new aggregator is created. This involves importing the aggregator class, creating an aggregator object and running the necessary functions. These functions will take as a paramiter the name of the individual / username to be profiled on the website. The response will contain text affiliated with that user from the website and will be added to a of all text associated with the individual so far. 

```python
from Data_Source_Aggregators import Twitter_Aggrigator as tw

aggrigator = tw.Twitter_Aggrigator()

response = aggrigator.pull_from_twitter(user)
try:
    self.list_of_text.extend(response)
except:
    self.list_of_text.append(response)
```

Inside of the individual [Data Source Agrregators](https://github.com/user1342/Hunch/tree/master/Data_Source_Aggregators) code can contain any array of functions. The only necessity is that it takes as a **paramiter of the username** and **returns a list of the text affiliated with the user**. E.g. the Reddit aggregator will return all of the comments the specified Reddit user has made. 
