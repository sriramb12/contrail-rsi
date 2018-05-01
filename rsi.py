#!/usr/bin/python
###############################################################
#
# Contrail rsi tool for collecting a node information
# Usage:
#    ./rsi.py <node ip>
#  Ex: 
#      ./rsi.py 10.219.90.82
#  Output:
#     collects specified commands( see scripts/ folder within)
#     as a compressed tar file 
#        saves it locally rsi-<ddMMMyy-hhmmss>.tgz
#     Ex: rsi-20Mar18-121953.tgz  
###############################################################

import os
import sys
import getpass
import os.path
import paramiko
from paramiko import SSHClient
from scp import SCPClient

archivedir='scripts'
archive='scripts.tar'

#TBD: traverse all tenants 
#for now, specific tenant information is captured
tenantcred='tenant.cred'

def printout(f):
 for line in f:
   print line

def checkPing(host):
    response = os.system("ping -c 1 -t2 " + host + "> /dev/null")
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus 

def checkServer(server, user, pwd, chkcmd):
 if not checkPing(server):
  print server, 'not reachable?'
  print 'exiting'
  exit(0)    
 proxy = None
 ssh = paramiko.SSHClient()
 ssh.load_system_host_keys()
 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 try:
   ssh.connect(server, username=user, password=pwd, timeout=2)
   stdin, stdout, stderr = ssh.exec_command(chkcmd)
 
   for line in stderr:
     if 'not' in line:
       print server, 'is not a contrail node?'
       ssh.close()
       return False
   c=0
   for line in stdout:
     c+=1
   if not c:
       print server, 'is not running contrail services?'
       ssh.close()
       return False
   print server, 'is a contrail node'
   return True
   
   return True
 except paramiko.AuthenticationException:
   print("Authentication failed?")
   return False
 except:
   print("unknown error")
   print server, 'is a contrail node?'
   return False
 ssh.close()

def runRsi(server, file, user, pwd):
 global tenantcred
 proxy = None
 ssh = paramiko.SSHClient()
 #ssh.known_hosts = None
 ssh.load_system_host_keys()
 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 ssh.connect(server, username=user, password=pwd)

 # SCPClient takes a paramiko transport as its only argument
 scp = SCPClient(ssh.get_transport())
 stdout = ssh.exec_command('mkdir -p rsi 2>>/tmp/err')
 targetfile='/root/rsi/'+file
  
 scp.put(file, targetfile)
 if os.path.isfile(tenantcred):
   scp.put(file, tenantcred)
 
 
 #remove local scripts tarball
 os.system('rm scripts.tar')
 
 stdout = ssh.exec_command('tar xf ' + targetfile + ' -C rsi/ >> rsi/rsi.log')
 stdout = ssh.exec_command('rsi/scripts/rsi.sh')[1]
 printout(stdout)
 scp.get('/root/rsi/rsi.tgz', 'rsicollected.tgz')
 stdout = ssh.exec_command('rm /root/rsi/rsi.tgz')
 stdout = ssh.exec_command('rm /root/rsi/rsi.tar')
 print('Rsi collected and extracted as following :')
 os.system('tar --strip-components 1 -zxvf ' +'rsicollected.tgz') 
 os.system('rm rsicollected.tgz')
 os.system('rm -rf /root/rsi/scripts')

 #stderr = ssh.exec_command('bash test.sh')[2]

def checkScripts():
 #print 'checking'
 if not os.path.isdir(archivedir):
  return False
 #print archivedir, 'is found..'
 return True

if not checkScripts():
 print archivedir, 'is not found!'
 exit(0)
user='root'
server=''

if len(sys.argv) < 2:
   print 'Enter Node FQDN/Address:',
   server = raw_input()

else:
   server = sys.argv[1]

user = 'root'
#Comment this line
pwd = 'Juniper'
#Uncomment this line
#pwd = getpass.getpass()
print 'Note: password is hardcoded! use getpass()'
print 'logging to', server




os.system('tar cf ' + archive + ' scripts/')

if checkServer(server, user, pwd, 'contrail-status'):
  print "OK"
  runRsi(server, archive, user, pwd)
else:
  print('exiting');
