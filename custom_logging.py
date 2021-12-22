import config

def logprint(string): ## Log levels? Extra.
    if config.logging_enabled == True:
        print(string)
        #print("logging done")