from Data_Source_Collectors import Instagram_Collector as ic
from Data_Source_Collectors import Twitter_Collector as twc
from Data_Source_Collectors import Reddit_Collector as rc
from Data_Source_Collectors import Tumblr_Collector as tc

# An collector must have:
# - a 'pull' function that takes a username as a parameter. This returns a list of strings from that user.

#This shows the collectors that exist and can be used
dictionary_of_collectors = {"instagram":ic.Instagram_Collector(),
                             "twitter":twc.Twitter_Collector(),
                             "reddit":rc.Reddit_Collector(),
                             "tumblr":tc.Tumblr_Collector()
                             }