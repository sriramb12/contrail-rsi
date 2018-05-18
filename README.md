# contrail-rsi
contrail-rsi is a python/bash-script tool to collect necessary information from a given contrail node. 
it is tested on Ubuntu Linux and Windows powershell
place for contrail-scripts useful for users, jtac

### Installation:

**git clone https://github.com/sriramb12/contrail-rsi**
It will download the tool to your system

Requires :
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

  1. Does NOT work on windows git-bash (use powershell instead)
  2. At times, the RSI session is getting hung (no activity seen on contrail node)


## TODOs:

  * UX related:
     During contrail-rsi run, show progress of RSI (to show if it is working or hung)

  * Add more commands to each module for a comprehensive set of module status outputs 
     Ex: _add commands related to cassandra, zookeeper etc_

  * Configurabilty in Logs, better filters, more parameters to logging module 
`      contrail-rsi/scripts/logging`

### Configuration:
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
  
