# contrail-rsi
contrail-rsi is a python/bash-script tool to collect necessary information from a given contrail node. 
it is tested on Ubuntu Linux and Windows powershell
place for contrail-scripts useful for users, jtac

Requires :

  python 2.7 and the python modules: getpass paramiko scp 

  Tip: 'pip' can be used to install above modules
  Ex:
`      pip install getpass paramiko scp `

Known Issues:

  Does NOT work on windows git-bash (use powershell instead)


## TODOs:

  1. print updates on progress of RSI (to show if it is working or hung)

  2. At times, the RSI session is getting hung
