# contrail-rsi
contrail-rsi is a collection of python/bash-scripts to gather necessary information from a given contrail node, intended for contrail troubleshooting
**Tested on Ubuntu Linux**

### Installation:

**git clone https://github.com/sriramb12/contrail-rsi**
It will download the tool to your system

Requires:
  'root' access to the contrail-node
  python 2.7 and the python modules: getpass paramiko scp 

####     Install Tip:
__'pip' can be used to install above modules__
<<<<<<< HEAD

#### Usage:
*./rsi.py <nodeIP>*

####  Ex:

root@controller-1:~/contrail-rsi# ./rsi.py 10.219.90.76
Password: 
Warning: password is hardcoded! use getpass()
logging to 10.219.90.76
10.219.90.76 is a contrail node
OK
RSI saved to:  CFTSBM6CMP-1526539840.tgz

=======
####  Ex:
>>>>>>> 803f7559af2b2fb7e5189aabf0fe5bf45c309dc6
**pip install getpass paramiko scp** 
###    Usage:
      Navigate to the folder where 'rsi.py' is present 
      `cd contrail-rsi`
      ./rsi.py [node-IP]
##### Exmple:
  ./rsi.py 10.219.90.82
Known Issues:
  * Does NOT work on windows git-bash (use powershell instead)
  * On rare occassions, RSI session is returning with no data (no activity seen on contrail node for a minute)

## TODOs:
  * Add introspect outputs
  * Make it work for 'non-root' users as well. Need to log some contrail ER defects 
  * RSI Analysis: Build analysis engine to figure out any anamolies in
       configuration, logs, runtime data (using introspect outputs)
  * UX related:
     During contrail-rsi run, show progress of RSI (to show if it is working or hung)
  * Add more commands to each module for a comprehensive set of module status outputs 
     Ex: _add commands related to cassandra, zookeeper etc_
  * Configurabilty in Logs, better filters, more parameters to logging module 
`      contrail-rsi/scripts/logging`

### Customize/Configure:
  contrail-rsi is highly extensible and configurable to get relevant information from the node of interest 
#### Node level RSI configuration:
  Please take a look at: 
`      contrail-rsi/scripts/<module> folders to customize`
       Many commands need to be added which are usually requested from customer team
#### Log configuration:
  Contrail logs are volumious and rollover quickly. This tool enables JTAC Engineer to add some filters
  Please take a look at 
`      contrail-rsi/scripts/logging/logfilters.txt ` to customize filters
`      contrail-rsi/scripts/logging/excludedlogs.txt ` to add/edit/delete/  to change what log files can be omitted
