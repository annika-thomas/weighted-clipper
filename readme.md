# CLIPPER (Weighted Graph) — Minimal Example Repo

This repo is a **minimal, easy-to-run example** showing how to use **CLIPPER** with **weighted** pairwise consistency (i.e., you keep edge-strength information instead of binarizing the graph).

> **Upstream / master README:** This repository’s setup notes and background are adapted from the official CLIPPER repository, which should be treated as the **master source of truth**:
> - https://github.com/mit-acl/clipper :contentReference[oaicite:0]{index=0}

---

## What is CLIPPER?

**CLIPPER** is a graph-theoretic framework for robust, pairwise data association used in robotics and autonomy (e.g., point cloud registration, sensor calibration, place recognition). It forms a graph using **geometric consistency** and reduces association to the **maximum clique** problem. CLIPPER provides a relaxation that (1) enables guarantees and (2) works on **weighted graphs**, avoiding the information loss from binarization common in other approaches. :contentReference[oaicite:1]{index=1}

The upstream CLIPPER repo provides **MATLAB and C++ implementations**, plus **Python bindings** and examples. :contentReference[oaicite:2]{index=2}

---

## What this repo adds

This repo is intentionally small and opinionated:

- A single **weighted** example you can run end-to-end
- A couple of helper utilities to construct a **weighted consistency graph**
- “Copy/paste” commands to build CLIPPER (via submodule) and run the demo

If you want the full set of benchmarks, MATLAB tooling, bindings options, etc., use the upstream CLIPPER repo directly. :contentReference[oaicite:3]{index=3}

---

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
