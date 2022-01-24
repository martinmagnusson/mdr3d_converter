import config

def logprint(string): ##Log to temp string.
    if config.logging_enabled == True:
        config.log += string

def log_finalize():
    with open(config.logfile_path, "w") as f:
        f.writelines(config.log)
    if config.batch_enabled == True:
        with open(config.batchlog_path, "w") as f:
            print("\n creating Batchlog")
            f.writelines(config.batchlog)