#!/usr/bin/env python

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class SimpleStorage:

	def __init__(self, aws_access_key, aws_secret_key):
		self.conn = S3Connection(aws_access_key, aws_secret_key)

	def list_buckets(self):
		return self.conn.get_all_buckets()

	def create_bucket(self, bucket_name):
		'''Creates and returns a bucket. Bucket names are unique across Amazon S3.'''
		return self.conn.create_bucket(bucket_name)

	def get_bucket(self, bucket_name):
		return self.conn.get_bucket(bucket_name)

	def delete_bucket(self, bucket_name):
		bucket = self.conn.get_bucket(bucket_name)
		bucket.delete()

	#def send_file(self, file_name, bucket_name, path_prefix):
	def send_file(self, file_name, **kwargs):
		""" Send the file specified by `file_name` to S3 for storage. """
		bucket_name = kwargs['bucket_name']
		path_prefix = kwargs['path_prefix']

		bucket = self.get_bucket(bucket_name)
	
		k = Key(bucket)
		key = file_name[len(path_prefix):len(file_name)]

		if key[0] != os.path.sep:
			key = os.path.sep + key

		k.key = key
		k.set_contents_from_filename(file_name)
