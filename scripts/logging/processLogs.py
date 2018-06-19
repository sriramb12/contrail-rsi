#It performs 3 operations
# a. Omits specific log files 
excludedFiles='excludedlogs.txt'
#loganalysis-tbd.txt
excludedFilesList =[]

# b. removes unwanted logs from 
excFilterFile='exclPatterns.txt'

# c. fetches only interesting logs
incFilterFile='inclPatterns.txt'

# d. generates a list of all logs in /var/logs 
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

def applyFilters(includeFlag, logFilters):
 flag = '-v'
 global debug
 if includeFlag:
   flag = ''
 print 'applyFilters ', flag
 for logfile in logFilters:
   print logfile
   patterns = logFilters[logfile]
   if not os.path.isfile(logfile): 
     continue
   print 'applying filters on ', logfile
   cmd = "grep  " + patterns[0] + " " + logfile + ' | grep  -v ^$ '
   if len(patterns) > 1:
    for p in patterns[1:] :
      if not include:
       cmd += (" | grep -v " + p)
      else:
       cmd += (" | grep -e " + p)
   cmd += " > " + outdir + logfile
   if debug:
     print 'processing ', logfile, cmd
   os.system(cmd)

try:
  os.system("mkdir " + outdir)
except:
  pass

inFilters = {}
exFilters = {}
filteredLogFiles =[]

def parseFilterFile(filterFile):
#Parse custom log filter files and load into corresponding dictionary
# It prepares a dict of include or exclude patterns 
 global debug
 if debug:
   print 'parse filters', filterFile
 f = open(filterFile)
 logFilters = {}
 linenum=0
 for line in f:
   linenum += 1
   #print line
   if line[0] is not '#' :
     try:
       (key, lst) = line.rstrip('\n').split(':')
       val=(lst.split(','))
       logFilters[key] = val
       print line
       filteredLogFiles.append( key.split('/')[-1])
     except:
       if True:
         print 'Exception: ignoring line ', linenum, line
       continue
   else:
      if debug:
         print 'IGnoring line ', linenum , line
      continue
 print logFilters
 return logFilters

inFilters = parseFilterFile(incFilterFile)
exFilters = parseFilterFile(excFilterFile)

print inFilters
print filteredLogFiles
try:
 f = open(excludedFiles)

 for exFile in f:
    excludedFilesList.append(exFile.rstrip('\n'))

except:
 if debug:
   print 'no filters exist'

logFileCount=1
for root, dirs, files in os.walk(indir):
    folder= outdir
    folder += os.path.join(root, '')
    cmd = "mkdir -p " + folder 
    
    os.system(cmd)
    for logfile  in files:
      if logfile .endswith(".log") :
        f = logfile
        lf = (os.path.join(root, logfile ))
        if  f in filteredLogFiles:
          print f
          if debug:
           print "skipping ", f
        if  f not in inFilters.keys() and f not in exFilters.keys() and  lf not in excludedFilesList:
          sz = os.stat(lf).st_size
          if  sz > logFileSizeThreshold:
            print 'Skipping ', lf, "size ", sz/(1024*1024), "M, is too big?"
          if  sz < logFileSizeThreshold and  lf not in excludedFilesList:
           cmd = "cp " + lf + " " + folder
           os.system(cmd)
           logFileCount+=1

print 'number of log files copied:', logFileCount
applyFilters(True, inFilters)
#applyFilters(False, exFilters)
