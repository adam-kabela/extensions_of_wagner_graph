from sage.all import *

preimage_of_Gamma_3 = graphs.PathGraph(7)
preimage_of_Gamma_3.add_edges([(1,7),(5,8)])

def add_pendants(G, should_see_pendant):
    Gprime = copy(G)
    for v in should_see_pendant:
        new = Gprime.order()
        Gprime.add_edge(v, new)
    return Gprime

# custom function, since sage subdivide function does not allow multigraphs
def subdivide_edge(G, e): 
    Gprime = copy(G)
    new = Gprime.order()
    Gprime.add_edge(e[0], new)
    Gprime.add_edge(e[1], new)
    Gprime.delete_edge(e) # edge multiplicity is reduced by 1
    return Gprime
    
def remove_pendant(G, v):
    Gprime = copy(G)
    for u in Gprime.neighbors(v):
        if Gprime.degree(u) == 1:
            Gprime.delete_vertex(u)
    return Gprime

def contains_preimage_of_Gamma_3(M):
    G = copy(M)
    G = G.to_simple() #we can omit multiedges in host graph since we search a simple subgraph
    if (G.subgraph_search(preimage_of_Gamma_3, induced = False) is None):
        return False
    return True
            
W = graphs.WagnerGraph()
W.allow_multiple_edges(True)

W1 = copy(W)
W1 = subdivide_edge(W1, (0,1))
W1.add_edge(0,8)

W2 = copy(W)
W2 = subdivide_edge(W2, (0,4))
W2.add_edge(0,8)

Ws = [W, W1, W2]

for M in Ws:
    if M.order() == 8:
        should_see_pendant = list(range(8)) # every vertex for Wagner graph W
    else:
        should_see_pendant = list(range(1,8)) # every vertex not incident with a multiedge for W_1, W_2  
    MplusPendants = add_pendants(M, should_see_pendant) #first add pendants to all
    for to_be_subdivided in Subsets(M.edges(labels = False), submultiset=True):
        subM = copy(MplusPendants)
        for e in to_be_subdivided:
            subM = subdivide_edge(subM, e)
        for e in to_be_subdivided:
            subM = remove_pendant(subM, e[0]) #remove pendant since not needed here anymore
            subM = remove_pendant(subM, e[1])
        if (contains_preimage_of_Gamma_3(subM) == False):
            print("We consider multigraph with edges")
            print(M.edges(labels=False))
            print("and subdivide")
            print(to_be_subdivided)
            print("The resulting multigraph has edges")
            print(subM.edges(labels=False))
            print("It does not contain the graph preimage of Gamma_3.")
          
print("Done.")
