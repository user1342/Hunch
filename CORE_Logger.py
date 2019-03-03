import datetime

import CORE_ConfigInterpreter as cc

def log(text):
    default_log_file = cc.Config().get_log_path("core_config.json")

    current_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = current_dt + " | " + str(text)

    if cc.Config().get_verbose("core_config.json"):
        print(message)

        try:
            log_file = open (default_log_file, "a")
        except:
            log_file = open(default_log_file, "w")

        log_file.write(message +"\n")
        log_file.close()
