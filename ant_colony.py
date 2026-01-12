from logger import Logger, logging
from ant import Ant
from ant_path import AntPath
from ant_heuristic_params import AntHeuristicParams
#------------------------------------------------------------------------------
from collections import defaultdict
import networkx as nx
import concurrent.futures
import threading
import numpy as np


#------------------------------------------------------------------------------
class AntColony:
  '''
    Instantiate N ants and optionally preload pheromone levels from 
    a previously saved search state (Path object). 
    N = AntHeuristicParams.NUMBER_OF_ANTS_PER_ITERATION
  '''
  def __init__(
    me,
    mesh: nx.classes.digraph.DiGraph,
    dag: nx.classes.digraph.DiGraph,
    existing_path: AntPath = None
  ):
    me.log = Logger('and_colony', level=logging.INFO)
    num_ants = AntHeuristicParams.NUMBER_OF_ANTS_PER_ITERATION
    me.mesh = mesh

    assert len(mesh.nodes) >= len(dag.nodes)

    # preload pheromone levels or start with none
    if existing_path:
      for u, v in existing_path.mesh.edges:
        mesh.edges[u, v].setdefault('pheromone',
          existing_path.mesh.edges[u, v]['pheromone'])
        mesh.edges[u, v].setdefault('usage_count',
          existing_path.mesh.edges[u, v]['usage_count'])
        assert mesh.edges[u, v]['weight'] > 0
    else:
      for u, v in mesh.edges:
        mesh.edges[u, v].setdefault('pheromone', 0)
        mesh.edges[u, v].setdefault('usage_count', 0)
        assert mesh.edges[u, v]['weight'] > 0

    # for prioritizing shorter paths
    grouped = defaultdict(list)
    for u, v, data in me.mesh.edges(data=True):
      if 'weight' in data:
        grouped[data['weight']] = np.exp(-data['weight'])

    me.ants = [Ant(mesh, dag, grouped, i) for i in range(num_ants)]
    me.log.i(f'ant colony consists of [{num_ants}] ants')

  def go(me):
    active_threads = []

    def monitored_go(task):
      tid = threading.get_ident() % 10
      active_threads.append(tid)
      me.log.d(f'{tid:<2} 🚀')
      res = task.go()
      active_threads.remove(tid)
      me.log.d(f'{tid:<2} ✅')
      return res

    with concurrent.futures.ThreadPoolExecutor() as executor:
      paths = list(executor.map(monitored_go, me.ants))

    paths.sort()

    return paths

