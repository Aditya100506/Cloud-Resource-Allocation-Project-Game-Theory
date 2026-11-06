# Strategic Decision-Making in Cloud Resource Allocation

A lightweight Python/Streamlit prototype for a Game Theory project.

## Features
- FCFS and Priority-Based cloud resource allocation.
- CPU/RAM capacity constraints.
- Accepted/rejected requests and utilization metrics.
- Interactive table and strategy comparison chart.
- Two-tenant normal-form game with payoff matrix and pure-strategy Nash equilibrium calculation.

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Command-line demo
```bash
python3 main.py
```

## Game-theory model
Actions for each tenant: Low Bid or High Bid.
Illustrative payoff matrix (Tenant A, Tenant B):
- (Low, Low): (5, 5)
- (Low, High): (2, 7)
- (High, Low): (7, 2)
- (High, High): (3, 3)

Each tenant's best response is High Bid when the other chooses Low Bid, and Low Bid when the other chooses High Bid. Therefore there are two pure-strategy Nash equilibria: (High Bid, Low Bid) and (Low Bid, High Bid). The payoff assumptions are illustrative and should not be represented as measured data.

## Interpretation
FCFS and priority-based allocation are simple policies. Higher utilization is not automatically socially optimal: priority, fairness, and service-level objectives also matter. This prototype is a simulator, not a deployment on a real cloud provider.
