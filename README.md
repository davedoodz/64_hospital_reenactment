<pre>
      ___________________________
     |  _____________________  |
     | | + | + | 64 | + | + | |
     | |___|___|____|___|___| |
     | |  __    __    __    | |
     | | |  |  |  |  |  |   | |
     | | |__|  |__|  |__|   | |
     |_________[] [] _________|
          H O S P I T A L
</pre>

# 64 Hospital Reenactment

A procedural floor-plan generator that lays out a 64-room hospital from room-to-room traffic data instead of a hand-drawn plan.

## What it is

Hospitals are full of rooms that need to be near each other — wards next to nursing stations, labs next to the departments that use them — and far from ones that don't. This project takes an association chart (how often each pair of rooms is visited together, plus each room's footprint) and procedurally places every room on a grid so that the most-connected rooms end up closest together.

The placement algorithm is written in Python: it finds the "hottest" room (most total traffic), places it first, then repeatedly picks the next room with the strongest association to what's already placed and drops it into the grid cell that minimizes distance to its connected neighbors. The same logic is also wired up as a Grasshopper definition (`.gh`) for direct use inside Rhino, with a flowchart documenting the procedure.

A small Flask app turns the resulting association data into a heatmap, so the room-to-room traffic that drives the layout can be inspected visually.

## Highlights

- **Adjacency-driven placement** — rooms are ordered and positioned purely from traffic data, not manual layout.
- **Dual implementation** — the same algorithm exists as standalone Python (`python code.py`, `hospital_code/`) and as a Grasshopper definition for Rhino, with a flowchart (`flowchart2.pdf`, `grasshopper flowchart.png`) documenting the logic.
- **Heatmap viewer** — `heatmap_app/` is a tiny Flask server that visualizes the association chart as a heatmap in the browser.
- **Real dataset** — the layout is driven by `SURE_64HospitalAssociationChart.csv`, a 21+ room association/area table.

## Stack

Python (stdlib: `csv`, `math`, `operator`), Flask for the heatmap viewer, Grasshopper/Rhino for the parallel visual definition.

## Run locally

Placement algorithm (prints the computed room order, placement grid, and final positions):

```bash
cd "64 Hospital Reenactment"
python3 "python code.py"
```

Heatmap viewer:

```bash
cd "64 Hospital Reenactment/heatmap_app"
pip install flask
python3 app.py
# open http://localhost:5000
```

## Map

```text
64 Hospital Reenactment/
├── python code.py                         # standalone placement algorithm
├── hospital_code/                         # same algorithm, packaged with its own CSV
├── heatmap_app/                           # Flask viewer for the association chart
├── SURE_64HospitalAssociationChart.csv/.xlsx   # room adjacency + area data
├── SURE_RESEARCH_...PYTHON_SUN.gh         # Grasshopper definition
└── flowchart2.pdf, grasshopper flowchart*.png  # process diagrams
```
