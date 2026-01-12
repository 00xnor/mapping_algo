import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


#------------------------------------------------------------------------------
class AntMesh:
  def __init__(me, n):
    me.g = nx.grid_2d_graph(n, n)

    nodes = list(me.g.nodes())
    adj_matrix = np.identity(len(nodes)).astype('int')
    adj_matrix[adj_matrix == 0] = -1
    adj_matrix[adj_matrix == 1] = 0
    adj_matrix[adj_matrix == -1] = 1

    for i in range(len(adj_matrix)):
      for j in range(len(adj_matrix[i])):
        if i == j:
          continue
        else:
          start = nodes[i]
          end = nodes[j]
          d = np.abs(start[0]-end[0]) + np.abs(start[1]-end[1])
          adj_matrix[i][j] = d

    label_map = {}
    for i, node in enumerate(me.g.nodes):
      label_map[node] = i
      pass
    me.g = nx.relabel_nodes(me.g, label_map)

    for i in range(len(me.g.nodes)):
      x = i % n
      y = int(i / n)
      me.g.nodes[i]['pos'] = (x,-y)

    # complete graph
    me.graph = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph())

    for i in range(len(me.graph.nodes)):
      x = i % n
      y = int(i / n)
      me.graph.nodes[i]['pos'] = (x,-y)

  def show(me, complete=False):
    g = me.graph if complete else me.g

    node_pos = nx.get_node_attributes(g, 'pos')
    edge_weight = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx(g, node_pos, node_color='lightgreen',
      with_labels=True, node_size=800)
    nx.draw_networkx_edge_labels(g, node_pos, edge_labels=edge_weight)
    plt.show()
    pass

  pass

