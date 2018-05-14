exclpatternFile='exPattern.txt'

logdict = {}

with open(exclpatternFile) as f:
    for line in f:
       (key, val) = line.rstrip('\n').split(':')
       logdict[key] = val

print logdict.keys()


for f in logdict():
   print f
   #if str(f in logFileList:
      #print 'processing ', f
