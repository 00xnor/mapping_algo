from logger import Logger, logging
from ant_path import AntPath
from ant_heuristic_params import AntHeuristicParams
#------------------------------------------------------------------------------
import numpy as np
import networkx as nx


#------------------------------------------------------------------------------
log = Logger('ant', level=logging.INFO)


#------------------------------------------------------------------------------
class Ant:
  def __init__(
    me,
    mesh: nx.classes.digraph.DiGraph,
    dag: nx.classes.digraph.DiGraph,
    grouped: dict,
    ant_id: int = -1,
    alpha: int = 1,
    beta: int = 1,
  ):
    me.mesh = mesh
    me.dag = dag
    me.grouped = grouped
    me.alpha = alpha
    me.beta = beta
    me.end_node_encountered = False
    me.ant_id = ant_id

  def choose_next_hop(
    me,
    path: AntPath,
    unvisited: list[int, ...],
    dag_edge: tuple[int, int],
    dag_node: int,
    end_node: int
  ):
    if len(unvisited) < 1:
      return None

    ps = me.get_probs_for_all_edges(
      path,
      unvisited,
      dag_edge,
      dag_node
    )

    sample_probs = np.divide(ps, sum(ps)).tolist()

    # force the last mesh node (bottom right) to be chosen last
    if end_node in dag_edge:
      me.end_node_encountered = True

    if me.end_node_encountered or unvisited[0] == end_node:
      choice = unvisited[-1]
    else:
      choice = np.random.choice(unvisited[:-1], 1, sample_probs[:-1])[0]

    return choice

  def get_probs_for_all_edges(
    me,
    path: AntPath,
    unvisited: list[int, ...],
    dag_edge: tuple[int, int],
    dag_node: int
  ):
    ps = []

    for node in unvisited:
      mesh_edge = path.mesh.edges[path.mesh_current, node]
      p = me.get_prob_for_an_edge(path, mesh_edge, dag_edge, dag_node)
      ps.append(p)

    return ps

  def get_prob_for_an_edge(
    me,
    path: AntPath,
    mesh_edge: tuple[int, int],
    dag_edge: tuple[int, int],
    dag_node: int
  ):
    distance = mesh_edge.get('weight', 1)

    energy_route = AntHeuristicParams.ENERGY_ROUTE_ONE_BYTE
    energy_link = AntHeuristicParams.ENERGY_LINK_ONE_BYTE
    energy_per_byte = (distance + 1)*energy_route + distance*energy_link
    number_of_bytes = path.dag.edges[dag_edge].get('weight', 1) # comm cost
    energy_per_transfer = number_of_bytes*energy_per_byte
    tau = 1/energy_per_transfer # energy component

    time_route = path.dag.nodes[dag_node]['weight'] # comp cost
    time_link = path.dag.edges[dag_edge]['weight']*distance
    time_total = time_route + time_link
    phi = 1/time_total # time component

    p = (tau**me.alpha)*(phi**me.beta)    # energy-time heuristic
    p += mesh_edge['pheromone']           # consider history
    p += me.grouped[mesh_edge['weight']]  # prioritize shorter paths

    return p

  def go(me, random_start = None):
    dag_start = list(me.dag.nodes)[0]

    if random_start:
      mesh_start = np.random.choice(list(me.mesh.nodes))
    else:
      mesh_start = list(me.mesh.nodes)[0]

    path = AntPath(me.mesh, me.dag, mesh_start, dag_start)

    # sort the edges so that the last node is processed last
    # i.e. force the output to be at the bottom left of the mesh
    end_node = me.dag.order()-1
    dag_edges = sorted(
      list(nx.edge_bfs(me.dag)),
      key = lambda e: (e[0] == end_node or e[1] == end_node)
    )

    unvisited_mesh_nodes = path.get_unvisited_mesh_nodes()
    log.d(f'{'-'*80}\nant [{me.ant_id}] starts at mesh node [{mesh_start}]')

    me.end_node_encountered = False

    while dag_edges:
      dag_edge = dag_edges.pop(0)

      mesh_node = me.choose_next_hop(
        path,
        unvisited_mesh_nodes,
        dag_edge,
        dag_edge[0],
        end_node
      )

      used = path.visit_and_map(dag_edge, dag_edge[1], mesh_node)

      if used:
        log.d(f'ant [{me.ant_id}] hops to [{mesh_node}]')
        unvisited_mesh_nodes.remove(mesh_node)

    return path

