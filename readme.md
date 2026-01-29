# Weighted CLIPPER Python Example

This repository provides a **minimal, self-contained Python example** demonstrating how to use **CLIPPER** with **weighted data associations**.

It is intended as a lightweight, readable companion to the official CLIPPER repository, showing how to:
- generate candidate landmark associations,
- compute **per-association confidence weights**, and
- inject those weights into CLIPPER’s affinity matrix before solving.

> **Upstream / master repository:**  
> This example builds directly on the official CLIPPER implementation.  
> Please treat the upstream repo as the *source of truth* for CLIPPER itself:  
> https://github.com/mit-acl/clipper

---

## What is CLIPPER?

**CLIPPER** is a graph-theoretic framework for robust data association, commonly used in robotics and perception problems such as point cloud registration and landmark matching.

Given a set of candidate associations, CLIPPER:
- scores pairwise geometric consistency,
- builds an affinity and constraint graph, and
- solves for a globally consistent subset of associations using a maximum-clique-style optimization.

Unlike purely binary formulations, CLIPPER supports **weighted graphs**, allowing additional confidence information to influence the solution.

---

## What this repo demonstrates

This example focuses on a **weighted extension** of the standard CLIPPER workflow:

1. Two synthetic landmark sets are generated with partial overlap.
2. A dense candidate association list (cartesian product) is constructed.
3. Associations are filtered and **weighted** based on landmark size consistency.
4. CLIPPER computes geometric consistency using a Euclidean distance invariant.
5. The computed association weights are injected onto the **diagonal of the CLIPPER affinity matrix**.
6. CLIPPER solves for a consistent subset of associations.
7. The result is visualized as two x–y plots with lines connecting selected matches.

The goal is to show *how* and *where* weights can be incorporated, not to provide a full benchmark or application pipeline.

---

## Initial Repository Setup

This repository uses the official **CLIPPER** implementation as a git submodule.
CLIPPER itself is not a pure Python package and must be built from source.

For full details, refer to the upstream CLIPPER repository:
https://github.com/mit-acl/clipper

The instructions below summarize the standard setup used by this repository.

---

### Clone the repository (with submodules)

```bash
git clone --recurse-submodules https://github.com/annika-thomas/weighted-clipper.git
cd weighted-clipper
```

If the repository was already cloned without submodules, initialize them with:

```bash
git submodule update --init --recursive
```


## Setting up the Python virtual environment

This repository uses a Python virtual environment to manage dependencies for the
example code. CLIPPER itself is built separately and is **not** installed via
`pip`.

---

### Create and activate the virtual environment

From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your shell prompt should be prefixed with `(venv)`.

Upgrade `pip` (recommended):

```bash
pip install --upgrade pip
```

### Install Python dependencies

Install the required Python packages for the example code:

```bash
pip install -r env/requirements.txt
```

### Build CLIPPER and Python bindings

CLIPPER is built using CMake. The following commands compile the C++ library and
install the Python bindings (`clipperpy`) into the currently active Python
environment.

Make sure your Python virtual environment is activated before running these
commands.

```bash
cd third_party/clipper
mkdir -p build
cd build
cmake -DBUILD_BINDINGS_PYTHON=ON ..
make -j
make pip-install
```

After installation, verify that CLIPPER is available in Python:

```bash
python -c "import clipperpy; print('clipperpy installed successfully')"
```
If this command fails, check the following:

- Ensure the correct Python virtual environment is activated.
- Re-run `make pip-install` after activating the virtual environment.
- Confirm that `clipperpy` appears in the list of installed packages:

```bash
  pip list | grep clipper
```

## Citation

If you use CLIPPER in academic work, please cite the CLIPPER paper (from the upstream repo): :contentReference[oaicite:4]{index=4}

```bibtex
@inproceedings{lusk2021clipper,
  title={{CLIPPER}: A graph-theoretic framework for robust data association},
  author={Lusk, Parker C and Fathian, Kaveh and How, Jonathan P},
  booktitle={2021 IEEE International Conference on Robotics and Automation (ICRA)},
  pages={13828--13834},
  year={2021},
  organization={IEEE}
}
