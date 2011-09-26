#!/usr/bin/env python

""" This is the shunter. It shunts zipped data files from the twitter
collection project into sub-directories for each day. 24 files/day adds up to a
lot of files in one directory. To prevent that, each day has it's own
directory. """

import os
import shutil

def get_directory_file_list(datadir):
	directory_listing = os.listdir(datadir)

	#separate directories, and data files

	directories = []
	data_files = []
	for d in directory_listing:
		if os.path.isdir(d):
			directories.append(d)
		elif 'gz' in d:
			#We're only interested in shunting the zipped files
			data_files.append(d)

	return (directories, data_files)

def extract_dir_name(data_file_name):
	""" From the data filename, extract the date """
	#Example file name: tweets.txt.2011-03-14_04.gz
	return data_file_name.split('.')[2].split('_')[0].replace('-', '')

def extract_directory_names(data_files):
	""" From the list of data_files, extract what the directory names should be. """
	days = [extract_dir_name(d) for d in data_files if len(d) > 1]
	#The day of the year is the name of the directory
	return set(days)

def create_directories(path_prefix, dir_names):
	""" Create the directories if they do not already exist """
	for d in dir_names:
		path = os.path.join(path_prefix, d)
		if not os.path.exists(path):
			os.mkdir(path)

def move_files(path_prefix, data_files):
	for f in data_files:
		directory = os.path.join(path_prefix, extract_dir_name(f))
		src = os.path.join(path_prefix, f)
		dest = os.path.join(directory, f)
		shutil.move(src, dest)

def shunt(data_directory):
	#Move the data files into directories for each day
	(directories, data_files) = get_directory_file_list(data_directory)
	dir_names = extract_directory_names(data_files)
	create_directories(data_directory, dir_names)
	move_files(data_directory, data_files)
