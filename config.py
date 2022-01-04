# shared Variables in program
logging_enabled = False
Filetypes = ["ROS Gridmap", "2D Standard", "Pointcloud", "Test XSD"]
Font = "Helvetica, 14"
Filetype = Filetypes[0] ##Default filetype set

# Related to file conversion, reset after each conversion.
program_path = ""
Selected_file_path = ""
Selected_file_path_dir = ""
properties = {} ##Dict to hold all file data.
filename = ""
logfile_path = ""
output_name = ""