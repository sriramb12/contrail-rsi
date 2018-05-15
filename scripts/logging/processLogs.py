#It performs 3 operations
# a. Omits specific log files 
excludedFiles='excludedlogs.txt'
#loganalysis-tbd.txt
excludedFilesList =[]
# b. Filters out unwanted logs from 
filteredFiles='logfilters.txt'
# c. generates a list of all logs in /var/logs 
logFileList='allLogs.txt'
# ALL output is written to the folder specified in the 1st (and only) argument 

#TODO
# use log file attributes (os.stat) to a greater extent (such as created time and so on)
# analyze logs (specific methods for a given log file)
#  Ex: /var/log/haproxy.log has a lot of repetitive logs with different clients. can we crunch/summarize and learn?

logFileSizeThreshold = 10*1024
import os
import sys

try:
 if len(sys.argv) < 2:
  exit(0) 
 folder= sys.argv[1] + '/'
 Folder= sys.argv[1] + '/'
 os.system("mkdir " + folder)
except:
 print 'mkdir exception'
 exit(0)

logFilters = {}


with open(filteredFiles) as f:
    for line in f:
      if line[0] != '/':
          print 'ignoring ', line
          continue
      (key, lst) = line.rstrip('\n').split(':')
      val=lst.split(',')
      logFilters[key] = val

with open(excludedFiles) as f:
  for exFile in f:
    excludedFilesList.append(exFile.rstrip('\n'))

print excludedFilesList

prefix = "/var/log/"
copyCount = 0
filterLogFileList=[]
for root, dirs, files in os.walk(prefix):
    folder= sys.argv[1]
    folder += os.path.join(root, '')
    cmd = "mkdir -p " + folder 
    
    os.system(cmd)
    for logfile  in files:
        f = logfile.split('/')[-1]
        l = (os.path.join(root, logfile ))
        if logfile .endswith(".log") :
          sz = os.stat(l).st_size
          if  sz > logFileSizeThreshold and l not in logFilters.keys() and  l not in excludedFilesList:
           cmd = "cp " + l + " " + folder
           
           if copyCount < 10:
            os.system(cmd)
            copyCount += 1
          #  print cmd, "copied ", l
            os.system("ls -l " + l )
        os.system("ls -l " + l + " >> " + Folder + logFileList)

print 'number of files for copy:', len(logFileList)
print 'number of filter files found ', len(filterLogFileList)


folder= sys.argv[1]
count = 0
for f in logFilters:
   patterns = logFilters[f]
   cmd = "grep -v " + patterns[0] + " " + f + ' | grep -v ^$ '
   if len(patterns) > 1:
     for p in patterns[1:] :
       cmd += (" | grep -v " + p)
   cmd += " > " + folder + f
   print 'processing\n', cmd
   os.system(cmd)
print 'The following log files are filtered:'
for f in logFilters:
   print f
