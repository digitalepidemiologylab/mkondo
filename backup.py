#!/usr/bin/env python

import os
import shutil

class SimpleBackup:
	PROCESSED_DIR = 'SB_DATA_SB'

	def __init__(self, sub_dirs_only, backup_helper):
		""" sub_dirs_only is the list of directories where we don't process files, only sub
		directories. backup_helper is a function that backs up one file. """
		self.sub_dirs_only = sub_dirs_only
		self.backup_helper = backup_helper
		self.base_dir = None

	def backup(self, dir_name, **kwargs):
		for root, dirs, files in os.walk(dir_name):
			dirs[:] = [d for d in dirs if not SimpleBackup.PROCESSED_DIR in d]
			self.base_dir = dir_name

			if not self.sub_dirs_only or (not root in self.sub_dirs_only):
				for f in files:
					file_name = os.path.join(root, f)
					self.backup_helper(file_name, **kwargs)
					self.shunt(f, root)

	def shunt(self, filename, directory):
		source = os.path.join(directory,filename)

		#create target directory if it doesn't exist
		target_directory = os.path.join(directory, SimpleBackup.PROCESSED_DIR)

		if not os.path.exists(target_directory):
			os.mkdir(target_directory)	

		#move file from source to target
		target = os.path.join(target_directory, filename)
		shutil.move(source, target)
