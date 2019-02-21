from Liklihood_Detectors import Relationship_Detection as rd
from Liklihood_Detectors import Goal_Detection as gd
from Liklihood_Detectors import Location_Detection as ld
from Liklihood_Detectors import url_recognition as ur
from Liklihood_Detectors import blacklist_recognition as br

#A detector must have a:
# - 'detector_name' variable.
# - 'get_score' function, that takes a string of text to be profiled as a parameter. This returns a dictionary.

#This lists the detectors that exist and can be used.
list_of_detectors = [rd.Relationship_Detection(),
                     gd.Goal_Detection(),
                     ld.Location_Detection(),
                     ur.Url_Recognition(),
                     br.Blacklist_Recognition()]