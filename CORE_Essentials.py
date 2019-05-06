import time
import requests
import CORE_Logger

'''
This function loops for the given amount of seconds and if no connection is made to the internet before the timeout then it raises an exception.
'''
def check_connected(timeout_seconds):
    t_end = time.time() + timeout_seconds
    while time.time() < t_end:

        success = False
        try:
            url = requests.get("http://google.com")
            success = True
            CORE_Logger.log("Connection to internet made.")
            break
        except:
            CORE_Logger.log("Failed to connect to the internet, retrying...")
            success = False

        time.sleep(timeout_seconds/5)

    if success == False:
        CORE_Logger.log("No internet connection found. Raising Exception...")
        raise Exception("No Internet Connection Found")