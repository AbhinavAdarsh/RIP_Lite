"""
Example topology of Quagga routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        quaggaHosts = []
        quaggaHosts.append(QuaggaHost(name='h1', ip='172.0.1.1/16',loIP=None))
        quaggaHosts.append(QuaggaHost(name='r1', ip='172.0.2.1/16',loIP=None))
        quaggaHosts.append(QuaggaHost(name='r2', ip='173.0.3.2/16',loIP=None))
        quaggaHosts.append(QuaggaHost(name='r3', ip='174.0.3.1/16',loIP=None))
        quaggaHosts.append(QuaggaHost(name='r4', ip='175.0.4.1/16',loIP=None))
        quaggaHosts.append(QuaggaHost(name='h2', ip='177.0.5.1/16',loIP=None))

        # Add switch for IXP fabric
        #ixpfabric = self.addSwitch('fabric-sw1')

	# Create a list to store all the hosts and routers
	host_routers = []

        # Setup each Quagga router, add a link between it and the IXP fabric
        for host in quaggaHosts:

            # Create an instance of a host, called a quaggaContainer
            quaggaContainer = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)
	    
	    host_routers.append(quaggaContainer)
            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            #self.addLink(quaggaContainer, ixpfabric)

	# Add all the links as per the topology
	# 0 - h1, 1 - r1, 2 - r2, 3 - r3, 4 - r4, 5 - h2 
	self.addLink(host_routers[0], host_routers[1])
	self.addLink(host_routers[1], host_routers[2])
	self.addLink(host_routers[1], host_routers[3])
	self.addLink(host_routers[2], host_routers[4])
	self.addLink(host_routers[3], host_routers[4])
	self.addLink(host_routers[4], host_routers[5])
