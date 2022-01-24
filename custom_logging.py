import config

def logprint(string): ##Log to temp string.
    if config.logging_enabled == True:
        config.log += string

def batchlogprint():
    pps = float(config.duration)/float(config.size)*100000
    config.batchlog += "\n" + str(config.filename) + "\t&\t" + str(config.size) + "\t&\t" + str(config.duration) +"\t&\t"+ str(round(pps, 2)) + "\t\\\\"

def log_finalize():
    with open(config.logfile_path, "w") as f:
        f.writelines(config.log)
    config.log = ""

def batch_log_finalize():
    with open(config.batchlog_path, "w") as f:
        print("\nWritingBatchlog")
        f.writelines(config.batchlog)
    config.batchlog = ""