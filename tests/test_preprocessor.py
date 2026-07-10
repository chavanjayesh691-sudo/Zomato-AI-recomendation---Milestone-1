import pandas as pd

from src.data.preprocessor import preprocess_dataframe


def test_preprocess_basic():
    df = pd.DataFrame([
        {"name": "A", "location": "Bengaluru", "cuisines": "Italian, Pizza", "rate": "4.1/5", "approx_cost(for two people)": "₹800", "votes": "10"},
        {"name": "", "location": "Delhi", "cuisines": "Chinese", "rate": "3.9/5", "approx_cost(for two people)": "500", "votes": "5"},
    ])

    out = preprocess_dataframe(df)
    assert not out.empty
    assert all(col in out.columns for col in ["name", "location", "cuisines", "rating", "cost_for_two", "votes"])
    assert out.iloc[0]["location"] == "bangalore"
    assert out.iloc[0]["rating"] == 4.1
    assert out.iloc[0]["cost_for_two"] == 800
