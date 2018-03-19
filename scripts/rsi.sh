#!/bin/bash
log=rsi/rsi.log
ts=rsi-`date +%d%b%y-%H%M%S`
dir=rsi/$ts
date >> $log
echo Creating `pwd`/$dir >> $log
mkdir $dir
err=$dir/err.txt
LAST_LOG_PERIOD=2

#Change this to another value, depending on need
#This will fetch log files which are changed in last 30 minutes
LAST_LOG_PERIOD=30


function getConfig()
{
   dir=$1
   echo collecting config from : /etc/ >> $dir/nodeinf.txt
   tar cf $dir/etc.tar /etc/
   gzip $dir/etc.tar 
   ls -l $dir/etc.tar.gz >> $dir/nodeinf.txt
   echo ===== >> $dir/nodeinf.txt
}

# step1. Common information (applicable to any openstack/contrail nodes[ ubuntu based]) 
#    Function: getNodeInfo()
# collect common node information

function getNodeInfo()
{
   #assign logfilename
   nodeInfo=$1
   echo $nodeInfo
   touch $nodeInfo
   echo runcmd:  uname -a >> $nodeInfo
   uname -a > $nodeInfo
   echo ------ >> $nodeInfo
   
   echo runcmd:  free >> $nodeInfo
   free -h >> $nodeInfo
   echo ------ >> $nodeInfo
   
   echo runcmd:  uptime >> $nodeInfo
   uptime >> $nodeInfo
   echo ------ >> $nodeInfo
   
   echo runcmd:  lsb_release >> $nodeInfo 2>>$err
   lsb_release -a >> $nodeInfo
   echo ------ >> $nodeInfo
   echo runcmd:  openstack-version >> $nodeInfo
   nova-manage --version >> $nodeInfo
   echo ------ >> $nodeInfo
   echo runcmd:  openstack-status >> $nodeInfo
   openstack-status >> $nodeInfo
   echo ------ >> $nodeInfo

   echo runcmd:  contrail-version >> $nodeInfo
   contrail-version >> $nodeInfo
   echo ------ >> $nodeInfo

   echo runcmd:  contrail-status -x >> $nodeInfo
   contrail-status -x  >> $nodeInfo
   echo ------ >> $nodeInfo

   echo runcmd:  contrail-status -d >> $nodeInfo
   contrail-status -d  >> $nodeInfo
   echo ------ >> $nodeInfo

   echo runcmd:  openstack-status >> $nodeInfo
   openstack-status >> $nodeInfo
   echo ------ >> $nodeInfo

}

function repeatcmds()
{
  file=$1/$2.txt
  cmdfile=~/rsi/scripts/$2-cmds
  for i in `seq $3`
  do
  echo rpt: running cmds from $cmdfile for $3 repetitions >> $file
  while read -r cmdline;
  do
    echo running : $cmdline >> $file;
    `echo $cmdline` >> $file;
  done < $cmdfile
  echo sleeping for $4 seconds.. >> $file
  sleep $4
  done
  echo ===== >> $file
}


function getLatestLogs()
{
  rm -rf log/*
  mkdir $1/log 2>/dev/null
  find /var/log/ -mmin -$LAST_LOG_PERIOD -exec cp --parents {} $1/log/ \;
  tar czf $1/logs.tgz $1/log/
}

function getMonitorData()
{
  echo $1
  rm -rf monitor/*
  mkdir log 2>/dev/null
  cp -R /var/log/monitor .
  tar czf $1/monitor.tgz monitor
}
getLatestLogs $dir
if [ -d "/var/log/monitor" ]; then
echo collecting monitoring data.. >>  $log
getMonitorData $dir
else
echo monitoring not running >>  $log

fi

# step2. Find node type
#    Function: getNodeType()
function getRoles()
{
status=`contrail-status| grep supervisor`

if `echo $status| grep -q supervisor-contr`; then
    role="$role controller"
    
fi
if `echo $status | grep -q supervisor-conf`; then
    role="$role config"
fi
#if `echo $status | grep -q supervisor-datab`; then
    #role="$role db"
#fi
if `echo $status | grep -q supervisor-ana`; then
    role="$role analytics"
fi
if `echo $status | grep -q supervisor-v`; then
    role="$role vrouter"
fi


#for i in $role
#do
#  echo $i
#done
    eval "$1='$role'"
}

roles=''
getRoles roles
echo The node has : $roles ..>> $dir/roles.txt
echo The node has : $roles ..>> $log

for role in $roles
do
  file=$dir/$role.txt
  date > $file
  echo Running $role/$role.sh >> $log
  echo Running $role/$role.sh >> rsi/err.txt
  
  for cmdfile in rsi/scripts/$role/*.sh 
  do
    echo Running Command file: Running $role $cmdfile >> $file
    echo $cmdfile >>  rsi/err.txt
    echo $cmdfile $role.txt 2>> rsi/err.txt
    bash $cmdfile $role.txt 2>> rsi/err.txt
    echo `date` completed >> $file
  done
  #Specific commands for a node type
  repeatcmds $dir $role 1 0
  
done
# step1. Common information (applicable to any openstack/contrail nodes[ ubuntu based]) 
#    Function: getNodeInfo()

# collect common node information
getNodeInfo $dir/nodeinf.txt
getConfig $dir $dir/nodeinf.txt
getLatestLogs $dir
getMonitorData $dir

tar zcf ~/rsi/rsi.tgz $dir
cp rsi.tgz ~/rsi/$dir.tgz
rm -rf /root/rsi/scripts
rm -rf /root/rsi/scripts.tar
echo `date` completed run >> $log
echo "========" >> $log
exit
