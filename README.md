# contrail-rsi
contrail-rsi is a collection of python/bash-scripts to gather necessary information from a given contrail node, intended for contrail troubleshooting
**Tested on Ubuntu Linux**

### Installation:

**git clone https://github.com/sriramb12/contrail-rsi**
It will download the tool to your system

Requires:
  python 2.7 and the python modules: getpass paramiko scp 

####     Install Tip:
__'pip' can be used to install above modules__
####  Ex:
**pip install getpass paramiko scp** 
###    Usage:
      Navigate to the folder where 'rsi.py' is present 
      `cd contrail-rsi`
      ./rsi.py [node-IP]
##### Exmple:
  ./rsi.py 10.219.90.82
Known Issues:
  * Does NOT work on windows git-bash (use powershell instead)
  * At times, the RSI session is getting hung (no activity seen on contrail node)

## TODOs:
  * Add introspect outputs
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
