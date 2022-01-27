from ctypes import Array, sizeof
import json
import os.path
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import re
import numpy
from bs4 import BeautifulSoup #XML

def ROS():
    log.logprint("\n\nExtracting Data from ROS Gridmap:")
    with open(config.Selected_file_path, "r") as f:  # Extract data as dict.
        for line in f:
            if not (line == "" or line == ";" or line == "\n"): ##Make sure line is not empty.
                (key, val) = line.strip().split(":")
                #print("\n" +str(key) + "\t" +str(val))
                config.properties[key] = val.lstrip()
        #print("\ntest dict:" + str(config.properties))
        log.logprint("\nOpened file: " + str(os.path.realpath(f.name)))
    pgm_file_path = os.path.abspath(str(
        config.Selected_file_path_dir) + "/" + str(config.properties["image"].strip()))
    with ImageProc.open(pgm_file_path, mode="r") as pgmf:
        log.logprint("\n\nOpeninng Accompanying image file:")
        log.logprint("\nLoading PGM data from:" + str(pgm_file_path))
        pixels = list(pgmf.getdata())
        width, height = pgmf.size
        config.size = str(len(pixels))
        config.properties.update(dict({"width": width})) 
        config.properties.update(dict({"height": height})) 
        config.properties.update(dict({"pixels": pixels})) 
    log.logprint("\tWidth:" + str(width) + "\n\theight:" +
                 str(height) + "\n\tAmount: " + config.size)

def PCD():
    log.logprint("\n\nExtracting Data from Pointcloud file:")
    with open(os.path.abspath(config.Selected_file_path), "r") as f:  # Extract data as dict.
        file_data = f.read()
        log.logprint("\nOpened file: " + str(os.path.realpath(f.name)))
        config.properties["version"] = re.search(
            "VERSION\s(.*)", file_data).group(1)
        config.properties["fields"] = re.search(
            "FIELDS\s(.*)", file_data).group(1)
        config.properties["type"] = re.search("TYPE\s(.*)", file_data).group(1)
        config.properties["count"] = re.search(
            "COUNT\s(.*)", file_data).group(1)
        config.properties["size"] = re.search("SIZE\s(.*)", file_data).group(1)
        size = re.search("SIZE\s(.*)", file_data).group(1)
        sizelen = len(size.split())
        log.logprint("\n\tArray Elements: " + str(sizelen))
        config.properties["width"] = re.search(
            "WIDTH\s(.*)", file_data).group(1)
        config.properties["height"] = re.search(
            "HEIGHT\s(.*)", file_data).group(1)
        config.properties["viewpoint"] = re.search(
            "VIEWPOINT\s(.*)", file_data).group(1)   
        config.properties["total_points"] = re.search(
            "POINTS\s(.*)", file_data).group(1)
        config.properties["data_encoding"] = re.search(
            "DATA\s(.*)", file_data).group(1)
        last_line = re.search("(DATA\s.*)", file_data).group(1)
        # config.properties["points"] = re.search(last_line + "\s((.*\n*)*)", file_data).group(1)
        # log.logprint("\ntest points:"+ str(config.properties["points"]))
        
    with open(os.path.abspath(config.Selected_file_path), "r") as f:  # Extract data
        file_matrix = f.readlines()
        matrix = []
        record = False
        for lines in file_matrix:  # find last line, record rows after that in matrix.
            if record == True:
                data = lines.split(" ")
                if sizelen == 3:
                    matrix.append([float(data[0]),float(data[1]),float(data[2])])
                elif sizelen == 4:
                    matrix.append([float(data[0]),float(data[1]),float(data[2]),float(data[3])])
                elif sizelen == 5:
                    matrix.append([float(data[0]),float(data[1]),float(data[2]),float(data[3]),float(data[4])])
            if str(lines).rstrip() == str(last_line).rstrip() and record == False:
                #print("last line found")
                record = True
    config.size = str(len(matrix))
    log.logprint("\n\tSize of matrix is:" + config.size) 
    config.properties["list_of_points"] = matrix
    config.matrix_out = matrix
    
def XML(file):
    log.logprint("\nConverting from 2D Standard")
    with open(file, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    num_cells = Bs_data.find('num_cells_x')
    cells = Bs_data.find_all('cells')
    log.logprint(num_cells)
    log.logprint(cells)