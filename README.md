cacheSim
========

A Cache Simulator for a Microprocessor Architecture Coursework.

Simulates both direct mapped cache or set associative of 2,4 or 8 ways.


 Written in Python for version 2.7.5+
 Developed and tested with Python 2.7.5
 Should work with Python 3+

 Short note on Pythonic OOP:
===========================
 
 By design, Python does not support Private methods.
 However, any method prepended with an underscore
 indicates an internal method. The interpreter does not
 react to this, but is in place so that internal methods are not
 accidentally accessed, as one would have to break convention of
 using an underscored method from outside the class.

 Microprocessor Architecture Coursework 2: Cache Simulator

 Based on a simple Von Neumann Architecture
 using CPU instructions located by default
 in trace file "trace.txt"
 Generates Log File "cache.log" provided by Python logging library

 BASIC OPERATION:
================
 Two thread based classes: 'CacheSim' and 'CpuSim'
 CpuSim reads the tracefile into memory and sends them to global FIFO
 Queue object 'instructionQueue'.

 CacheSim pops the first item off the queue before simulating the
 function of a cache, as defined by the input parameters.
 This process will be repeated until the Queue is empty, at which point
 the program will exit.

 LOG FILE:
=========
 The log file will by default be set to INFO verbosity. However, DEBUG
 messages may be displayed also by changing the logging value to:
 'level = logging.DEBUG'.

 By default, each run of the simulator will clear the logfile and
 overwrite it. If this is not desired, you must change the filemode
 from 'W' (write) to 'R' (read).

 Each log entry it prepended with the level (i.e. INFO, DEBUG, WARNING or ERROR)
 followed by the 'branch'. For this project, all branches are 'root'.
 Log entries generated by the a thread will also include the thread name,
 either CPUSIM or CACHESIM for the respective threads.

 After this will be the message. A cache HIT will be signified by 'HIT!',
 and ANY cache misses signified with 'MISS'.
 In debug mode, addresses may be represented in their hex form,
 as this is how they have been read in.
 Most logging outputs will refer to binary information in the
 integer form, including index and tag values.

 If a value has not been assigned, the pythonic type 'None' will be
 allocated as there is nothing to assign. Please consider that in a real
 system, this may just be an invalid or garbled value containted in
 memory that has no functional value.
