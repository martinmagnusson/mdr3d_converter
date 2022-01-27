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
    #print("Start Converting")  # Create popup?
    start = time.time()  # start timer.
    get_new_filenames()
    create_json(config.output_name)
    config.time_now = str(datetime.now())
    log.logprint(os.path.abspath("\nConverting: " + str(file)))
    if filetype == "ROS Gridmap":
        log.logprint("\nConverting from ROS Gridmap")
        extract.ROS()
        addtojson.Rosgrid()
    elif filetype == "2D Standard":
        extract.XML(file)
    elif filetype == "Pointcloud":
        log.logprint("\nConverting from PCD Pointcloud")
        extract.PCD() 
        addtojson.Pointcloud()
    log.logprint("\nPrinting Properties dict")
    log.logprint("\nClearing temp extracted data")
    log.log_finalize() ##Print logs to file.
    config.duration = format(time.time()-start)
    print("\nElapsed time is  " + str(config.duration))
    if config.batch_enabled == True:
        print("\nAdding to Batchlog")
        log.batchlogprint() # stores the file data in batch log.
    reset_config() ## Resets the variables holding data, so a new one can be performed without carryover.

def reset_config():  # will be needed to run after each convert probably.
    config.properties.clear()
    config.Selected_file_path = "" 
    #config.Selected_file_path_dir = ""
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
    #print("Template path is:" + str(template_path))
    if os.path.exists(output_name):
            os.remove(output_name)
    shutil.copyfile(template_path, output_name)
    log.logprint("\nJSON file created \nHeader taken from: " +
                 str(template_path))

def get_new_filenames():
    get_path_log_file()
    get_path_batch_log_file()
    get_path_converted_file()

def get_path_log_file():
    config.program_path = os.path.dirname(__file__)
    config.logfile_path = os.path.realpath(
        config.Selected_file_path.split(".")[0] + "_Log.txt")

def get_path_batch_log_file():
    config.program_path = os.path.dirname(__file__)
    config.batchlog_path = os.path.realpath(
        config.Selected_file_path_dir + "\Batch_Log.txt")

def get_path_converted_file():
    config.program_path = os.path.dirname(__file__)
    config.output_name = os.path.realpath(
        config.Selected_file_path.split(".")[0] + "_Converted.json")

def batch_ROS():
    for file in os.listdir(config.Selected_file_path_dir):
        if file.endswith('.yaml'):  # Assume ROS Gridmaps are always YAML files.
            config.filename = str(file)
            config.Selected_file_path = os.path.join(
                config.Selected_file_path_dir , config.filename)
            print("Converting:" + config.filename)
            convert(config.Selected_file_path, config.Filetype)          

def batch_PCD():
    for file in os.listdir(config.Selected_file_path_dir):
        if file.endswith('.pcd'):  # Assume ROS Gridmaps are always YAML files.
            config.filename = str(file)
            config.Selected_file_path = os.path.join(
                config.Selected_file_path_dir, config.filename)
            print("Converting:" + config.filename)
            convert(config.Selected_file_path, config.Filetype)