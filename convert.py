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
from datetime import datetime

# Currently this function just accepts the manually input filetype and prints and returns it to confirm.
def identify(string):
    log.logprint("\nIdentifying file as: " + str(string))
    filetype = string
    return filetype

def convert(file, filetype): #Main function for handling full conversions.
    start = time.time()  # start timer.
    get_paths(file)
    create_json(config.output_name)
    config.time_now = str(datetime.now())
    log.logprint(os.path.abspath("\nConverting: " + str(file)))
    if filetype == "ROS Gridmap":
        log.logprint("\nConverting from ROS Gridmap")
        extract.ROS(file)
        addtojson.Rosgrid()
    elif filetype == "2D Standard":
        extract.XML(file)
    elif filetype == "Pointcloud":
        log.logprint("\nConverting from PCD Pointcloud")
        extract.PCD(file) 
        addtojson.Pointcloud()
    log.logprint("printing Properties dict")
    log.logprint("\nClearing temp extracted data")
    reset_config() ## Resets the variables holding data, so a new one can be performed without carryover.
    print("\nConversion Done!")
    log.logprint("\nElapsed time is  {}s".format(time.time()-start))

def reset_config():  # will be needed to run after each convert probably.
    config.properties.clear()
    config.Selected_file_path = ""
    config.filename = ""
    config.logfile_path = ""
    config.output_name = ""
    config.matrix_out = []
    config.time_out = ""

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

def get_paths(file):
    config.program_path = os.path.dirname(__file__)
    log.logprint("Program_Path: " + str(config.program_path))
    config.Selected_file_path = os.path.abspath(file)
    log.logprint("Selected_file_Path: " + str(config.Selected_file_path))
    config.Selected_file_path_dir = os.path.dirname(file)
    log.logprint("Selected_file_Path_dir: " +
                 str(config.Selected_file_path_dir))
    config.Selected_file_path = os.path.splitext(str(file))
    log.logprint("\nSelected_file_path: ")
    log.logprint(config.Selected_file_path)
    config.output_name = os.path.realpath(
        config.Selected_file_path[0] + "_Converted.json")
