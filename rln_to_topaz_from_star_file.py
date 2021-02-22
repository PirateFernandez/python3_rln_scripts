import os
import sys
try:
	filewithpath = sys.argv[1]
	
except IndexError:
	print("Wrong usage, please input absolute path to the star file.")
	print("Correct usage:")
	print("pythonn3.x rln_to_topaz_from_star_file.py /path/path/relion_dir/Select/particles.star")
	print("Please provide absolute path to file.")
	exit()
#filewithpath = '/home/ifernandez/Documents/python3_work/particles.star'
filewithpath_split = filewithpath.split('/')
root_path_pre = filewithpath_split[:-1]
root_path_pre.append('topaz_particles.txt')
root_path = "/".join(root_path_pre)
with open(filewithpath, 'r') as f:
	filelines_pre = f.readlines()
"""Remove empty lines from list of lines."""
filelines = [i for i in filelines_pre if i != '\n']
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
filelines_body_clean_columns = []
for i in filelines_body_clean:
	i_split = i.split()
	filelines_body_clean_columns.append(i_split)

x_coor_column = 0
y_coor_column = 0
mic_name_column = 0
for i in filelines_header_clean:
	if '_rlnCoordinateX' in i:
		x_column_list = i.split("#")
		x_coor_column = (int(x_column_list[-1]))-1
for i in filelines_header_clean:
	if '_rlnCoordinateY' in i:
		y_column_list = i.split("#")
		y_coor_column = (int(y_column_list[-1]))-1
for i in filelines_header_clean:
	if '_rlnMicrographName' in i:
		mic_name_column_list = i.split("#")
		mic_name_column = (int(mic_name_column_list[-1]))-1
x_coor_val = []
y_coor_val = []
for i in filelines_body_clean_columns:
	x_coor_val.append(i[x_coor_column])
for i in filelines_body_clean_columns:
	y_coor_val.append(i[y_coor_column])
mic_name_path = []
mic_name_single = []
for i in filelines_body_clean_columns:
	i_split = i[mic_name_column].split("/")
	mic_name_single.append(i_split[-1])
mic_name_single_no_ext = []
for i in mic_name_single:
    i_split = i.split(".")
    mic_name_single_no_ext.append(i_split[-2])
header_topaz = 'image_name	x_coord	y_coord'
to_print = 'image_name	x_coord	y_coord'
for i in range(0, len(x_coor_val)):
	to_print += f"\n{mic_name_single_no_ext[i]}\t{x_coor_val[i]}\t{y_coor_val[i]}"
output = 'topaz.txt'
with open(output, 'w') as f:
	f.write(to_print)




print(to_print.strip())


#print(len(mic_name_single), len(x_coor_val), len(y_coor_val))

#print(f"header_topaz")
#for i in filelines_body_clean[0:3]:
#	print(f"{header_topaz}\n{filelines_body_clean[img_name_column]}\t{filelines_body_clean[x_coor_column]}\t{filelines_body_clean[y_coor_column]}")
#for i in filelines_body_clean_columns:
#	print(i([x_coor_column-1]))
