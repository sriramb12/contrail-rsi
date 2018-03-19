dir=$1
echo $dir
file=$dir/vrouter.txt
log=$dir/rsi.log
echo Running vrouter.sh >> $log


function getFlowSummary()
{
  vrinf=$1
  echo runcmd:flow -s `date` >> $vrinf
  flow -s >> $vrinf &
  sleep 6
  kill -9 `pidof flow`
}

function getFlowrate()
{
  vrinf=$1
  echo runcmd:getFlowrate >> $vrinf
  echo runcmd:flow -r `date` >> $vrinf
  flow -r >> $vrinf &
  sleep 5
  kill -9 `pidof flow`
  echo ===== >> $vrinf
}
function getFlowList()
{
  vrinf=$1
  echo runcmd:flow -l >> $vrinf
  for i in `seq 5`
  do
    flow -l >> $vrinf
    sleep 2
  done
  echo ===== >> $vrinf
}

function getRoutes()
{
  vrinf=$1
  echo runcmd:getRoutes >> $vrinf
  vrflist=`vrfstats --dump | grep ^V | cut -f2 -d' '`
  echo VRF list:$vrflist >> $vrinf
  for vrf in $vrflist
  do
    echo runcmd:rt --dump $vrf >> $vrinf
    rt --dump  $vrf >> $vrinf
  done
  echo ===== >> $vrinf
}

vif --list
#For VRouter In addition to above:
# Ref: https://www.juniper.net/documentation/en_US/contrail2.1/topics/task/configuration/vrouter-cli-utilities-vnc.html
#  o vif --list
#  o vif --get <id> iterate over all 
#  o vrfstats --dump
#  o vrfstats --get <id> iterate over all 
#  o dropstats (multiple snapshots)
#  o Flow -l
#  o flow -r flow -s (multiple snapshots) 
#  o rt --dump <vrfid> iterate over all 
#  o mpls --dump
#  o mirror --dump
#  o mirror --get <id> iterate over all 
#  o vxlan --dump
#  o vxlan --get <id> iterate over all 
#  o nh --list
#  o nh --get <id> iterate over all 

function getVrInfo()
{
  echo  `date` rsi for vrouter >> $file
  repeatcmds 1 1
  getFlowrate $1
  getFlowSummary $1
  getRoutes $1
}
getVrInfo  $file
echo  `date` completed running rsi for vrouter >> $file
echo completed running $i >> ../rsi.log
