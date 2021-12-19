from ctypes import Array, sizeof
import json
import os.path
import shutil
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import time
import re

def identify(string): ##Currently this function just accepts the manually input filetype and prints and returns it to confirm.
    log.logprint("\nIdentifying file as: " + str(string))
    filetype = string
    return filetype

def convert(file, filetype):
    log.logprint(os.path.abspath("\nConverting: " + str(file)))
    if filetype == "ROS Gridmap":
        convert_ROS(file)
    elif filetype == "2D Standard":
        convert_2DStandard(file)
    elif filetype == "Pointcloud":
        convert_pointcloud(file)

def convert_ROS(file):
    start = time.time() #start time
    log.logprint("\nConverting from ROS Gridmap")
    config.program_path = os.path.dirname(__file__)
    log.logprint("Program_Path: " + str(config.program_path))
    config.Selected_file_path =os.path.abspath(file)
    log.logprint("Selected_file_Path: " + str(config.Selected_file_path))
    config.Selected_file_path_dir =os.path.dirname(file)
    log.logprint("Selected_file_Path_dir: " + str(config.Selected_file_path_dir))
    properties = {}
    with open(file,"r") as f: ##Extract data as dict.
        config.properties = dict(i.strip().split(":", 1) for i in f)
        log.logprint("\ntest dict:"+ str(config.properties))
        log.logprint("Opened file: " +  str(os.path.realpath(f.name)))
    pgm_file_path = os.path.abspath(str(config.Selected_file_path_dir) + "/" + str(config.properties["image"].strip())) ##Not sure why a .strip has to be applied here again. since its done earlier
    with ImageProc.open(pgm_file_path, mode="r") as pgmf:
        log.logprint("Loading PGM data.")
        pixels = list(pgmf.getdata())
        width, height = pgmf.size
        config.properties.update(dict({"width": width}))
        config.properties.update(dict({"height": height}))
        config.properties.update(dict({"pixels": pixels}))
    log.logprint("\tWidth:" + str(width) + "\n\theight:" + str(height) + "\n\tAmount: \n")
    log.logprint(properties)
    config.filename = os.path.splitext(str(file)) ##remove extension from file to make name for convert.
    log.logprint("\nfilename: ")
    log.logprint(config.filename)
    output_name =os.path.realpath(config.filename[0] + "_Converted.json")
    ## Create JSOn file and original required Headers.
    create_json(output_name)
    #pixels_to_dict(config.properties)
    add_to_json(config.properties, output_name)
    end = time.time()
    print("Conversion Done!")
    log.logprint("Elapsed time is  {}s".format(end-start))
  
def pixels_to_dict(properties): #Format the read pixels to fit in a JSON, since pixels already in array this is probably unceessary.
    x = 0 #May not be required if the target standard doesnt require X,Y coordinates.
    y = 0
    temp = "["
    for n in properties["pixels"]:
        temp = temp + str(n) + "," ##assemble the values to a string.
    temp = temp + "]"
    tempdict = {"items": temp}
    properties.update(tempdict)
    log.logprint("\nPrinting propterties[\"items\"]:" + properties["items"])

def reset_config(): ## will be needed to run after each convert probably.
    return 0    

def convert_2DStandard(file):
    log.logprint("\nConverting from 2D Standard")
    json.dumps("2D standard test output")

def convert_pointcloud(file):
    log.logprint("\nConverting from pointcloud")
    with open(file,"r") as f: ##Extract data as dict.
        file_data = f.read()  
        print(file_data[:])
        config.properties["version"] = re.search("VERSION\s(.*)", file_data).group(1)
        config.properties["fields"] = re.search("FIELDS\s(.*)", file_data).group(1)
        config.properties["type"] = re.search("TYPE\s(.*)", file_data).group(1)
        config.properties["count"] = re.search("COUNT\s(.*)", file_data).group(1)
        config.properties["size"] = re.search("SIZE\s(.*)", file_data).group(1)
        config.properties["width"] = re.search("WIDTH\s(.*)", file_data).group(1)
        config.properties["height"] = re.search("HEIGHT\s(.*)", file_data).group(1)
        config.properties["viewpoint"] = re.search("VIEWPOINT\s(.*)", file_data).group(1)
        config.properties["points"] = re.search("POINTS\s(.*)", file_data).group(1)
        config.properties["data"] = re.search("DATA\s(.*)", file_data).group(1)
        print("\n properties data:" + str(config.properties))
        #log.logprint("\ntest dict:"+ str(config.properties))
        log.logprint("Opened file: " +  str(os.path.realpath(f.name)))

def add_to_json(properties, filename): #https://www.geeksforgeeks.org/append-to-json-file-using-python/
    with open(filename,'r+') as file: ## Currently everything is added as its own "Values" key, not sure if correct.
        log.logprint("Opened file:" + str(filename))
        log.logprint(properties)
        file_data = json.load(file) # First we load existing data into a dict.
        file_data["properties"].update({"list_of_voxels": properties["pixels"]}) # Join new_data with file_data inside emp_details
        file_data["properties"].update({"resolution": str(float(properties["resolution"]))})
        file_data["properties"].update({"map_description": "converted from old maptype"})
        file_data["properties"].update({"size": [int(properties["width"]), int(properties["height"]) , int(1) ]})
        file_data["properties"].update({"localmap_id": filename}) ##<-- get real name not path..
        file.seek(0) # Sets file's current position at offset.
        json.dump(file_data, file, indent = 4)# convert back to json.

def create_json(output_name): ## Sets up the very most basic JSON 3D MDR document which can be edited with real data.
    template_path = os.path.realpath(str(config.program_path) + "/JSON_Templates/3D_DenseGrid.json")
    shutil.copyfile(template_path, output_name)
    log.logprint("\nJSON file created \nHeader taken from: " + str(template_path))