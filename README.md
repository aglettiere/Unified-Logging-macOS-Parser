# SystemLogParser

### Purpose
The system.log files (including system.log and the gzipped archived system log files) for macOS display a variety of warning messages from the Mac's software. This script organizes the data from these files and builds them into CSV and JSON files.

### Overview
System.log describes issues regarding the computer system, DNS, and networking instances. The file is stored as a .log text file and the old rotated files are stored as gzip files. When the total files hit 50MB, the oldest gets deleted. These files can illuminate important details about the computer's system processes and provide evidence of suspicious activity.

### Compatibility
The parser supports Python 2.7.

### Usage
To run the file against your local machine, you can run the following command:
```
sudo python SystemLogParser.py
```
This command will output a CSV file to the current working directory from which the .py file was run.

To create a JSON file include the -j or --jsn argument:
```
sudo python SystemLogParser.py -j
```

To specify the output of the file include the -o or --output argument as seen below:
```
sudo python SystemLogParser.py -o /output/path
```

### Output
The program provides the option to produce a CSV or JSON output. The CSV headers include the date of the message, the time (in 24-hour mode), the computer name, the name of the process or app that sent the message, the process ID, and the actual message.

The JSON file includes the fields as they appear below:
```
{"Process Name": "systemstats", 
"Process ID": "50", 
"Computer Name": "Allisons-MacBook-Pro", 
"Time": "05:33:25", 
"Date": "Jul 31", 
"Message": "assertion failed: 17G65: systemstats + 914800 [D1E75C38-62CE-3D77-9ED3-5F6D38EF0676]: 0x40 "}
```
