import re
import subprocess as sp
import time

'''
A class used to gather information from generic websites
'''
class Generic_Aggrigator:

    # The constructor
    def __init__(self):
        self.list_of_occurances = []

    #method used to gather information from a defined website
    def scrape_website(self,website, username, nested_pages_timeout = 10):

        list_of_urls = []
        list_of_urls.append(website)
        base_url = re.search("^.+?[^\/:](?=[?\/]|$)", website)

        #Assigned the base url to be equal to the contents of the main url
        if base_url is not None:
            base_url = base_url.group(0)
        else:
            raise Exception("Failed to parse base URL")


        iterator = 0
        #Loops through the websites in the url list to be scanned
        for url in list_of_urls:
            iterator = iterator + 1

            #Downloads the page for it's contents
            website = sp.Popen(["curl", url], stdout=sp.PIPE)
            list_of_lines_of_website = website.communicate()[0].split(b"\n") # Breaks each line up of the downaloded website.

            #Loops through each line downloaded
            for line in list_of_lines_of_website:
                line = str(line)
                #Searches for all of the links on the line
                nested_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)

                #If links are found and they belong to the base url they are added to the list of urls to be scanned
                if nested_urls:
                    for nested_url in nested_urls:
                        if base_url in nested_url:
                            if nested_url not in list_of_urls:
                                list_of_urls.append(nested_url)

                #Checks the line for if the username has been mentioned
                occurances_of_user = re.findall(username, line)

                #If the username has been mentioned the line is added to the list
                if occurances_of_user:
                        self.list_of_occurances.append(line)

            #Closes the loop if it's over the set threshold
            if iterator >= nested_pages_timeout:
                break

        # Chunks the responses down to 10 samples, mainly for testing purposes.
        return self.list_of_occurances[0:10]

