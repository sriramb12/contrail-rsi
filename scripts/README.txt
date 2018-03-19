This folder contains the scripts which will be run by various contrail nodes)
a contrail node can be
  o Controller
  o Config
  o Analytics
  o vrouter
These will be sent to the specified node via scp 

Following is the file org for scripts:
  
 .../rsi/rsi.py  
   Python script which orchestrates RSI by logging into a contrail node (specified in command line)
    
  Requires:
    python
    scp
    root credentials for the target node

 .../rsi/scripts/rsi.sh
   A Bash script file which runs on the node (logged in by rsi.py) 
   This executes some common contrail commands and invokes below set of scripts 

Each node has a couple of scripts:
  node.sh
     Contains specific commands which may not be runnable in straight forward method. Example: flow -r (needs some logic to terminate)

  node-cmds
     contains commands which can be run straight away 
   ex:
     uname -a
     contrail-status
     etc

 
