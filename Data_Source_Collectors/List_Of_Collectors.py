from Data_Source_Collectors import Instagram_Collector as ia
from Data_Source_Collectors import Twitter_Collector as tw
from Data_Source_Collectors import Reddit_Collector as ra
from Data_Source_Collectors import Tumblr_Collector as ta

# An collector must have:
# - a 'pull' function that takes a username as a parameter. This returns a list of strings from that user.

#This shows the collectors that exist and can be used
dictionary_of_collectors = {"instagram":ia.Instagram_Collector(),
                             "twitter":tw.Twitter_Collector(),
                             "reddit":ra.Reddit_Collector(),
                             "tumblr":ta.Tumblr_Collector()
                             }