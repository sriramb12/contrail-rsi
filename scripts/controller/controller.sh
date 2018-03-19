dir=$1/$2
file=$dir/$2
date > $file
echo running controller.sh >> $file


# Identify and add all subsystems debug info for controller 
# supervisor-control:           active
#contrail-control              active              
#contrail-control-nodemgr      active              

#Add commands related to

#contrail-dns                  active              
#contrail-named                active           



echo finished running controller.sh >> $file
