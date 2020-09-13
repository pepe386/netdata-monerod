# Netdata monerod plugin
Plugin to monitor your Monero node. This plugin has some code from energid plugin ( https://github.com/netdata/netdata/tree/master/collectors/python.d.plugin/energid ). I include some alarms you can use to monitor your node uptime and sync status. 

## Requirements 
1. netdata: https://github.com/netdata/netdata
1. monero daemon with rpc json api enabled 
1. python requests module: https://requests.readthedocs.io/en/master/ ( python -m pip install requests )

## Installation
1. Copy monero.chart.py to your pyhon.d directory, usually /usr/libexec/netdata/python.d/
1. Modify monero.conf file with your monero daemon information and copy file to /etc/netdata/python.d/ directory
1. Optional: copy health.d/monero.conf to /etc/netdata/health.d/ directory if you want uptime/sync alarms
1. Restart netdata

