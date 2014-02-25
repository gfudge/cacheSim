#!/usr/bin/python

class Cache(cacheMemorySize, ways, cacheLineLength):

	# Constructor Method
	def __init__(self):
		# Class Properties
		self.memorySize = cacheMemorySize
		self.ways = ways
		self.lineLength = cacheLineLength
		
		self.blockCount = (self.memorySize)/(self.lineLength)
		# Init blocks as hash table
		self.cacheBlocks = {}
		# Flush the cache
		self.flush()

	def flush(self):
		# For all lines in cache
		for line in range(self.memorySize):
			# flush cache line
			#

	def access(self):

	def write(self):
		# write to cache

	def read(self):
		# read from cache
