import numpy as np
import pandas as pd
import pytest
from engine import clean_text, quality_report, run_pipeline, transform_new_batch


def test_clean_text_and_negation():
    assert clean_text("<b>NOT &amp; good!!!</b>") == "not & good!!!"
    assert clean_text(None) == ""


def test_quality_report():
    result = quality_report(pd.DataFrame({"a": [1, None]}))
    assert result.loc[0, "Missing"] == 1


def test_all_roles_and_new_batch():
    df = pd.DataFrame({
        "Age": [20, 30, None, 45],
        "Dept": ["A", None, "B", "A"],
        "Review Text": ["very good product", "not good", "bad delivery", "nice dress"],
    })
    run = run_pipeline(df, ["Age"], ["Dept"], "Review Text")
    assert run["matrix"].shape[0] == 4
    assert "STEP 6/6" in run["logs"]
    new = pd.DataFrame({"Age": [22], "Dept": ["NEW"], "Review Text": ["unseen product"]})
    new_matrix = transform_new_batch(run["pipeline"], new, ["Age"], ["Dept"], "Review Text")
    assert new_matrix.shape == (1, run["matrix"].shape[1])
    values = run["matrix"].data if hasattr(run["matrix"], "tocsr") else np.asarray(run["matrix"])
    assert np.isfinite(values).all()


def test_without_text():
    df = pd.DataFrame({"Amount": [1.0, None, 3.0], "Category": ["X", "Y", "X"]})
    run = run_pipeline(df, ["Amount"], ["Category"])
    assert run["matrix"].shape[0] == 3


def test_duplicate_role_rejected():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(ValueError, match="one role"):
        run_pipeline(df, ["a"], ["a"])
