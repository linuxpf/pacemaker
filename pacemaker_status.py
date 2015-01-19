#!/usr/bin/python
#20150106
#support pacemaker 1.1 (rhel6/centos6)
import sys, getopt, os,re, subprocess
from pcs import usage, cluster, utils, status

def main(arv):
    #sub_cmd = argv.pop(0)
    arv = arv[0]
    if arv == "resources":
        resource_show()
     
    elif arv == "nodes":
        nodes_status()
    else:
        usage.status()
        sys.exit(1)
		
#offline_nodes = []
#check pacemaker offline nodes 
def nodes_status():
    Msg = 0
    all_nodes = utils.getNodesFromCorosyncConf()
    online_nodes = utils.getCorosyncActiveNodes()
    offline_nodes = []
    for node in all_nodes:
        if node in online_nodes:
            next
        else:
            offline_nodes.append(node)
    online_nodes.sort()
    offline_nodes.sort()
    if len(offline_nodes)> 0:
	    Msg=len(offline_nodes)
#	  
    info_dom = utils.getClusterState()
    nodes = info_dom.getElementsByTagName("nodes")
    if nodes.length == 0:
        #utils.err("No nodes section found")
        sys.exit(0) 
    onlinenodes = []
    offlinenodes = []
    standbynodes = []
    for node in nodes[0].getElementsByTagName("node"):
        if node.getAttribute("online") == "true":
            if node.getAttribute("standby") == "true":
                standbynodes.append(node.getAttribute("name"))
            else:
                onlinenodes.append(node.getAttribute("name"))
        else:
            offlinenodes.append(node.getAttribute("name"))

#    print "Pacemaker Nodes:"

#    print " Online:",
#    for node in onlinenodes:
#        print node,
#    print ""
#    print " Standby:",
#    for node in standbynodes:
#        print node,
#    print ""
#    print " Offline:",
#    for node in offlinenodes:
#        print node,
#   print ""
    if len(offlinenodes) > 0:
        Msg = len(offlinenodes)
#check cluster_status on current node
    (output, retval) = utils.run(["crm_mon", "-1", "-r"])
    if (retval != 0):
	    Msg=-1
	    sys.exit(0)
    print Msg

#pcs status resource resource_show
def resource_show():
    output = subprocess.Popen('/usr/sbin/pcs status resources',stdout=subprocess.PIPE,shell=True)
    output.wait()
    #(output, retval) = utils.run(["pcs", "status", "resources"])
    #print output.stdout.read()
    retval= output.returncode
    
    Msg =0
    if retval != 0:
        Msg=-1
	#preg = re.compile(r'.*(Started:.*)')
    for line in output.stdout.read().split('\n'):
	    if re.search(r"Started",line) or re.search(r"standby",line):
                continue
            elif re.search(r"Stopped",line) or re.search(r"unmanaged",line):
	        Msg += 1
    print Msg

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        print "Usage: %s (nodes|resources)" % sys.argv[0]
        sys.exit(0)
    else:
        main(sys.argv[1:])
