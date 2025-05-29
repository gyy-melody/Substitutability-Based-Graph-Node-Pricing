from collections import defaultdict

import time

# 记录开始时间
start_time = time.time()

def read_tree(file_path):
    tree = {}
    with open(file_path, 'r') as f:
        for line in f.readlines():
            parent, child = map(int, line.strip().split('	'))
            if parent not in tree:
                tree[parent] = []
            tree[parent].append(child)
    return tree


def build_graph(tree):
    graph = defaultdict(lambda: {'incoming': set(), 'outgoing': set()})
    for parent, children in tree.items():
        for child in children:
            graph[parent]['outgoing'].add((parent, child))
            graph[child]['incoming'].add((parent, child))
    return graph


def find_all_incoming_edges(graph, target_node):
    visited = set()
    stack = [(target_node, None)]  # (当前节点, 到该节点的边)
    all_incoming_edges = set()

    while stack:
        current_node, incoming_edge = stack.pop()
        if current_node in visited:
            continue
        visited.add(current_node)

        if incoming_edge is not None:
            all_incoming_edges.add(incoming_edge)

        for edge in graph[current_node]['incoming']:
            stack.append((edge[0], edge))

    return all_incoming_edges


def find_all_outgoing_edges(graph, start_node):
    visited = set()
    stack = [(start_node, None)]  # (当前节点, 来自的边)
    all_outgoing_edges = set()

    while stack:
        current_node, incoming_edge = stack.pop()
        if current_node in visited:
            continue
        visited.add(current_node)

        if incoming_edge is not None:
            all_outgoing_edges.add(incoming_edge)

        for edge in graph[current_node]['outgoing']:
            stack.append((edge[1], edge))

    return all_outgoing_edges


def calculate_overlap(graph):
    result = {}
    nodes = list(graph.keys())

    for node in nodes:
        incoming_edges = find_all_incoming_edges(graph, node)
        outgoing_edges = find_all_outgoing_edges(graph, node)

        incoming_overlap_count = 0
        incoming_total_count = len(incoming_edges)

        outgoing_overlap_count = 0
        outgoing_total_count = len(outgoing_edges)

        other_nodes_count = len(nodes) - 1  # 当前节点外其他所有节点的个数

        for other_node in nodes:
            if other_node == node:
                continue

            other_incoming_edges = find_all_incoming_edges(graph, other_node)
            other_outgoing_edges = find_all_outgoing_edges(graph, other_node)

            incoming_overlap_count += len(incoming_edges & other_incoming_edges)
            outgoing_overlap_count += len(outgoing_edges & other_outgoing_edges)

            if incoming_total_count > 0:
                incoming_overlap_ratio = incoming_overlap_count / incoming_total_count
            else:
                incoming_overlap_ratio = 0

            if outgoing_total_count > 0:
                outgoing_overlap_ratio = outgoing_overlap_count / outgoing_total_count
            else:
                outgoing_overlap_ratio = 0

            overlap_ratio = (incoming_overlap_ratio + outgoing_overlap_ratio) / other_nodes_count /2
            result[node] = overlap_ratio

    return result

def output_to_file(node_info, overlap_avg, output_path):
    with open(output_path, 'w') as f:
        for node, (incoming_edges, outgoing_edges, overlap) in node_info.items():
            f.write(f"{node}:{overlap_avg[node]}\n")
            # f.write(f"{node}:{incoming_edges}:{outgoing_edges}:{overlap_avg[node]}\n")

if __name__ == "__main__":

    # 记录开始时间
    start_time = time.time()

    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/弹性/10-d_tree.txt'
    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/Cora/cora.cites'
    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/Google/支配树结构.txt'
    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/Google/edges.txt'
    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/test3/800-d_tree.txt'
    # tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/dataset/email_dtree.txt'
    tree_file_path = 'C:/Users/ASUS/PycharmProjects/untitled/AAApost/dataset/msg.txt'

    output_path = 'msg_sim原图.txt'

    tree = read_tree(tree_file_path)
    graph = build_graph(tree)
    overlap_ratios = calculate_overlap(graph)

    node_info = {}
    for node in graph:
        incoming_edges = find_all_incoming_edges(graph, node)
        outgoing_edges = find_all_outgoing_edges(graph, node)
        node_info[node] = (incoming_edges, outgoing_edges, overlap_ratios[node])

    overlap_avg = {}
    for node in overlap_ratios:
        overlap_avg[node] = overlap_ratios[node]

    # 记录结束时间
    end_time = time.time()

    # 计算运行时间
    running_time = end_time - start_time

    # 打印运行时间
    print(f"运行时间：{running_time} 秒")

    output_to_file(node_info, overlap_avg, output_path)

