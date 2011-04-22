#!/usr/bin/env python

import os

class SimpleBackup:
	PROCESSED_DIR = 'SIMPLE-PROCESSED'

	def __init__(sub_dirs_only, backup_helper):
		""" sub_dirs_only is the list of directories where we don't process files, only sub
		directories. backup_helper is a function that backs up one file. """
		self.sub_dirs_only = sub_dirs_only
		self.backup_helper = backup_helper
		self.base_dir = None

	def backup(self, dir_name):
		for root, dirs, files in os.walk(dir_name):
			dirs[:] = [d for d in dirs if not SimpleBackup.PROCESSED_DIR in d]

			self.base_dir = dir_name

			if not root in ignore_list:
				for f in files:
					self.backup_helper(f)
					self.shunt(f, root)

	def shunt(filename, directory):
		source = os.path.join(directory,filename)

		#create target directory if it doesn't exist
		target_directory = os.path.join(directory, SimpleBackup.PROCESSED_DIR)

		if not os.path.exists(target_directory):
			os.path.mkdir(target_directory)	

		#move file from source to target
		target = os.path.join(target_directory, filename)
		shutil.move(source, target)
