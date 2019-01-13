# Hunch

A predictive policing framework that uses natural language processing (NLP) at it's core.
![Hunch Flow Diagram](https://github.com/user1342/Hunch/blob/master/Hunch_FlowDiagram.png?raw=true)
## Installation

To use the AWS Comprehend aggregation for Hunch you will need to have the [AWS CLI](https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html) installed.  As part of setting up the AWS CLI you will need to create an AWS [IAM](https://console.aws.amazon.com/iam) user with the "ComprehendFullAccess" group and set this as your user when it comes to the configure stage.

```bash
pip install awscli --upgrade --user
```
```bash
aws configure
```
The Reddit aggregation requires the Reddit [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html) api to be installed. You will also need a [Reddit developed application](https://www.reddit.com/prefs/apps/) and use the keys created as part of that process.

```bash
pip install praw
```
The Twitter aggrigator requires the [Tweepy](http://www.tweepy.org/) module and requires [Twitter App API keys](https://developer.twitter.com/en/apps).

```bash
pip install tweepy
```

## Usage
There is an example Python script called [Example_Profile_Script.py](https://github.com/user1342/Hunch/blob/master/Example_Profile_Script.py) that contains the necessary code to profile an individual. A sample of this is below:

```python

import Core_Aggregator
import Core_Individual

my_aggrigator = Core_Aggregator.WebsiteToCrawl(["twitter","reddit"],"realdonaldtrump")

my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data())

results = my_individual.profile()

print(results["likelihood"])

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate... When I make some.

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)
