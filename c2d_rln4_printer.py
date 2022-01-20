import os
import sys
import numpy as np
try:
	import mrcfile
except ImportError:
	print("### mrcfile python package missing.###")
	print("### visit: https://pypi.org/project/mrcfile/ ###")
	print("### try: ###")
	print("### conda install --channel conda-forge mrcfile ###")
	print("### or: ###")
	print("### pip install mrcfile ###")
	exit()
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
#import matplotlib.gridspec as gridspec
try:
	path_to_mrcs_file = sys.argv[1]
except IndexError:
	print("### Wrong usage, please provide absolute path to mrcs file with the c2d.###")
	print("Correct usage:")
	print("python3.X c2d_rln4_printer.py /path/rln4_folder/Class2D/jobxxx/run_itxxx_classes.mrcs /path/rln4_folder/Select/jobxxx/class_averages.star OR a comma separated list of classes to print.")
	print("python3.X c2d_rln4_printer.py /path/rln4_folder/Class2D/jobxxx/run_itxxx_classes.mrcs 10,12,33")	
	exit()
try:
	path_to_star_file = sys.argv[2]
except IndexError:
	print("### Wrong usage, please provide absolute path to class_averages.star with selected classes or a python list with the classes to print.###")
	print("python list example: [2, 33, 45]")
	print("Correct usage:")
	print("python3.X c2d_rln4_printer.py /path/rln4_folder/Class2D/jobxxx/run_itxxx_classes.mrcs /path/rln4_folder/Select/jobxxx/class_averages.star OR a comma separated list with classes to print.")
	print("python3.X c2d_rln4_printer.py /path/rln4_folder/Class2D/jobxxx/run_itxxx_classes.mrcs 10,12,33")
	exit()
###
if os.path.isfile(path_to_star_file):
	with open(path_to_star_file, 'r') as f:
		good_classes_pre = []	
		f_lines = f.readlines()
		for i in f_lines:
			if i[0].isdigit():
				i_split = i.split("@")
				good_classes_pre.append(int(i_split[0]))
else:	
	good_classes_pre = [int(i) for i in list(path_to_star_file.split(","))]
###
good_classes = sorted(good_classes_pre)
good_classes_renum = [i-1 for i in good_classes]
###
with mrcfile.open(path_to_mrcs_file) as emd:
	nx, ny, nz = emd.header['nx'], emd.header['ny'], emd.header['nz']
	np_emd = emd.data.flatten(order='F').reshape(nx, ny, nz)
###
for i in (good_classes_renum):
	c2d_num = i + 1
	fig = plt.figure(figsize=(2,2))
	f1_ax1  = fig.add_subplot()
	plt.imshow(np_emd[:,:,i], cmap="gray")
	f1_ax1.set_yticks([])
	f1_ax1.set_yticklabels([])
	f1_ax1.set_xticks([])
	f1_ax1.set_xticklabels([])
	plt.savefig(f"c2d-number-{c2d_num}.png", dpi=300)
###

