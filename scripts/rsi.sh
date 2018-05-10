#!/bin/bash
ROOT_DIR=/root/rsi
RSILOG=$ROOT_DIR/rsi.log
ts=rsi-`date +%d%b%y-%H%M%S`
outputDir=$ROOT_DIR/$ts
RUNLOG=$outputDir/summary.txt
scriptDir=$ROOT_DIR/scripts
monitorDir=/var/log/monitor

#comment this line!!
#rm -rf $ROOT_DIR/rsi-*

start=`date +%s`
date >> $RSILOG 
echo Creating $outputDir >> $RSILOG 

mkdir $outputDir
ERRLOG=$outputDir/err.txt
function narrate()
{
   echo $1 | tee -a $RSILOG $RUNLOG $ERRLOG $2 > /dev/null
}

narrate "`date` collecting contrail-rsi from `hostname`"

function getConfig()
{
   dir=$1
   narrate "collecting config from : /etc/"
   tar Pcf $outputDir/etc.tar /etc/
   narrate =====
}

#Change this to another value, depending on need
#This will fetch log files which are changed in last 'n' minutes
LAST_LOG_PERIOD=1

function getLatestLogs()
{
  mkdir $1/log 2>/dev/null
  cd /var/log
  find . -mmin -$LAST_LOG_PERIOD -exec cp --parents {} $1/log/ \;
  tar  Pczf $1/logs.tgz $1/log/
}

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
    eval "$1='$role'"
}

function runCmdFile()
{
input=$1
f=`echo $1| cut -f6 -d\/`
grep -v ^$ $input | grep -v "^#" > $input.tmp
out=$2/$f.txt
while IFS= read -r cmd
do
  narrate "Executing:$cmd" $out 
  narrate "==============" $out
  $cmd 1>>$out  2>>$ERRLOG
  echo  "....">> $out 
done < $input.tmp
rm $input.tmp
}


function getCommonInfo()
{
   narrate "common.sh:Step 1.a: Getting Common Information "
   return
   runCmdFile common.sh $outputDir
}

narrate "Step 1.a: Get system information (applicable for any contrail node)"
     getCommonInfo

narrate "Step 1.b: Fetch recent logs"
  getLatestLogs $outputDir

narrate "Step 1.c: Fetch /etc/"
  getConfig

narrate "Step 2: Getting contrail roles"
#Step 2: Find what rolea are running
roles=''
     getRoles roles

#Step 2: Execute role specific commands 
narrate "The Node has :  $roles"


for role in $roles
do
  narrate "processing $role "
  roledir=$outputDir/$role
  mkdir $roledir
  file=$roledir/$role.txt
  date >> $file
  for cmdfile in `ls $scriptDir/$role/*sh`
  do
    narrate "Running $cmdfile"
    runCmdFile $cmdfile  $roledir
    narrate  === 
  done
done

#Step 3: create a tar(zipped) file
end=`date +%s`
runtime=`expr $end - $start`
narrate "finished contrail-rsi in $runtime seconds"

tar zcf $outputDir.tgz $outputDir
ls -lh $outputDir.tgz >> $RSILOG
rm -rf $outputDir
