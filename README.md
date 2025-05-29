# Substitutability-Based-Graph-Node-Pricing
This repository contains the implementation of the node pricing algorithm proposed in the paper **"Substitutability-Based Graph Node Pricing"**. The algorithm leverages graph structural properties and economic substitutability principles to determine node values in directed graphs. The implementation consists of two core modules:

1. **dominator_tree.py**: Converts graph data into dominator tree structures using the Lengauer-Tarjan algorithm
2. **path_similarity.py**: Computes path similarity metrics and node prices based on substitutability

## Requirements
- Python 3.8+
- NetworkX 3.0+
- NumPy 1.20+
- tqdm (for progress bars)
- Graph datasets in edge list format (`*.txt` or `*.csv`)

Install dependencies with:
```bash
pip install networkx numpy tqdm
```

## Repository Structure
```
graph-node-pricing/
├── dominator.py             # Dominator tree construction
├── similarity.py            # Path similarity and pricing calculation
├── datasets/                # Sample graph datasets
│   ├── college_msg.txt      # CollegeMsg dataset
│   └── etc.                 # Other datasets
├── results/                 # Output directory for results
├── LICENSE
└── README.md
```

## 1. Dominator Tree Construction (`dominator_tree.py`)
Implements the Lengauer-Tarjan algorithm to convert directed graphs into dominator trees.

### Features:
- Efficient O(m log n) time complexity
- Handles disconnected components
- Supports large-scale graphs

### Usage:
```python
from dominator import build_dominator_tree

# Load your directed graph (NetworkX DiGraph)
graph = nx.read_edgelist("datasets/college_msg.txt", create_using=nx.DiGraph)

# Build dominator tree with root node '0'
dom_tree = build_dominator_tree(graph, root='0')

# Save dominator tree to file
nx.write_edgelist(dom_tree, "results/college_msg_dominator.edgelist")
```

### Output:
- Dominator tree as a NetworkX DiGraph
- Tree structure stored in edge list format

## 2. Path Similarity & Node Pricing (`path_similarity.py`)
Computes node similarity metrics for basic prices using dominator trees.

### Key Metrics:
- **Path Similarity**: Jaccard similarity of edge sets
- **Positional Criticality**: Node indispensability score
- **Node Substitutability**: Economic substitutability metric
- **Node Prices**: Final price assignments

### Usage:
```python
from similarity import calculate_node_prices

# Load dominator tree
dom_tree = nx.read_edgelist("results/college_msg_dominator.edgelist", create_using=nx.DiGraph)

# Calculate node prices
prices = calculate_node_prices(dom_tree, root='0', epsilon=1e-6)

# Save results
import json
with open("results/college_msg_prices.json", "w") as f:
    json.dump(prices, f, indent=2)
```

### Output:
JSON file containing:
```json
{
  "node_prices": {
    "0": 0.214,
    "1": 0.183,
    "2": 0.097,
    ...
  },
  "substitutability_scores": {
    "0": 0.043,
    "1": 0.356,
    ...
  },
  "criticality_scores": {
    "0": 0.312,
    "1": 0.278,
    ...
  }
}
```

## Datasets
Sample datasets are provided in the `datasets/` directory:

1. **CollegeMsg** (1,899 nodes, 59,835 edges):
   - Temporal messaging network
   - Source: SNAP Dataset Collection

2. **Email-Eu-core** (1,005 nodes, 25,571 edges):
   - Email communication network
   - Source: Leskovec et al. (2007)

To use custom datasets:
1. Format as edge list: `source_node,target_node`
2. Place in `datasets/` directory
3. Update file path in scripts

## Experimental Results
The algorithm produces:
1. Node prices reflecting structural importance
2. Substitutability scores (lower = more unique)
3. Criticality scores (higher = more indispensable)

Example output distribution for sparse vs. dense graphs:
- **Sparse graphs**: Wider price distribution
- **Dense graphs**: More concentrated prices


