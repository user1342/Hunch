from Data_Source_Aggregators import Instagram_Aggrigator as ia
from Data_Source_Aggregators import Twitter_Aggrigator as tw
from Data_Source_Aggregators import Reddit_Aggrigator as ra
from Data_Source_Aggregators import Tumblr_Aggrigator as ta

# An aggregator must have:
# - a 'pull' function that takes a username as a parameter. This returns a list of strings from that user.

#This shows the aggregators that exist and can be used
dictionary_of_aggrigators = {"instagram":ia.Instagram_Aggrigator(),
                             "twitter":tw.Twitter_Aggrigator(),
                             "reddit":ra.Reddit_Aggrigator(),
                             "tumblr":ta.Tumblr_Aggrigator()
                             }