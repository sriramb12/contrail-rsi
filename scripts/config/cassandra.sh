nodetool describecluster >> $1
nodetool gcstats >> $1
nodetool gossipinfo >> $1
nodetool netstats >> $1
nodetool ring >> $1
nodetool -h 127.0.0.1 info >> $1
