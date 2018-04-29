#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None


def startNetwork():
    "instantiates a topo, then starts the network and prints debug information"

    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo()

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
    net.start()

    info('** Dumping host connections\n')
    dumpNodeConnections(net.hosts)
    
    # Need to assign IPs to all the interfaces in the topology created
    info('** Assigning IPs to interfaces\n')
    net.get('r1').cmd('ip address add 173.0.3.3/16 dev r1-eth1')
    net.get('r1').cmd('ip address add 174.0.3.4/16 dev r1-eth2')
    net.get('r2').cmd('ip address add 175.0.3.5/16 dev r2-eth1')
    net.get('r3').cmd('ip address add 176.0.3.6/16 dev r3-eth1')
    net.get('r4').cmd('ip address add 176.0.4.2/16 dev r4-eth1')
    net.get('r4').cmd('ip address add 177.0.4.3/16 dev r4-eth2')
 
    # Set IP forwarding to 1    
    net.get('h1').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    net.get('h2').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    net.get('r1').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    net.get('r2').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    net.get('r3').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    net.get('r4').cmd('echo 1  > /proc/sys/net/ipv4/ip_forward')
    

    info('** Testing network connectivity\n')
    net.ping(net.hosts)

    info('** Dumping host processes\n')
    for host in net.hosts:
        host.cmdPrint("ps aux")

    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
