import re
import os
import sys
import numpy as np
import scipy
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt 
#filewithpath = '/Users/israel_CUMC/Desktop/MATPLOTLIB/run_ct15_data_1000lines.star'
try:
	filewithpath = sys.argv[1]
	
except IndexError:
	print("Wrong usage, please input absolute path to the star file.")
	print("Correct usage:")
	print("pythonn3.x rln_star_2_mollweide.py /path/path/relion_dir/Refine3D/jobxxx/run_class1.star")
	print("Please provide absolute path to file.")
	exit()
filewithpath_split = filewithpath.split('/')
root_path_pre = filewithpath_split[:-1]
root_path_pre.append('mollweide.png')
root_path = "/".join(root_path_pre)
with open(filewithpath, 'r') as f:
	filelines_pre = f.readlines()
filelines = filelines_pre[4:-2]
filelines_header = []
filelines_body = []
for i in filelines:
	if i.startswith('_rln'):
		filelines_header.append(i)
for i in filelines:
	if i[1].isdigit():
		filelines_body.append(i) 
#filelines_header_clean = list(filter(None, filelines_header))
filelines_header_clean = [ i.strip() for i in filelines_header]
filelines_body_clean = [ i.strip() for i in filelines_body]
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
rot = []
tilt = []
for i in filelines_body_clean:
	i_split = i.split()
	rot.append(float(i_split[rot_column]))
for i in filelines_body_clean:
	i_split = i.split()
	tilt.append(float(i_split[tilt_column]))
color_cmap = input("Which colormap do you want?\nDefault is 'plasma', if 'plasma' is ok hit Enter, if not, other options are:\n'viridis', 'hot', 'Greys', 'coolwarm'\nFor more options check: https://matplotlib.org/tutorials/colors/colormaps.html\nPlease type a colormap or hit enter:\n" )
if color_cmap:
	color_cmap = color_cmap
else:
	color_cmap = 'plasma'
tilt_m90 = [x -90 for x in tilt]
rot_rad = np.deg2rad(rot)
tilt_m90_rad = np.deg2rad(tilt_m90)
vertical_rad = np.vstack([tilt_m90_rad, rot_rad])
m = gaussian_kde (vertical_rad)(vertical_rad)
plt.figure()
plt.subplot(111, projection="mollweide")
plt.scatter(rot_rad, tilt_m90_rad, cmap=color_cmap, c=m, s=5)
plt.grid(None)
plt.xticks([])
plt.yticks([])
plt.vlines(0,-1.6,1.6, colors='k', linestyles='dashed')
plt.hlines(0,-10,10, colors='k', linestyles='dashed')
plt.savefig('mollweide')
plt.savefig(root_path, dpi=300)
plt.show()


