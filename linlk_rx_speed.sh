#!/usr/bin/env bash

set -eu

iface="$1"
stat="/sys/class/net/${iface}/statistics/rx_bytes"
prev=$(<$stat)
while sleep 1; do
	cur=$(<$stat)
	echo "$cur $prev" | awk '{s=($1-$2)/1024; 
	if(s>=1){printf "%.2f KB/s\n",s;} 
	else if(s>=1024){s=s/1024; printf "%.2f MB/s\n",s;}
	else if(s/1024>=1){s=s/1024; printf "%.2f GB/s\n",s;}
	else{printf "%.2f KB/s\n",s}}'
	prev="$cur"
done
