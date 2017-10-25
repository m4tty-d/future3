#!/usr/bin/env python3

import os
import networkx as nx
import numpy as np
from numpy import linalg as LA
import collections as cl
import copy as cp
import matplotlib.pyplot as plt

def main():
    # az egyes csoportok számosságának a szummája
    population = 0

    # ebben a gráfban tároljuk az egyes csoportok közötti kapcsolatokat
    G = nx.DiGraph()

    nodes_with_cardinality = {}

    for root, dirs, files in os.walk("City"):

        # végigiterálok a file-okon
        for file in files:
            file_full_path = root + os.sep + file

            FILE = open(file_full_path, 'r')

            G.add_node(file_full_path)

            i = 0

            for line in FILE:
                # az első sorban van az adott csoport számossága
                if i == 0:
                    population += int(line)
                    nodes_with_cardinality[file_full_path] = int(line)
                else:
                    G.add_edge(file_full_path, "".join(line.rsplit('\n')))

                i += 1

            FILE.close()

    n = len(list(G.nodes))
    print(list(G.nodes))
    print(n)

    matrix = np.zeros( (n,n) )

    # a dict nem rendezett, ezért rendezem az adatokat a node-ok nevei szerint és berakom egy ordereddict-be
    nodes_with_cardinality = cl.OrderedDict(sorted(nodes_with_cardinality.items(), key=lambda t: t[0]))

    # a node-okat is név szerint rendezem
    nodes = cl.OrderedDict(enumerate(sorted(list(G.nodes))))

    vector = np.asarray( [(i/population) for i in nodes_with_cardinality.values()] )

    for i in nodes.keys():
        for j in nodes.keys():
            neighbors = list(nx.all_neighbors(G, nodes[i]))
            num_of_neighbors = len(neighbors)

            if num_of_neighbors > 0 and nodes[j] in neighbors:
                matrix[i][j] = 1 / num_of_neighbors

    vector = vector.dot(matrix)

    iteracio = 0

    while True:
        print("\n{}.iteracio\n".format(iteracio))

        pv = cp.deepcopy(vector)

        vector = vector.dot(matrix)

        if LA.norm(pv - vector) < 0.00000001:
            break

        for i in range(len(vector)):
            print("{} - {}".format(nodes[i], population*vector[i]) )

        iteracio += 1
        #s = 0
        #for v in np.nditer(vector):
        #    s += v
        #print("\nÖsszeg: {}".format(s))

    nx.draw(G, with_labels=True)
    plt.show()

if __name__ == '__main__':
    main()
