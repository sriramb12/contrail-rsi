# contrail-rsi
contrail-rsi is a python/bash-script tool to collect necessary information from a given contrail node. 
it is tested on Ubuntu Linux and Windows powershell
place for contrail-scripts useful for users, jtac

Requires :

  python 2.7 and the python modules: getpass paramiko scp 

####  Install Tip:

   'pip' can be used to install above modules

####  Ex:

      *pip install getpass paramiko scp*

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
  RSI tool is highly configurable to get relevant information from the node of interest 

#### Node level RSI configuration:
  Please take a look at: 
`      contrail-rsi/scripts/<module> folders to customize`
       Many commands need to be added which are usually requested from customer team

#### Log configuration:
  Contrail logs are volumious and rollover quickly. This tool enables JTAC Engineer to add some filters
  Please take a look at 
`      contrail-rsi/scripts/logging/logfilters.txt to add/edit/delete/ some filters`
`      contrail-rsi/scripts/logging/excludedlogs.txt to add/edit/delete/ to change what log files can be omitted`
  
