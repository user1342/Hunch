# Hunch
A Predictive Policing and Threat Aggregation toolset. This modular toolset, powered by Natural Language Processing and Open Source Intelligence, is desiged to provide the user with actionable data including: signals, pivots, and risk levels. In collecting this information all that is required from the user is a 'source'(e.g. Twitter) and 'username'(e.g. Jane Doe). Current source collectors include: Twitter, Instagram, Tumblr, and Reddit. 

For more on how Natural Language Processing can be used to predict crime, check out this [article](https://www.infosecurity-magazine.com/next-gen-infosec/language-processing-motive/) and a [talk](https://www.youtube.com/watch?v=9F0vbbjw9jk&t=1s). 

If you have a specific use case for Hunch and would like help in it's implementation then please reach out to [James Stevenson](http://www.jamesstevenson.me/). 

<img src="https://github.com/user1342/Hunch/blob/master/Hunch_FlowDiagram.png"  width = 400> <img src="https://github.com/user1342/Hunch/blob/master/Demo.gif" width = 400>

## Installation

To use the AWS Comprehend aggregation for Hunch you will need to have the [AWS CLI](https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html) installed.  As part of setting up the AWS CLI you will need to create an AWS [IAM](https://console.aws.amazon.com/iam) user with the "ComprehendFullAccess" group and set this as your user when it comes to the configure stage.

```bash
pip install awscli --upgrade --user
```
```bash
aws configure
```
The Reddit aggregation requires the Reddit [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html) api to be installed. You will also need a [Reddit developed application](https://www.reddit.com/prefs/apps/) and use the keys created as part of that process. The API keys will need to be added to the [Core_Config.Json](https://github.com/user1342/Hunch/blob/master/core_config.json).

```bash
pip install praw
```
The Twitter aggrigator requires the [Tweepy](http://www.tweepy.org/) module and requires [Twitter App API keys](https://developer.twitter.com/en/apps). The API keys will need to be added to the [Core_Config.Json](https://github.com/user1342/Hunch/blob/master/core_config.json).

```bash
pip install tweepy
```
The core display requires the [Dash](https://dash.plot.ly/) python plugin to be installed. The display also uses [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html) to display tables. 
```bash
pip install dash==0.35.1
pip install dash-html-components==0.13.4
pip install dash-core-components==0.42.1
pip install dash-table==3.1.11
pip install dash-auth==1.2.0
```
```bash
pip install pandas
```
Location detection requires the [GeoPy](https://pypi.org/project/geopy/) plugin that can be installed with the command below. The Location Detection also uses the [UK Police Crime API](https://data.police.uk/docs/). This API does not currently require an API key. 
```bash
pip install geopy
```
The URL Recognition script requires the [Requests](https://pypi.org/project/requests/2.7.0/) plugin to un shorten url shortlinks. 
```bash
pip install requests
```

## Usage
There is an example Python script called [Example_Profile_Script.py](https://github.com/user1342/Hunch/blob/master/Example_Profile_Script.py) that contains the necessary code to profile all individuals in the [JSON FILES folder](https://github.com/user1342/Hunch/tree/master/Json_Files) as well as launching the display interface on localhost. A simplified version of this can be found below:

```python

import Core_Collector
import Core_Display
import Core_Individual

my_aggrigator = Core_Collector.WebsiteToCrawl([{"twitter":"realdonaldtrump"}],"Donald J. Trump")

my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data(), my_aggrigator.name)

Core_Display.create_website([my_individual.profile()]).generate_page()

```
In addition to this you can use the [Lazy](https://github.com/user1342/Hunch/blob/master/Lazy.py) tool which cuts down on the code needed to profile individuals, however, loses some of the additional functionality.
```python

import Lazy

list_to_profile = [
    [[{"twitter":"realdonaldtrump"}],"Donald J. Trump", 1],
    [[{"twitter":"AOC"}],"Alexandria Ocasio-Cortez", 1],
    [[{"reddit":"user_simulator"}],"user_simulator", 1]
]

lazy_profle = Lazy.lazy_profile()

for individual in list_to_profile:
    lazy_profle.profile(individual[0],individual[1], individual[2])

lazy_profle.display_webpage()

```


## Contributing
Pull requests are welcome, including creating new detectors, aggrigators, and analysers. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate... When I make some.

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)
