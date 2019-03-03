from Methodologies import Relationship_Detection as rd
from Methodologies import Goal_Detection as gd
from Methodologies import Location_Detection as ld
from Methodologies import url_recognition as ur
from Methodologies import blacklist_recognition as br

#A methodology must have a:
# - 'methodology_name' variable.
# - 'get_score' function, that takes a string of text to be profiled as a parameter. This returns a dictionary.

#This lists the methodologies that exist and can be used.
list_of_methodologies = [rd.Relationship_Detection(),
                     gd.Goal_Detection(),
                     ld.Location_Detection(),
                     ur.Url_Recognition(),
                     br.Blacklist_Recognition()]