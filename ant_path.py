import networkx as nx


#------------------------------------------------------------------------------
class AntPath:
  def __init__(
    me,
    mesh: nx.classes.digraph.DiGraph,
    dag: nx.classes.digraph.DiGraph,
    mesh_start: int,
    dag_start: int
  ):
    me.mesh = mesh
    me.mesh_start = mesh_start
    me.mesh_nodes = [mesh_start]
    me.mesh_current = mesh_start
    me.mesh_visited = set(me.mesh_nodes)
    me.mesh_edges = []
    me.mesh_cost = 0

    me.dag = dag
    me.dag_start = dag_start
    me.dag_nodes = [dag_start]
    me.dag_current = dag_start
    me.dag_visited = set(me.dag_nodes)
    me.dag_edges = []
    me.dag_cost = 0

    me.dag_cost_hops = 0

  def __contains__(me, node):
    return node in me.mesh_nodes

  def __repr__(me):
    line = '-'*92

    zipped = zip(me.dag_nodes, me.mesh_nodes)
    mapped = list(sorted(zipped, key=lambda x: x[1]))

    str_mpath = '--'.join([f'{str(n[1]):<2}' for n in mapped])
    str_dpath = '--'.join([f'{str(n[0]):<2}' for n in mapped])
    r = f'{line}\n'
    r += f'{'cost':<5} | {'mesh nodes':<10} | {str_mpath} | hops\n'
    r += f'{me.dag_cost:<5} | {'task nodes':<10} | '
    r += f'{str_dpath} | {me.dag_cost_hops:<4}'
    return r

  def __iter__(me):
    return iter(me.dag_edges)

  def __eq__(me, other):
    return me.dag_cost == other.dag_cost

  def __lt__(me, other):
    return me.dag_cost < other.dag_cost

  def get_unvisited_mesh_nodes(me):
    nodes = []
    for node in me.mesh[me.mesh_current]:
      if node not in me.mesh_visited:
        nodes.append(node)
    return nodes

  def visit_and_map(
    me,
    dag_edge: tuple[int, int],
    dag_node: int,
    mesh_node: int
  ):
    mesh_node_used = False

    if dag_node not in me.dag_nodes:
      me.dag_nodes.append(dag_node)
      me.mesh_nodes.append(mesh_node)
      me.mesh_visited.add(mesh_node)

      mesh_edge = me.mesh_current, mesh_node
      data = me.mesh.edges[mesh_edge]
      me.mesh_edges.append(mesh_edge)
      me.mesh_cost += data['weight']
      me.mesh_current = mesh_node
      mesh_node_used = True

    me.dag_edges.append(dag_edge)
    start = me.dag_nodes.index(dag_edge[0])
    end = me.dag_nodes.index(dag_edge[1])
    e = me.mesh_nodes[start], me.mesh_nodes[end]
    n_hops = me.mesh.edges[e]['weight']
    me.dag_cost_hops += n_hops
    comm_weight = me.dag.edges()[dag_edge]['weight']
    comp_weight = me.dag.nodes()[dag_node]['weight']
    me.dag_cost += int(n_hops*comm_weight + comp_weight)

    me.dag.edges()[dag_edge]['mapped_weight'] = round(
      float(comm_weight*n_hops), 2)

    me.dag.edges()[dag_edge]['n_hops'] = n_hops

    me.dag.nodes()[dag_node]['mapped_weight'] = round(
      float(comp_weight), 2)

    return mesh_node_used

