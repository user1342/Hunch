import re
import subprocess as sp
import Core_ConfigInterpreter as cc

'''
A class used to gather information from generic websites
'''
class Instagram_Aggrigator:

    # The constructor
    def __init__(self):
        self.list_of_posts = []

    #method used to gather information from a defined website
    def pull_from_instagram(self,username):
        instagram_base_url = "https://www.instagram.com/"

        # Gets the text for the photos on their profile.
        url = instagram_base_url + username + '/'
        website = sp.Popen(["curl", url], stdout=sp.PIPE)
        list_of_lines_of_website = website.communicate()[0].split(
            b"\n")  # Breaks each line up of the downaloded website.
        post_list = re.findall(r'text\":(.*?),\"shortcode', str(list_of_lines_of_website))

        #Adds this text to the list and cuts the post length to a size set in the config.
        character_limit = cc.Config().get_aggrigat_character_limit("core_config.json")
        for post in post_list:
            #Removes excess characters
            post = re.sub(r"(\\\\[^ ]*)","", post)
            post = re.sub("}","",post)
            post = re.sub("]", "", post)
            post = post.strip("]")
            post = post.strip('"')
            if character_limit > len(post):
                pass
            else:
                post = post[0:character_limit]+"..."
            self.list_of_posts.append(post)

        #Checks if the amount requested to return in the config is above the amount actually returned by instagram.
        return_amount = cc.Config().get_default_aggregations("core_config.json")
        if return_amount > 11:
            return_amount = 11

        return self.list_of_posts[1:return_amount+1]

