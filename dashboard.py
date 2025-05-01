# dashboard.py
import streamlit as st, pandas as pd, pyarrow.parquet as pq, glob

def load_latest(service):
    files = glob.glob(f"/data/parquet/service={service}/date=*/part*.parquet")
    return pq.read_table(files).to_pandas()

svc = st.sidebar.selectbox("Service", ["auth-service","payments-service"])
df  = load_latest(svc).sort_values("window_start").tail(200)

st.line_chart(df.set_index("window_start")[["avg_latency","p95_latency"]])
st.line_chart(df.set_index("window_start")["error_rate_pct"])
violations = df[df["slo_violation"]]
st.metric("Current p95 (ms)", df.p95_latency.iloc[-1])
st.metric("Current error (%)", df.error_rate_pct.iloc[-1])
st.write(f"⚠️ Violations last 60 min: {len(violations)}")
