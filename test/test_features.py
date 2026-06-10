import pytest
import pandas as pd
import numpy as np
from src.features import build_features, split_xy, MODEL_FEATURE_COLUMNS


@pytest.fixture
def sample_data():
    """
    Provides a sample DataFrame with normal data for testing.
    This data simulates rows from the PaySim file.
    """
    data = {
        'step': [1, 1, 2],
        'type': ['PAYMENT', 'TRANSFER', 'CASH_OUT'],
        'amount': [9839.64, 181.00, 181.00],
        'nameOrig': ['C123', 'C456', 'C789'],
        'oldbalanceOrg': [170136.0, 181.0, 181.0],
        'newbalanceOrig': [160296.36, 0.0, 0.0],
        'nameDest': ['M123', 'C456_dest', 'C789_dest'],
        'oldbalanceDest': [0.0, 0.0, 21182.0],
        'newbalanceDest': [0.0, 0.0, 0.0],
        'isFraud': [0, 1, 1],
        'isFlaggedFraud': [0, 0, 0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_data():
    """Provides an empty DataFrame with the correct columns."""
    return pd.DataFrame(columns=[
        'step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig',
        'nameDest', 'oldbalanceDest', 'newbalanceDest', 'isFraud', 'isFlaggedFraud'
    ])


@pytest.fixture
def data_with_nulls():
    """Provides a DataFrame containing NaN values."""
    data = {
        'step': [1, 2, 3],
        'type': ['PAYMENT', 'TRANSFER', np.nan],
        'amount': [100.0, 200.0, np.nan],
        'oldbalanceDest': [0.0, 0.0, 100.0],
        'isFraud': [0, 1, 0]
    }
    return pd.DataFrame(data)


# --- Tests for Controlled Error Handling ---

def test_build_features_missing_columns_raises_error(sample_data):
    """
    Tests that build_features raises an error if a critical input column is missing.
    """
    # GIVEN: Data is missing the 'type' column
    data_missing_col = sample_data.drop(columns=['type'])

    # WHEN/THEN: Calling build_features should raise a ValueError
    with pytest.raises(ValueError, match="Missing required columns"):
        build_features(data_missing_col)

def test_split_xy_leakage_raises_error(sample_data):
    """
    Tests that split_xy raises an error if a potential data leakage column is found.
    """
    # GIVEN: Data contains a leakage-prone column ('newbalanceDest')
    data_with_leakage = build_features(sample_data)
    data_with_leakage['newbalanceDest'] = 0 # Add a column from LEAKAGE_PRONE_COLUMNS

    # WHEN/THEN: Calling split_xy should raise a ValueError
    with pytest.raises(ValueError, match="Leakage-prone columns found"):
        split_xy(data_with_leakage)

def test_split_xy_missing_features_raises_error(sample_data):
    """
    Tests that split_xy raises an error if a required model feature is missing.
    """
    # GIVEN: Feature-engineered data is missing the 'hour' column
    features_df = build_features(sample_data).drop(columns=['hour'])

    # WHEN/THEN: Calling split_xy should raise a ValueError
    with pytest.raises(ValueError, match="Missing model features"):
        split_xy(features_df)

def test_split_xy_missing_target_raises_error(sample_data):
    """
    Tests that split_xy raises an error if the target column is missing.
    """
    # GIVEN: Data is missing the 'isFraud' target column
    features_df = build_features(sample_data).drop(columns=['isFraud'])

    # WHEN/THEN: Calling split_xy should raise a ValueError
    with pytest.raises(ValueError, match="Missing target column"):
        split_xy(features_df)

# --- Tests for the build_features function ---

def test_build_features_normal_data(sample_data):
    """
    Test the build_features function with a normal, well-formed DataFrame.
    Objective: Ensure the function runs and creates new features with correct values.
    """
    # WHEN the build_features function is called
    features_df = build_features(sample_data)

    # THEN:
    # 1. The result must be a DataFrame.
    assert isinstance(features_df, pd.DataFrame)

    # 2. The DataFrame must contain all expected model features plus the target.
    expected_cols = set(MODEL_FEATURE_COLUMNS + ['isFraud'])
    assert set(features_df.columns) == expected_cols

    # 3. Verify that the feature values have been calculated correctly.
    # Row 0: type='PAYMENT' should result in is_high_risk_type=0.
    assert features_df.loc[0, 'is_high_risk_type'] == 0
    # Row 1: type='TRANSFER' should result in is_high_risk_type=1.
    assert features_df.loc[1, 'is_high_risk_type'] == 1
    # step=1 should result in hour=1 and is_night=0.
    assert features_df.loc[0, 'hour'] == 1
    assert features_df.loc[0, 'is_night'] == 1
    # oldbalanceDest=0.0 should result in is_dest_zero_balance=1.
    assert features_df.loc[0, 'is_dest_zero_balance'] == 1

def test_build_features_empty_data(empty_data):
    """
    Tests the build_features function with an empty DataFrame.
    Objective: Ensure the function does not crash and returns an empty DataFrame with feature columns.
    """
    # WHEN the function is called
    features_df = build_features(empty_data)

    # THEN:
    assert isinstance(features_df, pd.DataFrame)
    assert features_df.empty
    assert 'hour' in features_df.columns


def test_build_features_with_nulls(data_with_nulls):
    """
    Tests that the build_features function can handle null values without crashing.
    Objective: Ensure the function does not raise an error and maintains DataFrame length.
    """
    # WHEN the function is called with data containing nulls
    features_df = build_features(data_with_nulls)

    # THEN it should not crash and should return a DataFrame of the same length
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(data_with_nulls)


# --- Tests for the split_xy function ---

def test_split_xy_separation_and_leakage_guard(sample_data):
    """
    Tests that split_xy correctly separates X and y and guards against data leakage.
    Objective: Ensure 'isFraud' and other leakage columns are not in X.
    """
    # GIVEN: a feature-engineered dataframe
    features_df = build_features(sample_data)

    # WHEN: splitting into X and y
    X, y = split_xy(features_df)

    # THEN:
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)
    assert len(X) == len(y)
    assert y.name == 'isFraud'
    # Most importantly: The target and leakage-prone columns must not be in the feature set X
    assert 'isFraud' not in X.columns
    assert 'isFlaggedFraud' not in X.columns