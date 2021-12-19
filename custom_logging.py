import config

def logprint(string):
    if config.logging_enabled == True:
        print(string)
        #print("logging done")