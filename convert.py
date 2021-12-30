from ctypes import Array, sizeof
import json
import os.path
import shutil
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import time
import addtojson
import extract


# Currently this function just accepts the manually input filetype and prints and returns it to confirm.
def identify(string):
    log.logprint("\nIdentifying file as: " + str(string))
    filetype = string
    return filetype

def convert(file, filetype):
    log.logprint(os.path.abspath("\nConverting: " + str(file)))
    if filetype == "ROS Gridmap":
        start = time.time()  # start time
        extract.ROS(file)
        create_json(config.output_name)
        addtojson.Rosgrid(config.properties, config.output_name)
    elif filetype == "2D Standard":
        extract.XLM(file)
    elif filetype == "Pointcloud":
        extract.PCD(file)
    print("Conversion Done!")
    log.logprint("Elapsed time is  {}s".format(time.time()-start))

def reset_config():  # will be needed to run after each convert probably.
    program_path = ""
    Selected_file_path = ""
    Selected_file_path_dir = ""
    properties = {} ##Dict to hold all file data.
    filename = ""
    logfile_path = ""
    output_name = ""

# Sets up the very most basic JSON 3D MDR document which can be edited with real data.
def create_json(output_name):
    template_path = os.path.realpath(
        str(config.program_path) + "/JSON_Templates/Convert_Template.json")
    ## Check if output file already exists, if so, remove
    if os.path.exists(output_name):
            os.remove(output_name)
    shutil.copyfile(template_path, output_name)
    log.logprint("\nJSON file created \nHeader taken from: " +
                 str(template_path))
