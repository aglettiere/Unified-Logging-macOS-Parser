'''
@ author: Allison Lettiere
@ email: allisonglettiere@gmail.com
'''

import sys
import json
import csv
import glob
import gzip
import os
import argparse
import gzip
import shutil


class table_output:

	def __init__(self, name, table_headers, datatype, output_directory = './'):
		self.name = name
		self.table_headers = table_headers
		self.datatype = datatype
		self.output_name = self.name + '.' + self.datatype
		self.output_directory = output_directory
		self.data_name = os.path.join(output_directory, self.output_name)

		##initialize output files
		if self.datatype == 'csv':
			with open(self.data_name, 'wb') as file:
				writer = csv.writer(file)
				writer.writerow(table_headers)
		elif self.datatype == 'jsn':
			with open(self.data_name, 'wb') as file:
				pass

	##method to write data to the files, determines write method based upon type of output file
	def write_data(self, data):
		if self.datatype == 'csv':
			with open(self.data_name, 'a') as file:
				writer = csv.writer(file)
				writer.writerow(data)
		elif self.datatype == 'jsn':
			zipped_data = dict(zip(self.table_headers, data))
			with open(self.data_name, 'a') as file:
				json.dump(zipped_data, file, indent = 2)


def process_input():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", default = "./", help = "Location for completed output file (must be a valid directory on your device).", required = False)
	parser.add_argument("-j", "--json", help = "Output data in a json file", required = False, action = 'store_true')
	args = parser.parse_args()
	##check if the output is valid, reprompt if not
	if args.output:
		while os.path.isdir(args.output) == False:
			args.output = input("Please enter a valid directory: ")

	final_file = os.path.join(args.output, "SystemLogParser_output")

	table_headers = ['Date', 'Time', 'Computer Name', 'Process Name', 'Process ID', 'Message']

	if args.json:
		file_format = 'jsn'
	else:
		file_format = 'csv'

	##create new output object
	newParsedLog = table_output("SystemLogParser_output", table_headers, file_format, args.output)

	SystemLogParser(newParsedLog);


def SystemLogParser(newParsedLog):
	##check if the program is running with Administrator access
	if os.geteuid() != 0:
		print "Running parser without sudo access, but attempting to parse files on disk. This may fail without sudo access."
		print "If the parser fails, please use the sudo command."

	##unzip gzipped log files
	zipNumber = 0
	if not os.path.exists("/var/log/unzippedLogs"):
		os.makedirs("/var/log/unzippedLogs")
	for file in list(glob.glob('/var/log/system.log.*.gz')):
		with gzip.open(file, 'rb') as file_in:
			with open("/var/log/unzippedLogs/system.log." + str(zipNumber), 'w') as file_out:
				shutil.copyfileobj(file_in, file_out)
		zipNumber+=1

	allLogFiles = glob.glob("/var/log/unzippedLogs/system.log*") + glob.glob("/var/log/system.log")
	
	if len(allLogFiles) < 1:
		print "No log files found."
	else:
		print "Found {0} system log files to parse.".format(len(allLogFiles))
	
	openAndProcessFiles(allLogFiles, newParsedLog)


def openAndProcessFiles(allLogFiles, newParsedLog):
	for logFile in allLogFiles:
		with open(logFile, 'rb') as logs:
			logLines = logs.read().splitlines()
		
		with open(newParsedLog.data_name, 'a') as file:
			##loop through each line of the log file
			for index, line in enumerate(logLines):
				if line[0] != '\t':
					splitLocation = 0
					split_0 = line.split(' ')
					
					##some of the files have two spaces between the month name and the date, some have one 
					##this adjustment handles this difference
					if(split_0[1] == ''):
						splitLocation += 1
					
					date = split_0[0] + " "+ split_0[splitLocation + 1]
					time = split_0[splitLocation + 2]
					name = split_0[splitLocation + 3]
					
					##checks for lines that are messages indicating previous line repeats
					if name[0] == '-' and name[1] == '-' and name[2] == '-':
						repeats = int(split_0[splitLocation + 7])
						for i in range(repeats):
							newParsedLog.write_data([date, time, computerName, processName, processID, message])
						break
					else:
						computerName = name
					
					processNameandID = split_0[splitLocation + 4]
					processName = processNameandID.split('[')[0]
					processID = processNameandID.split('[')[1][:-2]
					
					##rejoin the words of the message to create the full string
					string = split_0[splitLocation + 5:]
					message = ''
					for word in string:
						message += word + " "

					##handle tabbed lines and append to previous message
					while logLines[index+1][0] == '\t':
						message += " "+ logLines[index+1][1:]
						index += 1

					newParsedLog.write_data([date, time, computerName, processName, processID, message])

				
if __name__ == "__main__":
	process_input()



