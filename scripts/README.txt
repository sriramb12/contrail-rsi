This folder contains the scripts which will be run by various contrail nodes)
a contrail node can be
  o Controller
  o Config
  o Analytics
  o vrouter
These will be part of the tool and uploaded from host automatically


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

Each node has a 2 types of scripts:
1. Files with names in "*-cmds" format. Use these if you simply want to add a direct command (etc: contrail-status) . This will be useful as the commands are logged and errors are tracked by rsi.sh
   Ex: vrouter-cmds
     contains commands which can be run straight away 
   ex:
     uname -a
     contrail-status
     etc
 
2. They run on their own
    Use these when we need some customization. The run time logging is upto the script
  node.sh
     Contains specific commands which may not be runnable in straight forward method. Example: flow -r (needs some logic to terminate)

For ease of analysis of RSI report, divide the commands into multiple files
