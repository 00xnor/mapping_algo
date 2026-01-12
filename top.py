from ant_colony_mission import AntColonyMission
from ant_mesh import AntMesh
#------------------------------------------------------------------------------
import networkx as nx
import pickle
import sys


#------------------------------------------------------------------------------
def create_example_graph():
  g = nx.DiGraph()

  g.add_edge(0,1)
  g.add_edge(1,2)
  g.add_edge(2,3)
  g.add_edge(2,4)
  g.add_edge(2,5)
  g.add_edge(2,6)
  g.add_edge(3,7)
  g.add_edge(4,7)
  g.add_edge(5,7)
  g.add_edge(6,7)
  g.add_edge(7,8)
  g.add_edge(8,9)
  g.add_edge(1,10)
  g.add_edge(10,11)
  g.add_edge(11,12)
  g.add_edge(12,9)
  g.add_edge(9,13)
  g.add_edge(13,14)
  g.add_edge(14,15)

  adj_matrix = nx.adjacency_matrix(g).todense()
  dag = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph())

  for n in dag.nodes:
    dag.nodes[n].setdefault('weight', 1.0)

  nx.set_edge_attributes(dag, 1.0, 'weight')

  return dag


#------------------------------------------------------------------------------
def main():
  best_path = 'best_path.bin'

  dag = create_example_graph()
  mesh = AntMesh(4)
  mission = AntColonyMission(mesh, dag, attempts=10000)

  for path in mission.swarm_the_graph():
    with open(best_path, 'wb') as f:
      pickle.dump(path, f)


#------------------------------------------------------------------------------
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    sys.exit()

