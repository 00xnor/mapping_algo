from logger import Logger, logging
from ant_colony import AntColony
from ant_path import AntPath
from ant_heuristic_params import AntHeuristicParams
from ant_mesh import AntMesh
#------------------------------------------------------------------------------
from collections import defaultdict
from collections import deque
import networkx as nx
import numpy as np
import time


#------------------------------------------------------------------------------
class AntColonyMission:
  def __init__(
    me,
    mesh: AntMesh,
    dag: nx.classes.digraph.DiGraph,
    attempts: int = 1000,
    existing_path: AntPath = None
  ):
    me.log = Logger('and_colony_mission', level=logging.INFO)
    me.colony = AntColony(mesh.graph, dag, existing_path)
    me.attempts = attempts
    me.windows = {}

    grouped = defaultdict(list)
    for _, _, data in me.colony.mesh.edges(data=True):
      if 'weight' in data:
        grouped[data['weight']].append(data['pheromone'])

    for k, _ in grouped.items():
      me.windows[k] = deque(maxlen=AntHeuristicParams.MOVING_AVERAGE_WINDOW)

  def swarm_the_graph(me):
    best_known = None
    start = time.time()

    while me.attempts:
      me.attempts -= 1

      runners = me.colony.go()
      top_runner = runners[0]
      me.deposit_pheromone(top_runner)

      if best_known is None or top_runner < best_known:
        best_known = top_runner
        print(best_known)

        elapsed = time.time() - start
        print(f'[{elapsed:.2f}s] [{me.attempts}]')

        yield best_known

  def deposit_pheromone(me, top_runner):
    for edge in me.colony.mesh.edges:
      pheromone_deposit = 0

      if edge in top_runner.mesh_edges:
        pheromone_deposit += (
          AntHeuristicParams.PHERONOME_DEPOSIT / top_runner.dag_cost)
        me.colony.mesh.edges[edge]['usage_count'] += 1

      curr_pheromone = me.colony.mesh.edges[edge]['pheromone']
      me.colony.mesh.edges[edge]['pheromone'] = pheromone_deposit + (
        1 - AntHeuristicParams.PHERONOME_EVAPORATION_RATE)*curr_pheromone

    # split by weight category
    grouped = defaultdict(list)
    for _, _, data in me.colony.mesh.edges(data=True):
      if 'weight' in data:
        grouped[data['weight']].append(data['pheromone'])

    # accumulate averages by weight category
    for k, v in grouped.items():
      me.windows[k].append(round(np.mean(v), 4))


