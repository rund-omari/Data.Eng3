# Student Live Coding — SDK DataForge Studio

**Goal:** Show *how* preprocessing runs, not just its final output. You can build a similar project with your own dataset after class.

## Step 1 — Inspect the data

Download Kaggle [Women's E-Commerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews). Read with Pandas and inspect `.head()`, `.info()`, `.isna().sum()`. Identify numerical, categorical and text columns. Don't use `Clothing ID` as numeric by default.

## Step 2 — Separate responsibilities

Open `engine.py` — reusable Pandas/Scikit-learn functions, **without Streamlit**. Open `app.py` — just Streamlit widgets, tables and Plotly charts. This means notebooks and apps reuse the same logic.

## Step 3 — Trace the code

Trace one raw review through:
`clean_text()` → `prepare_reference()` → `build_pipeline()` → `run_pipeline()` → feature matrix.

Note the branches:
- Numerical: `SimpleImputer(median)` → `StandardScaler`
- Categorical: fill missing category → `OneHotEncoder`
- Text: HTML/URL cleanup → `TfidfVectorizer` (includes n-grams)

## Step 4 — Turn processing into a visual app

In `app.py`, identify and explain:
`st.file_uploader`, `st.metric`, `st.dataframe`, `st.plotly_chart`, `st.multiselect`, `st.button`, `st.session_state`, `st.code`, `st.download_button`.

## Step 5 — Logging

In `engine.py`, find `logging.basicConfig()`, `.info()`, `.warning()`, `.exception()`. Click **Run preprocessing & capture logs**, then open Results & Logging. Explain each step and any warnings.

## Step 6 — Publish

Upload the files to GitHub, deploy `app.py` on Streamlit Community Cloud, and share the URL. Upload Kaggle data within the deployed app.

## Exit ticket

Submit:
- GitHub repository URL
- Published Streamlit URL
- Screenshot of Results & Logging
- Two sentences: (1) Why `ColumnTransformer`? (2) What is one reason to use `logging`?

**Remember:** No machine learning model is trained. A later prediction project would need a train/test split *before* fitting learned preprocessing.
