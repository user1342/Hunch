import re
import subprocess as sp
import Core_ConfigInterpreter as cc

'''
A class used to gather information from tumblr
'''
class Tumblr_Aggrigator:

    #method used to gather information from tumblr
    def pull(self,username):
        list_of_posts = []
        tumblr_base_url = ".tumblr.com"
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
            line = re.sub(r"\\.*? \w'", " ", line)
            line = line.replace("  ", "")
            line = line.replace("&rsquo;", "'")
            line = re.sub(r"&.*?;", "",line)
            if len(line) > 100:
                if character_limit > len(line):
                    character_limit = len(line)
                list_of_posts.append(line[0:character_limit]+"...")

        #Sets the amount to return as the value set in the config
        return_amount = cc.Config().get_default_aggregations("core_config.json")

        return list_of_posts[0:return_amount]

