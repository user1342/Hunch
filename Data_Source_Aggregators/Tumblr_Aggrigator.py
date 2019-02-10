import re
import subprocess as sp
import Core_ConfigInterpreter as cc

'''
A class used to gather information from tumblr
'''
class Tumblr_Aggrigator:

    # The constructor
    def __init__(self):
        self.list_of_posts = []

    #method used to gather information from tumblr
    def pull_from_tumblr(self,username):
        tumblr_base_url = ".tumblr.com"
        username = "elven-child"
        # Gets the text for the photos on their profile.
        url = username + tumblr_base_url
        website = sp.Popen(["curl", url], stdout=sp.PIPE)
        list_of_lines_of_website = website.communicate()[0].split(b"\n")

        #Sets the character limit for a post from the config
        character_limit = cc.Config().get_aggrigat_character_limit("core_config.json")

        #Finds each post from tumblr by looking at the ,p. blocks
        post_list = re.findall(r'<p>(.*?)<\/p>', str(list_of_lines_of_website))

        # The below loops through the posts and formats them accordingly
        for line in post_list:
            line = re.sub(r"(<.*?>)", "", line)
            #line = re.sub(r'(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', line)
            line = re.sub(r'\\.*?  ', "", line)
            line = line.replace("  ", "")
            line = line.replace("&rsquo;", "'")
            line = line.replace("&ldquo;", "")
            if len(line) > 100:
                if character_limit > len(line):
                    character_limit = len(line)
                self.list_of_posts.append(line[0:character_limit]+"...")

        #Checks if the amount requested to return in the config is above the amount actually returned by tumblr.
        return_amount = cc.Config().get_default_aggregations("core_config.json")
        if return_amount > 10:
            return_amount = 10

        return self.list_of_posts[1:return_amount+1]

