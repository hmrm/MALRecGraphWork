from __future__ import division
from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write
from pygraph.classes.exceptions import AdditionError
import sys

nodenames = sys.argv[1]
nodeedgedir = sys.argv[2]
predictionid = sys.argv[3]
iterations = sys.argv[4]

nodes = open(nodenames, "r").readlines()
userdata = sys.stdin.readlines() #format: line -> id rating

sys.stderr.write("Building Recommendation Graph\n")

dg = digraph()
dg.add_nodes([x.strip() for x in nodes])
try:
    for node in nodes:
        edges = open(nodeedgedir + "/" + node.strip()).readlines()
        for edge in edges:
            edge = edge.strip().split()
            try:
                dg.add_edge((node.strip(), edge[0]), wt=int(edge[2]))
                dg.add_node_attribute(edge[0], ("label", edge[1]))
            except AdditionError:
                pass
    
    sys.stderr.write("Normalizing Weights\n")
    for node in dg:
        totalweight = 0
        for neighbor in dg.neighbors(node):
            totalweight += dg.edge_weight((node, neighbor))
        for neighbor in dg.neighbors(node):
            try:
                dg.set_edge_weight((node, neighbor), dg.edge_weight((node, neighbor)) / totalweight)
            except ZeroDivisionError:
                pass
    
    sys.stderr.write("Setting Initial Values\n")
    for line in userdata:
        id_rating = line.strip().split()
        try:
            if id_rating[0] in dg:
                dg.add_node_attribute(id_rating[0], ("rating", int(id_rating[1])))
                dg.add_node_attribute(id_rating[0], ("initial", True))
                dg.add_node_attribute(id_rating[0], ("rated", True))
        except IndexError:
            pass
    
    sys.stderr.write("Iterating\n")
    for i in xrange(int(iterations)):
        sys.stderr.write("Iteration number " + str(i + 1) + "\n")
        newinfo = False
        for node in dg:
            if not ("initial", True) in dg.node_attributes(node):
                totalincidentweight = 0
                totalincidentvalues = 0
                for incident in dg.incidents(node):
                    if "rating" in [x[0] for x in dg.node_attributes(incident)]:
                        totalincidentweight += dg.edge_weight((incident, node))
                        totalincidentvalues += dg.edge_weight((incident, node)) * [x[1] for x in dg.node_attributes(incident) if x[0] == "rating"][0]
                if totalincidentweight > 0:
                    dg.add_node_attribute(node, ("newrating", totalincidentvalues / totalincidentweight))
                    dg.add_node_attribute(node, ("update", True))
        for node in dg:
            if ("update", True) in dg.node_attributes(node):
                if not ("rated", True) in dg.node_attributes(node):
                    newinfo = True
                dg.add_node_attribute(node, ("rating", [x[1] for x in dg.node_attributes(incident) if x[0] == "newrating"][0]))
                dg.add_node_attribute(node, ("update", False))
                dg.add_node_attribute(node, ("rated", True))
        sys.stderr.write("New information? :" + str(newinfo) + "\n")
        if not newinfo:
            break
        
except IndexError:
    print 5
    exit(0)

sys.stderr.write("Reading Prediction\n")
if not predictionid in [node for node in dg if ("rated", True) in dg.node_attributes(node)]:
    print 5
else:
    print [x[1] for x in dg.node_attributes(predictionid) if x[0] == "rating"][0]
