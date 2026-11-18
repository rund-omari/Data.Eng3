# SDK DataForge Studio — FINAL 2-HOUR LIVE CLASS

**Purpose:** Show how EDA, Data Cleaning, Encoding, Scaling, NLP (TF-IDF), Python Logging, and Streamlit fit into *one* reusable application. **No ML model training.**

## Real Kaggle dataset

Download **Women's E-Commerce Clothing Reviews**:  
https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews

The real source contains about **23,486 customer reviews**, including Age, Rating, Review Text, product departments and classes. Upload the real **Womens Clothing E-Commerce Reviews.csv** using the app sidebar. The Kaggle file is **not bundled** (it could not be fetched directly in this environment). `data/sdk_classroom_demo_SYNTHETIC.csv` is a fictional SDK classroom sample, **not Kaggle data**. It is included so deployment runs immediately while students download the dataset.

## Files (few, intentional)

- `app.py`: Streamlit dashboard, charts, widgets, results and publishing instructions
- `engine.py`: reusable preprocessing, logging and `ColumnTransformer` (no Streamlit dependency)
- `data/sdk_classroom_demo_SYNTHETIC.csv`: sample only
- `requirements.txt`: dependencies for deployment
- `Colab_Practice.ipynb`: short practice calling the same `engine.py`
- `INSTRUCTOR_LIVE_SCRIPT_AR.md`: minute-by-minute teaching plan
- `tests/test_engine.py`: basic quality checks

## Run locally or in GitHub Codespaces

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Google Colab workflow

- Students upload or clone the project into Colab, upload the Kaggle CSV, then import `engine.py`.
- Colab **is not hosting** the final Streamlit site. The app runs locally/Codespaces or from GitHub in **Streamlit Community Cloud**.
- The results/logs are in memory per session, not a persistent history.

## Deploy (free Community Cloud)

1. Upload the project files and `data/` folder to a GitHub repository (do not upload `__pycache__`).
2. Open https://share.streamlit.io and sign in with GitHub.
3. Create app → *Yup, I have an app* → select repository, branch and `app.py` entrypoint.
4. Deploy and open the resulting shareable link. The synthetic sample runs immediately; upload the real Kaggle CSV to the deployed app.

## Teaching decisions

- `Clothing ID` identifies a product; do not automatically scale it.
- `Rating` is ordinal; use it for EDA; do not treat it as a random continuous measure without a reason.
- Text cleaning retains `not`; overly aggressive cleaning can damage sentiment information.
- IQR outliers are flagged in the logs **but not deleted automatically**.
- Missing numeric values are imputed **inside the fitted `Pipeline`**, even if the readable interim DataFrame still displays NaN.
- Duplicate reviews or records are flagged, not automatically removed.
- This is **data preparation only**; since no ML evaluation occurs, the reference dataset is used for `fit_transform()`. If students later train predictive models, **split before fitting** any learned preprocessing.
- A new batch with the same columns uses `transform()`. A different schema requires a new configuration/fitted pipeline.

## Test

```bash
python -m pytest tests -q
```
