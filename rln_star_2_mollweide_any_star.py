import os
import sys
import numpy as np
import scipy
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt 
######
"""check if user supplied star file location with absolute path, if not handle the exception."""
try:
	filewithpath = sys.argv[1]
	
except IndexError:
	print("Wrong usage, please input absolute path to the star file.")
	print("Correct usage:")
	print("pythonn3.x rln_star_2_mollweide.py /path/path/relion_dir/Refine3D/jobxxx/run_class1.star")
	print("Please provide absolute path to file.")
	exit()
#####
"Use path to file to define a variable with the file name to save final png"""
filewithpath_split = filewithpath.split('/')
root_path_pre = filewithpath_split[:-1]
root_path_pre.append('mollweide.png')
root_path = "/".join(root_path_pre)
#####
"""Open python object with the user supplied file and read the file to a list where every line is an element of the list."""
with open(filewithpath, 'r') as f:
	filelines_pre = f.readlines()
"""Remove the three first line of the file and the last line."""
filelines = filelines_pre[4:-2]
"""Split the all-file list to two list containing lines from the header and lines with particle information."""
#####
filelines_header = []
filelines_body = []
for i in filelines:
	if i.startswith('_rln'):
		filelines_header.append(i)
for i in filelines:
	if i[1].isdigit():
		filelines_body.append(i) 
filelines_header_clean = [ i.strip() for i in filelines_header]
filelines_body_clean = [ i.strip() for i in filelines_body]
#####
"""Extract the column number for rot and tilt in the star file."""
rot_column = 0
tilt_column = 0
for i in filelines_header_clean:
	if '_rlnAngleRot' in i:
		rot_column_list = i.split("#")
		rot_column = (int(rot_column_list[-1]))-1
for i in filelines_header_clean:
	if '_rlnAngleTilt' in i:
		tilt_column_list = i.split("#")
		tilt_column = (int(tilt_column_list[-1]))-1
#####
"""Extract rot and tilt values from file and save them in to lists of floats."""
rot = []
tilt = []
for i in filelines_body_clean:
	i_split = i.split()
	rot.append(float(i_split[rot_column]))
for i in filelines_body_clean:
	i_split = i.split()
	tilt.append(float(i_split[tilt_column]))
#####
"""Ask user which colormap to use, default plasma."""
color_cmap = input("Which colormap do you want?\nDefault is 'plasma', if 'plasma' is ok hit Enter, if not, other options are:\n'viridis', 'hot', 'Greys', 'coolwarm'\nFor more options check: https://matplotlib.org/tutorials/colors/colormaps.html\nPlease type a colormap or hit enter:\n" )
if color_cmap:
	color_cmap = color_cmap
else:
	color_cmap = 'plasma'
#####
"""Manipulate list of rot and tilt to be in radians and in the range for the mollweide projection."""
"""Create numpy vertical stacks for kde scipy function."""
tilt_m90 = [i -90 for i in tilt]
rot_rad = np.deg2rad(rot)
tilt_m90_rad = np.deg2rad(tilt_m90)
vertical_rad = np.vstack([tilt_m90_rad, rot_rad])
m = gaussian_kde (vertical_rad)(vertical_rad)
x_60_rad = [1.047 for i in range(0,7)]
x_m60_rad = [-1.047 for i in range(0,7)]
x_120_rad = [2.094 for i in range(0,7)]
x_m120_rad = [-2.094 for i in range(0,7)]
#####
"""Plotting with matplotlib."""
fig = plt.figure()
ax = plt.subplot(111, projection="mollweide")
"""s-->size of the dots, alpha--> tranparency with 0 transparent and 1 opaque."""
ax.scatter(rot_rad, tilt_m90_rad, cmap=color_cmap, c=m, s=2, alpha=0.4)
"""Thse two lines remove the ticks and their labels."""
ax.set_yticklabels([])
ax.set_yticklabels([])
"""These for lines draw curve lines at x -120, -60, 60, 120."""
ax.plot(x_60_rad, np.arange(-1.5, 2, 0.5), color='k', lw=1.5, linestyle=':')
ax.plot(x_m60_rad, np.arange(-1.5, 2, 0.5), color='k', lw=1.5, linestyle=':')
ax.plot(x_120_rad, np.arange(-1.5, 2, 0.5), color='k', lw=1.5, linestyle=':')
ax.plot(x_m120_rad, np.arange(-1.5, 2, 0.5), color='k', lw=1.5, linestyle=':')
"""These two lines draw vertical and horizontal straight lines as x, y cartesian axes."""
ax.vlines(0,-1.6,1.6, colors='k', lw=1.5, linestyles=':')
ax.hlines(0,-10,10, colors='k', lw=1.5, linestyles=':')
"""Writes a png dpi 300 file at the same location where the star file is."""
plt.savefig(root_path, dpi=300)
plt.show()


