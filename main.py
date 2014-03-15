#!/usr/bin/python

import math
import logging
import Queue
import threading

# Bit Constants
DIRTY	= 0
VALID	= 1
TAG 	= 2
LINE	= 3

instructionQueue = Queue.Queue()

class cacheSim(threading.Thread):

	# Constructor Method
	def __init__( self ):
		# Init base class (Thread name = CACHESIM)
		threading.Thread.__init__(self, name='CACHESIM')
		# Class Properties (Public)
		self.memorySize = 2**20
		self.cacheSize = 2**16
		self.cacheWays = 1
		self.wordWidth = 32 #math.log(self.cacheSize, 2)
		self.cacheLineLength = 1
		self.dataLength = self.wordWidth
		self.indexWidth = math.log((self.cacheSize/(self.cacheWays * self.cacheLineLength * 4)),2)
		self.tagWidth = int(math.log(self.memorySize, 2) - self.indexWidth-4)
		self.cacheLines = (self.cacheSize / (self.cacheLineLength * 4))
		self.memoryLines = (self.memorySize / (self.cacheLineLength * 4))

		# Generate Bitmasks
		self.indexMask = self._generateIndexMask()
		self.tagMask = self._generateTagMask()

		# Call cache init method
		self._initCache()
		# Call memory init method
		self._initMainMemory()

	## PRIVATE METHODS

	def _initCache(self):
		logging.info('Initialising Cache of %s lines', self.cacheLines)
		# Initialise cache memory as list
		# using list comprehensions
		# 4 by (self.cacheLines) 'array'
		self.cacheMemory = [[False, False, None, None] for y in range(self.cacheLines)]
		logging.info('Cache initialised')

	def _initMainMemory(self):
		logging.info('Initialising Main Memory %s lines', self.memoryLines)
		# Initialise main memory as empty list
		# using list comprehensions
		# as type NONE
		self.mainMemory = [[None, None] for y in range(self.memoryLines)]
		logging.info('Main Memory initialised')

	def _int2Bin(self, s):	
		return str(s) if s<=1 else bin(s>>1) + str(s&1)

	# Generate Index Mask for CPU produced addresses
	def _generateIndexMask(self):
		binIndex = ''
		bit = self.wordWidth
		maskMax = int(self.wordWidth - self.tagWidth)
		maskMin = int(self.wordWidth - (self.tagWidth + self.indexWidth))
		print maskMax, maskMin
		while (bit > 0):
			if (bit < maskMax) and (bit > maskMin):
				binIndex = binIndex + "1"
			else:
				binIndex = binIndex + "0"
			bit -= 1
		logging.info('Index bitmask: %s', hex(int(binIndex, 2)))
		print binIndex
		return hex(int(binIndex, 2))

	# Generate Tag Mask for CPU produces addresses
	def _generateTagMask(self):
		binTag = ''
		print self.tagWidth
		bit = self.wordWidth
		while (bit > 0):
			if (bit > (self.wordWidth - self.tagWidth)):
				binTag = binTag + "1"
			else:
				binTag = binTag + "0"
			bit -= 1
		logging.info('Tag bitmask: %s', hex(int(binTag, 2)))
		print binTag
		return hex(int(binTag, 2))

	# Main execution routine
	# Contains majority of CACHE operations
	def _executeQueue(self):
		while not instructionQueue.empty():
			instruction = instructionQueue.get()
			logging.debug('Executing instruction: %s', instruction[0])
			# MASK TAGWIDTH BITS (Need tagwidth bitmask),
			# MASK INDEXWIDTH BITS (Need indexwidth bitmask)
			print instruction[1]
			index = self._generateIndex(instruction[1])
			tag = self._generateTag(instruction[1])
			print index, tag
			# Read operation
			if ( instruction[0] == 'R' ):
				logging.debug('Reading address %s', instruction[1])
				for way in range(self.cacheWays):
					
					if ( self.getValidBit(index) and self.getTag(index) ):
						logging.info('Hit: %s', index)
			# Write operation
			elif ( instruction[0] == 'W' ):
				logging.debug('Writing data %s to address %s', instruction[2], instruction[1])
			else:
				logging.warning('Invalid instruction: %s', instruction)	
	
	def _hex2int(self, hexa):
		return int(hexa, 0)
	
	def _generateIndex(self, address):
		return int(int(address, 16) & int(self.indexMask, 16))
	
	def _generateTag(self, address):
		return int(int(address, 16) & int(self.tagMask, 16))	
	
	# Method to read from memory
	def _readFromMemory(self, memoryLine, word):
		logging.log('Read from memory: %s', self.mainMemory[memoryLine][word])

	# Method to write to cache
	def _writeToCache(self, index, tag, word, data):
		self.cacheMemory[index][word] = data
		self.cacheMemory[index][TAG] = tag
		self.cacheMemory[index][DIRTY] = True
		self.cacheMemory[index][VALID] = True
		logging.log('Written to cache: %s', word)

	# Method to writeback to memory
	# Writes [index][word] from cache to main memory
	def _memoryWriteBack(self, memLine, index, word):
		self.mainMemory[memLine] = self.cacheMemory[index][word]
		self.setDirtyBit(index, 0)

	# Method to evict cache line
	def _evictCacheLine(self, index):
		self.cacheMemory[index][LINE] = ""
		self.cacheMemory[index][TAG] = ""
		self.cacheMemory[index][DIRTY] = False
		self.cacheMemory[index][VALID] = False
		logging.info('Cache line %s evicted', index)

	# PUBLIC METHODS (BIN?)
	
	# Method to get dirty bit of cache line (GET)
	def getDirtyBit(self, cacheLine):
		return self.cacheMemory[cacheLine][DIRTY]
	
	# Method to set dirty bit of cache line (SET)
	def setDirtyBit(self, cacheLine, dirtyBit):
		self.cacheMemory[cacheLine][DIRTY] = dirtyBit
		logging.debug('Set dirty bit of %s to %s', cacheLine, dirtyBit)
	
	# Method to get valid bit of cache line (GET)
	def getValidBit(self, cacheLine):
		return self.cacheMemory[cacheLine][VALID]

	# Method to set valid bit of cache line (SET)
	def setValidBit(self, cacheLine, validBit):
		self.cacheMemory[cacheLine][VALID] = validBit
		logging.debug('Set valid bit of %s to %s', cacheLine, dirtyBit)

	# Method to get TAG of cache line (GET)
	def getTag(self, cacheLine):
		return self.cacheMemory[cacheLine][TAG]

	def run(self):
		self._executeQueue()

class cpuSim(threading.Thread):
	# Constructor method
	def __init__(self):
		# Init thread base class
		threading.Thread.__init__(self, name='CPUSIM')
		# Open file "trace.txt", read only
		self._fileName = 'trace.txt'
		self._traceFile = open(self._fileName, 'r')
		logging.info('Trace file %s open', self._fileName)

	# PRIVATE METHODS
	
	# Method to read trace file
	def _generateTraceQueue(self):
		# For each line in file
		for line in self._traceFile.readlines():
			# Delimit whitespace and put list on queue
			instructionQueue.put(line.split())
			logging.debug('Read line: %s', line.strip())
		logging.info('File: %s has been read', self._fileName)
		
	def run(self):
		logging.info('CPU Queue Start')
		self._generateTraceQueue()
		logging.info('CPU Queue Finished')

def main():
	# Overwrite log file 
	logging.basicConfig(filename='cache.log', filemode='w', level=logging.DEBUG)
	# Instansiate CPU Simulator Thread
	logging.info('Initialising Threads')
	CpuSimulator = cpuSim()	
	CacheSimulator = cacheSim()
	# Start Threads
	logging.info('Starting Threads %s %s', CpuSimulator.name, CacheSimulator.name)
	CpuSimulator.start()	
	CacheSimulator.start()
	logging.info('Threads %s %s running...', CpuSimulator.name, CacheSimulator.name)
		
if __name__== "__main__":
	main()
