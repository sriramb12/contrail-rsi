
# Identify and add all subsystems debug info for config 
#supervisor-config:            active
#contrail-api:0                active              
#contrail-config-nodemgr       active              
#contrail-device-manager       backup              

#contrail-discovery:0          active              
#contrail-schema               backup              

#contrail-svc-monitor          backup              

#ifmap                         active          


keystone --os-username ADMIN --os-password contrail123 --os-auth-url http://192.168.10.81:5000/v2.0/tenant-list >> $file
