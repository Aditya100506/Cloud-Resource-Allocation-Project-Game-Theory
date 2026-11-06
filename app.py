import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from algorithms import allocate_fcfs, allocate_priority
from metrics import calculate_metrics
from game_theory import build_payoff_matrix, pure_nash_equilibria

st.set_page_config(page_title="Cloud Resource Allocation", page_icon="☁️", layout="wide")
st.title("☁️ Strategic Decision-Making in Cloud Resource Allocation")
st.caption("A game-theory-inspired simulator comparing allocation policies and strategic tenant choices.")

with st.sidebar:
    st.header("Cloud capacity")
    total_cpu = st.number_input("Available CPU cores", min_value=1, max_value=256, value=8, step=1)
    total_ram = st.number_input("Available RAM (GB)", min_value=1, max_value=1024, value=16, step=1)
    st.info("Requests are allocated only when both CPU and RAM are available.")

st.subheader("1. Application resource requests")
default_requests = pd.DataFrame([
    {"Application": "App A", "CPU cores": 6, "RAM (GB)": 8, "Priority": 1},
    {"Application": "App B", "CPU cores": 4, "RAM (GB)": 8, "Priority": 3},
    {"Application": "App C", "CPU cores": 2, "RAM (GB)": 8, "Priority": 2},
])
edited = st.data_editor(default_requests, num_rows="dynamic", use_container_width=True,
                        column_config={
                            "CPU cores": st.column_config.NumberColumn(min_value=1, max_value=256, step=1),
                            "RAM (GB)": st.column_config.NumberColumn(min_value=1, max_value=1024, step=1),
                            "Priority": st.column_config.SelectboxColumn(options=[1, 2, 3], help="1 = Low, 2 = Medium, 3 = High"),
                        })
requests = []
valid = True
for _, row in edited.iterrows():
    if pd.isna(row["Application"]) or not str(row["Application"]).strip():
        valid = False
        break
    if pd.isna(row["CPU cores"]) or pd.isna(row["RAM (GB)"]) or pd.isna(row["Priority"]):
        valid = False
        break
    requests.append({
        "name": str(row["Application"]),
        "cpu": int(row["CPU cores"]),
        "ram": int(row["RAM (GB)"]),
        "priority": int(row["Priority"]),
    })

if not valid:
    st.error("Complete every application row before running the simulation.")
elif not requests:
    st.warning("Add at least one application request.")
else:
    fcfs = allocate_fcfs(requests, int(total_cpu), int(total_ram))
    priority = allocate_priority(requests, int(total_cpu), int(total_ram))
    results = {"FCFS": fcfs, "Priority-Based": priority}

    st.subheader("2. Allocation results")
    tabs = st.tabs(["FCFS", "Priority-Based"])
    for tab, (label, result) in zip(tabs, results.items()):
        with tab:
            c1, c2, c3, c4 = st.columns(4)
            m = calculate_metrics(result, len(requests))
            c1.metric("CPU utilization", f"{m['CPU utilization (%)']}%")
            c2.metric("RAM utilization", f"{m['RAM utilization (%)']}%")
            c3.metric("Accepted", m["Accepted requests"])
            c4.metric("Acceptance rate", f"{m['Acceptance rate (%)']}%")
            accepted_names = {r["name"] for r in result["accepted"]}
            display_rows = []
            for r in requests:
                display_rows.append({
                    "Application": r["name"],
                    "CPU requested": r["cpu"],
                    "RAM requested (GB)": r["ram"],
                    "Priority": {3:"High", 2:"Medium", 1:"Low"}[r["priority"]],
                    "Status": "Accepted" if r["name"] in accepted_names else "Rejected",
                })
            st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)
            st.write(f"Allocated: **{result['used_cpu']} / {total_cpu} CPU cores** and **{result['used_ram']} / {total_ram} GB RAM**")

    st.subheader("3. Strategy comparison")
    metric_rows = []
    for label, result in results.items():
        metric_rows.append({"Strategy": label, **calculate_metrics(result, len(requests))})
    metric_df = pd.DataFrame(metric_rows).set_index("Strategy")
    st.dataframe(metric_df, use_container_width=True)
    chart_df = metric_df[["CPU utilization (%)", "RAM utilization (%)", "Acceptance rate (%)"]].T
    fig, ax = plt.subplots()
    chart_df.plot(kind="bar", ax=ax)
    ax.set_ylabel("Percent")
    ax.set_ylim(0, 100)
    ax.set_title("Allocation strategy comparison")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Strategy")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader("4. Game-theory model: two cloud tenants")
st.write("Two tenants independently choose a Low Bid or High Bid for scarce priority. Payoffs are illustrative net utility points.")
actions, payoffs = build_payoff_matrix()
payoff_df = pd.DataFrame(
    [[f"{payoffs[(a,b)][0]}, {payoffs[(a,b)][1]}" for b in actions] for a in actions],
    index=actions, columns=actions
)
payoff_df.index.name = "Tenant A \\ Tenant B"
st.caption("Each cell is (Tenant A payoff, Tenant B payoff). Rows are Tenant A's action; columns are Tenant B's action.")
st.table(payoff_df)
equilibria = pure_nash_equilibria()
if equilibria:
    st.success("Pure-strategy Nash equilibrium: " + "; ".join(
        f"A chooses {e['tenant_a']}, B chooses {e['tenant_b']} with payoffs {e['payoffs']}" for e in equilibria
    ))
else:
    st.info("No pure-strategy Nash equilibrium exists in this payoff matrix.")
st.caption("Model limitation: this small illustrative game demonstrates strategic incentives; its payoff values are assumptions, not empirical cloud-market data.")
