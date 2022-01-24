# shared Variables in program
#Related to UI
logging_enabled = False
batch_enabled = False
Filetypes = ["ROS Gridmap", "2D Standard", "Pointcloud"]
Font = "Helvetica, 14"
Filetype = Filetypes[0] ##Default filetype set

# Related to file conversion, reset after each conversion.
log = ""
batchlog = ""
program_path = ""
Selected_file_path = ""
Selected_file_path_dir = ""
properties = {} ##Dict to hold all file data.
filename = ""
logfile_path = ""
batchlog_path = ""
output_name = ""
matrix_out = []
time_now = ""
duration = []
size = []