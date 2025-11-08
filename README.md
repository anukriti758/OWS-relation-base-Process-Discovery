# Object-Centric Process Mining Toolkit

This repository contains the proposed Python implementation of our research on Object-Centric Process Mining (OCPM).  
It provides three core modules designed to support **object-wise sub-relation based process discovery**, **complexity analysis**, and **comparative evaluation** across multiple Object-Centric Event Logs (OCELs).

---

## 📁 Repository Structure

| File / Folder | Description |
|----------------|-------------|
| `object_wise_sub_discovery.py` | Implements object-type–wise sub-relation–based process discovery using PM4Py and OCEL 2.0. |
| `complexity_dashboard.py` | Computes and visualizes **complexity metrics** (inter-object, intra-object, and structural complexity) for discovered OCPNs and OCDFGs. |
| `complexity_comparison.py` | Compares multiple OCELs based on their discovered models’ complexity metrics to assess structural differences. |
| `noisy_data/` | Contains sample OCEL 2.0 JSON logs for experimentation. |
| `results/` | Stores generated models, metrics, and visual outputs. |

---

## ⚙️ Installation

### 1️⃣ Prerequisites
- Python 3.9 or above  
- Install dependencies:
```bash
pip install pm4py pandas numpy matplotlib networkx


**Usage Guide**
1. Object-Wise Sub-Relation Based Process Discovery

Discover and visualize object-type–specific models (OC-DFGs) from an OCEL.

python object_wise_sub_discovery.py


Input:
An OCEL 2.0 file (e.g., ContainerLogistics.jsonocel)

Output:

Prints universal relation counts

Generates object-type–wise OCDFG visualizations

Returns total and per-object-type relation statistics**

2. Complexity Dashboard

Analyzes discovered models using custom-defined complexity metrics, including:

Inter-object complexity

Intra-object complexity

Structural simplicity metrics (arc-degree, shared participation)

python complexity_dashboard.py


Output:

Complexity metric tables

Complexity distribution charts

Interactive dashboards for model analysis

3. Complexity Comparison

Compares multiple OCELs or sub-models to evaluate complexity variations across different perspectives or datasets.

python complexity_comparison.py


Output:

Comparative visualization of complexity metrics

Summarized report of structural variations

Statistical plots across multiple OCELs



Research Background

This repository supports the proposed research on:

Object-to-Object (O2O) and Object-to-Event (O2E) optimization

Object-wise sub-model discovery without filtering or dropping objects

Complexity quantification for OCPNs and OCDFGs
