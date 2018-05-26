#It performs 3 operations
# a. Omits specific log files 
excludedFiles='excludedlogs.txt'
#loganalysis-tbd.txt
excludedFilesList =[]
# b. Filters out unwanted logs from 
filterFile='logfilters.txt'
# c. generates a list of all logs in /var/logs 
logFileList='allLogs.txt'
# ALL output is written to the folder specified in the 1st (and only) argument 

#TODO
# use log file attributes (os.stat) to a greater extent (such as created time and so on)
# analyze logs (specific methods for a given log file)
#  Ex: /var/log/haproxy.log has a lot of repetitive logs with different clients. can we crunch/summarize and learn?

logFileSizeThreshold = 1000*1024
import os
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--outdir", help="output folder")
parser.add_argument("-i", "--indir", help="log folder")
parser.add_argument("-d", "--debug", action='store_true', help="debug")
args = parser.parse_args()

debug=False
if args.debug:
 debug=True
 
outdir='.'
if args.outdir:
 outdir=args.outdir
 
indir='/var/log'
if args.indir:
 indir=args.indir

try:
  os.system("mkdir " + outdir)
except:
  pass

logFilters = {}
filteredLogFiles =[]

f = open(filterFile)
linenum=0
for line in f:
  linenum += 1
  if line[0] is not '#' :
      try:
       (key, lst) = line.rstrip('\n').split(':')
       val=(lst.split(','))
       logFilters[key] = val
       filteredLogFiles.append( key.split('/')[-1])
      except:
        if debug:
         print 'ignoring line ', linenum
        pass
  else:
        if debug:
         print 'ignoring line ', linenum
        

try:
 f = open(excludedFiles)

 for exFile in f:
    excludedFilesList.append(exFile.rstrip('\n'))

except:
 if debug:
   print 'no filters exist'

logFileCount=1
filterLogFileList=[]
for root, dirs, files in os.walk(indir):
    folder= outdir
    folder += os.path.join(root, '')
    cmd = "mkdir -p " + folder 
    
    os.system(cmd)
    for logfile  in files:
      if logfile .endswith(".log") :
        f = logfile
        lf = (os.path.join(root, logfile ))
        if  debug and f in filteredLogFiles:
           print "skipping ", f
        if  f not in logFilters.keys() and  lf not in excludedFilesList:
          sz = os.stat(lf).st_size
          if  sz > logFileSizeThreshold:
            print 'skipping ', lf, "size ", sz/(1024*1024), "M, is too big?"
          if  sz < logFileSizeThreshold and lf not in logFilters.keys() and  lf not in excludedFilesList:
           cmd = "cp " + lf + " " + folder
           os.system(cmd)
           logFileCount+=1

print 'number of log files copied:', logFileCount

count = 0
for logfile in logFilters:
   patterns = logFilters[logfile]
   if not os.path.isfile(logfile): 
     continue
   print 'applying filters on ', logfile
   cmd = "grep -v " + patterns[0] + " " + logfile + ' | grep -v ^$ '
   if len(patterns) > 1:
     for p in patterns[1:] :
       cmd += (" | grep -v " + p)
   cmd += " > " + outdir + logfile
   if debug:
     print 'processing', cmd
   os.system(cmd)

