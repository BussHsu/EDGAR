1. Developed under python 3.5

2. Library dependencies: 
	I only use the standard python-dev libraries such as collections, datetime, os, sys.

3. Instruction to use:
	Should work well with the provided testing framework. I just follow the input format for python execution command in run.sh file.

4. Software Overview
	4.1 Sessionization.py: the main file, has SessionMonitor class that keep track of each connection session. It would print a line to output file when session expires, and when the reach_EOF method is called, it'll print the whole list of sessions. The session tracking table is implemented with Ordereddict data structure.
	4.2 data_loader.py: in utils module, this file defines the DataLoader class that read in the csv input and feed the data row one line by one line.
	4.3 def_struct.py: in utils module. this file defines several data structures: DateTime, WebPage, ConnectData. DateTime is a wrapper for python native datetime.datetime class, used to track users' login and log out time. WebPage records cik, accession, extension fields that uniquely identifies a document. It also has a hash function so can be added to a set when in tracking the session, thus automatically prevent counting same document multiple times. ConnectData is the combination of ip, DateTime and WebPage, which corresponds to a row of data. 
