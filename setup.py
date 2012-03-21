#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
	name = "mkondo",
	version = "0.0.3",
	description = "Mkondo is a library that helps download Twitter Streaming API data and manage that data.",
	long_description = " Contains code that complies with the Streaming API T&C. Contains code to backup that data, shunt it around, and finally, analyze portions of it", 
	author = "Shashank Khandelwal", 
	author_email = "shrew@alumni.cs.utexas.edu", 
	url="http://salathegroup.com", 
	packages = find_packages(exclude="test"),
	zip_safe = False
)
