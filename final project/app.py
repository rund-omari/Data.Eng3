"""SDK DataForge Studio — live final class. Run: streamlit run app.py"""
import hashlib
import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from engine import clean_text, quality_report, run_pipeline, transform_new_batch

st.set_page_config(page_title="SDK · DataForge Studio", page_icon="🧩", layout="wide")
st.markdown("""
<style>
:root{--magenta:#D63384;--cyan:#00B8D9;--navy:#192B50}
.stApp{background:#F8FAFE;color:#24344F}
section[data-testid="stSidebar"]{background:#F0F5FC}
h1,h2,h3{color:#192B50!important;letter-spacing:-.02em}
[data-testid="stMetric"]{background:white;border:1px solid #E1E9F2;border-radius:16px;padding:15px 17px;box-shadow:0 4px 18px #2A4B7B0A}
.stButton > button[kind="primary"]{background:linear-gradient(90deg,#D63384,#B52E90);border:none;color:white;border-radius:11px}
[data-testid="stDownloadButton"] button{border-radius:11px}
.dk-hero{background:linear-gradient(120deg,#132B56,#214B77);color:white;padding:23px 26px;border-radius:20px;margin:6px 0 20px;box-shadow:0 12px 25px #244A7D22}
.dk-hero h1{color:white!important;margin:0;font-size:2rem}
.dk-hero p{color:#BBDCED;margin:9px 0 0;font-size:1rem}
.dk-kicker{color:#76E7F4!important;font-weight:700;letter-spacing:.12em;font-size:.77rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="dk-hero"><div class="dk-kicker">SDK · TOUCH YOUR FUTURE · FINAL CLASSROOM PROJECT</div><h1>DataForge Studio ✦</h1><p>Explore → Clean → Encode & Scale → TF-IDF → Visualize → Log → Publish</p></div>""", unsafe_allow_html=True)

DEMO = Path(__file__).parent / "data" / "sdk_classroom_demo_SYNTHETIC.csv"
with st.sidebar:
    st.header("🗂️ Dataset")
    st.caption("Upload the Kaggle CSV to use the real dataset. The included sample is synthetic.")
    uploaded = st.file_uploader("Upload Kaggle CSV", type=["csv"])
    if uploaded is not None:
        file_bytes = uploaded.getvalue()
        signature = hashlib.sha256(file_bytes).hexdigest()
        try:
            df = pd.read_csv(io.BytesIO(file_bytes))
        except Exception as exc:
            st.error(f"Couldn't read CSV: {exc}")
            st.stop()
        source_name = uploaded.name
        real_upload = True
    else:
        df = pd.read_csv(DEMO)
        signature = "sdk-synthetic-sample"
        source_name = "SDK classroom demo (SYNTHETIC)"
        real_upload = False
    st.markdown("**Current source:**")
    st.caption(source_name)
    st.markdown("[Get real Kaggle dataset](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews)")
    st.divider()
    st.caption("No ML model is trained. This is a Data Preparation showcase.")

if st.session_state.get("dataset_sig") != signature:
    st.session_state["dataset_sig"] = signature
    st.session_state.pop("result", None)
    st.session_state.pop("batch_result", None)

if not real_upload:
    st.info("You're viewing a small **synthetic SDK classroom sample**. Upload the actual Kaggle CSV for the full 23,486-review project.")

page1, page2, page3, page4 = st.tabs([
    "01 · Explore & Visualize", "02 · Pipeline Builder", "03 · Results & Logging", "04 · Publish"
])

with page1:
    st.subheader("Explore the raw dataset")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{df.shape[1]:,}")
    c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    c4.metric("Exact duplicate rows", f"{int(df.duplicated().sum()):,}")
    st.dataframe(df.head(25), use_container_width=True, hide_index=True)
    with st.expander("Data types and missing values — EDA", expanded=True):
        st.dataframe(quality_report(df), use_container_width=True, hide_index=True)
        missing = df.isna().sum().rename_axis("Column").reset_index(name="Missing")
        fig = px.bar(missing, x="Column", y="Missing", title="Missing values by feature", color_discrete_sequence=["#D63384"])
        fig.update_layout(height=320, margin=dict(l=10,r=10,t=52,b=20))
        st.plotly_chart(fig, use_container_width=True)

    left,right = st.columns(2)
    with left:
        rating = "Rating" if "Rating" in df.columns else None
        if rating:
            counts = df[rating].value_counts(dropna=False).sort_index().rename_axis("Rating").reset_index(name="Count")
            fig = px.bar(counts, x="Rating", y="Count", color_discrete_sequence=["#2563EB"], title="Customer ratings")
            fig.update_layout(height=310, margin=dict(l=10,r=10,t=52,b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No Rating column selected in this dataset.")
    with right:
        group_col = next((c for c in ["Department Name","Class Name","Category"] if c in df), None)
        if group_col:
            group = df[group_col].fillna("Unknown").value_counts().head(8).rename_axis(group_col).reset_index(name="Count")
            fig = px.bar(group, x="Count", y=group_col, orientation="h", color_discrete_sequence=["#00B8D9"], title="Top categories")
            fig.update_layout(height=310, margin=dict(l=10,r=10,t=52,b=10), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No category column found for the sample chart.")
    st.caption("Teaching point: EDA is before preprocessing. A rating is an ordinal score; a product ID is an identifier, not a continuous numeric measure.")

with page2:
    st.subheader("Configure the preprocessing pipeline")
    st.caption("Same code handles numerical, categorical and text columns. Select roles; do not encode identifiers as ordinary numbers.")
    all_cols = list(df.columns)
    n_defaults = [c for c in ["Age", "Positive Feedback Count", "Review Length"] if c in all_cols]
    c_defaults = [c for c in ["Department Name", "Class Name", "Category", "Channel"] if c in all_cols]
    t_default = next((c for c in ["Review Text", "review_text"] if c in all_cols), None)
    n_cols = st.multiselect("🔢 Numerical → median imputation + StandardScaler", all_cols, default=n_defaults)
    c_cols = st.multiselect("🏷️ Categorical → fill Unknown + OneHotEncoder", all_cols, default=c_defaults)
    text_choice = st.selectbox("📝 Text → cleaning + TF-IDF", ["(No text)"]+all_cols,
                               index=1+all_cols.index(t_default) if t_default else 0)
    text_col = None if text_choice == "(No text)" else text_choice
    selected = n_cols+c_cols+([text_col] if text_col else [])
    if len(selected) != len(set(selected)):
        st.error("A column was assigned to more than one role. Please fix the selection.")
    elif not selected:
        st.warning("Select at least one feature.")
    else:
        st.markdown("**How the data will move**")
        c1,c2,c3 = st.columns(3)
        c1.info(f"**Numerical**\n\n{len(n_cols)} columns\n\nImputer → Scaler")
        c2.info(f"**Categorical**\n\n{len(c_cols)} columns\n\nUnknown → One-Hot")
        c3.info(f"**NLP**\n\n{'1 text column' if text_col else 'Not selected'}\n\nCleaning → TF-IDF")
        if st.button("▶ Run preprocessing & capture logs", type="primary", use_container_width=True):
            with st.spinner("Building your feature matrix..."):
                try:
                    result = run_pipeline(df, n_cols, c_cols, text_col)
                except Exception as exc:
                    st.error(f"Pipeline failed: {exc}")
                else:
                    st.session_state["result"] = result
                    st.session_state.pop("batch_result",None)
                    st.success("Pipeline completed. Open **03 · Results & Logging** to see each stage.")

with page3:
    result = st.session_state.get("result")
    if result is None:
        st.warning("First run a pipeline in **02 · Pipeline Builder**.")
    else:
        st.subheader("Processing results")
        c1,c2,c3,c4 = st.columns(4)
        matrix = result["matrix"]
        c1.metric("Processed rows", f"{matrix.shape[0]:,}")
        c2.metric("Generated features", f"{matrix.shape[1]:,}")
        c3.metric("Numeric matrix NaNs", "0")
        c4.metric("Execution time", f"{result['seconds']:.2f}s")
        st.caption("The readable cleaned table may still contain missing numeric values; median imputation happens inside the numeric Pipeline, so the final feature matrix has no NaNs.")
        st.markdown("**Raw vs cleaned text (NLP)**")
        roles = result["roles"]
        if roles[2]:
            text_compare = pd.DataFrame({"Original": df[roles[2]].head(6), "Cleaned": result["cleaned"][roles[2]].head(6)})
            st.dataframe(text_compare, use_container_width=True)
        else:
            st.caption("No text feature selected this run.")
        st.markdown("**Before vs after — missing values**")
        before = int(df[roles[0]+roles[1]+([roles[2]] if roles[2] else [])].isna().sum().sum())
        compare = pd.DataFrame({"Stage": ["Selected raw data", "Feature matrix"], "Missing cells": [before, 0]})
        fig = px.bar(compare, x="Stage", y="Missing cells", color="Stage", color_discrete_sequence=["#D63384", "#00B8D9"])
        fig.update_layout(showlegend=False,height=280, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Numerical feature matrix preview**")
        n_view = min(12, matrix.shape[1]); r_view = min(8, matrix.shape[0])
        sample = matrix[:r_view,:n_view]
        sample = sample.toarray() if hasattr(sample, "toarray") else sample
        st.dataframe(pd.DataFrame(sample, columns=result["features"][:n_view]).round(3),use_container_width=True,hide_index=True)
        st.caption("Only the first 12 feature columns are shown; TF-IDF generates many more. The full matrix is not densified.")

        st.subheader("📋 Pipeline execution logs")
        st.code(result["logs"], language="text")
        st.caption("INFO = completed step · WARNING = quality concern · ERROR/traceback = failure. Logs are captured per click, not persisted on Community Cloud.")
        l,r=st.columns(2)
        l.download_button("⬇ Download cleaned CSV", result["cleaned"].to_csv(index=False).encode("utf-8-sig"), "cleaned_reviews.csv", mime="text/csv")
        r.download_button("⬇ Download execution log", result["logs"], "pipeline.log", mime="text/plain")
        with st.expander("Optional: check that a new batch uses the same fitted features"):
            st.caption("Upload another CSV with the same selected columns. Use transform() — no refitting.")
            new_batch_file = st.file_uploader("Upload new batch CSV", type="csv", key="new_batch")
            if new_batch_file is not None and st.button("Transform new batch"):
                try:
                    next_df = pd.read_csv(new_batch_file)
                    next_mat = transform_new_batch(result["pipeline"], next_df, *roles)
                    st.success(f"New batch: {next_mat.shape[0]} rows × {next_mat.shape[1]} features (same vocabulary/schema).")
                except Exception as exc:
                    st.error(str(exc))

with page4:
    st.subheader("Publish on Streamlit Community Cloud")
    st.write("**Students publish the same project they built today.** The app only needs Python files, a demo CSV, and `requirements.txt` on GitHub.")
    st.markdown("""
1. Create a new **GitHub repository** and upload `app.py`, `engine.py`, `requirements.txt`, and the `data/` folder.
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Choose **Create app → Yup, I have an app**.
4. Select the repository and branch, set the main file path to **`app.py`**, and choose **Deploy**.
5. Open the published URL. The synthetic demo works instantly; upload the **real Kaggle CSV** from the sidebar.
    """)
    st.info("Google Colab stays your code practice environment. Community Cloud runs the published app from GitHub. Do not rely on Colab tunnels for your final app.")
    st.caption("Important: session results and in-memory logs reset when the app restarts. No permanent database or model training is required in this final class.")
