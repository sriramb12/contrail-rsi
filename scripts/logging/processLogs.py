# This filters logs folder based on known log spammers
#It does 2 kinds of filtees
# a. Omits log file 
excludedFiles='skipLogFiles.txt'
# b. Omits unwanted logs from 
exclpatternFile='skipLogs.txt'
excludedFilesList =[]

import os
import sys
try:
 if len(sys.argv) < 2:
  exit(0) 
 folder= sys.argv[1]
 os.system("mkdir " + folder)
except:
 print 'mkdir exception'
 exit(0)

with open(excludedFiles) as f:
  for exFile in f:
    excludedFilesList.append(exFile.rstrip('\n'))

print excludedFilesList

prefix = "/var/log/"
count = 0
logFileList=[]
for root, dirs, files in os.walk(prefix):
    folder= sys.argv[1]
    folder += os.path.join(root, '')
    cmd = "mkdir -p " + folder 
    os.system(cmd)
    for file in files:
        if file.endswith(".log"):
             logFileList.append(os.path.join(root, file))

print 'number of files found ', len(logFileList)



logdict = {}

with open(exclpatternFile) as f:
    for line in f:
       (key, val) = line.rstrip('\n').split(':')
       logdict[key] = val

folder= sys.argv[1]
for f in logFileList:
  if f in excludedFilesList:
    print 'skipping log file:', f
    pass
  for k in logdict.keys():
   if k in f:
      print 'processing ', f
      os.system
      for patterns in logdict.values():
         pattern = patterns.split(",")
         cmd = "grep -v " + pattern[0] + " " + f
         print cmd
         if len(patterns) > 1:
          for p in pattern[1:] :
           cmd += (" | grep -v " + p)
          cmd += " > " + folder + f
          os.system(cmd)
