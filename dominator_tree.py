from collections import defaultdict
import time
# import sys
# sys.setrecursionlimit(1000)  # 设置更大的递归深度限制


# 记录开始时间
start_time = time.time()


def select_root_node(graph):
    """
    Select the root node of the graph.
    Choose the node with an in-degree of 0 as the root node.
    If there are multiple such nodes, select the one with the maximum degree.
    """
    zero_in_degree_nodes = [node for node in graph if len(graph[node]) == 0]
    if not zero_in_degree_nodes:
        return None
    degrees = {node: len(graph[node]) for node in zero_in_degree_nodes}
    return max(zero_in_degree_nodes, key=degrees.get)


def compute_doms(input_file, output_file):
    """Compute the dominators for all nodes in the graph defined by the input file.
    Node A dominates node B if all paths from the root to B go through A. Writes
    the dominator tree structure to the output file.

    The implementation follows the "simple" version of Lengauer & Tarjan "A Fast
    Algorithm for Finding Dominators in a Flowgraph" (TOPLAS 1979).
    """

    # Read the input file to create the graph
    graph = defaultdict(list)
    with open(input_file, 'r') as f:
        for line in f:
            start, end = map(int, line.strip().split(','))
            graph[start].append(end)

    root_node = select_root_node(graph)  # 选择根节点

    parent = {}
    ancestor = {}
    vertex = []
    label = {}
    semi = {}
    pred = defaultdict(list)
    bucket = defaultdict(list)
    dom = {}

    def dfs(v):
        semi[v] = len(vertex)
        vertex.append(v)
        label[v] = v

        for w in graph[v]:
            if w not in semi:
                parent[w] = v
                dfs(w)
            pred[w].append(v)

    def compress(v):
        if ancestor[v] in ancestor:
            compress(ancestor[v])
            if semi[label[ancestor[v]]] < semi[label[v]]:
                label[v] = label[ancestor[v]]
            ancestor[v] = ancestor[ancestor[v]]

    def evaluate(v):
        if v not in ancestor:
            return v
        compress(v)
        return label[v]

    def link(v, w):
        ancestor[w] = v

    # Step 1: Initialization.
    dfs(next(iter(graph)))  # Start DFS from any node in the graph

    for w in reversed(vertex[1:]):
        # Step 2: Compute semidominators.
        for v in pred[w]:
            u = evaluate(v)
            if semi[u] < semi[w]:
                semi[w] = semi[u]

        bucket[vertex[semi[w]]].append(w)
        link(parent[w], w)

        # Step 3: Implicitly define the immediate dominator for each node.
        for v in bucket[parent[w]]:
            u = evaluate(v)
            dom[v] = u if semi[u] < semi[v] else parent[w]
        bucket[parent[w]] = []

    # Step 4: Explicitly define the immediate dominator for each node.
    for w in vertex[1:]:
        if dom[w]!= vertex[semi[w]]:
            dom[w] = dom[dom[w]]

    # Write the dominator tree structure to the output file
    with open(output_file, 'w') as f:
        for node, dominators in dom.items():
            f.write(f"{node}: {dominators}\n")

# 记录结束时间
end_time = time.time()

# 计算运行时间
running_time = end_time - start_time

# 打印运行时间
print(f"运行时间：{running_time} 秒")


# Call the function with the input and output file paths
compute_doms('./dataset/input.txt', './dataset/output.txt')

