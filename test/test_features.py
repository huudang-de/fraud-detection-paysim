import pytest
import pandas as pd
import numpy as np

# Import the functions and variables you need to test
from src.features import build_features, split_xy, MODEL_FEATURE_COLUMNS

@pytest.fixture
def sample_data():
    """Provides a normal, sample DataFrame for testing."""
    # Try to create a dictionary with sample data here
    # It should include columns like 'step', 'type', 'amount', 'oldbalanceDest', 'isFraud', ...
    data = {
        'step': [1, 1, 2],
        'type': ['PAYMENT', 'TRANSFER', 'CASH_OUT'],
        'amount': [9839.64, 181.00, 181.00],
        'oldbalanceDest': [0.0, 0.0, 21182.0],
        'isFraud': [0, 1, 1],
        # Add other necessary columns from the original dataset
        'nameOrig': ['C123', 'C456', 'C789'],
        'oldbalanceOrg': [170136.0, 181.0, 181.0],
        'newbalanceOrig': [160296.36, 0.0, 0.0],
        'nameDest': ['M123', 'C456_dest', 'C789_dest'],
        'newbalanceDest': [0.0, 0.0, 0.0],
        'isFlaggedFraud': [0, 0, 0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def empty_data():
    """Provides an empty DataFrame with the correct columns."""
    # Retrun an empty DataFrame, but define the columns is should have
    return pd.DataFrame(columns=[
        'step', 'type', 'amount', 'oldbalanceDest', 'isFraud', 'isFlaggedFraud',
        'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'newbalanceDest'
    ])

@pytest.fixture
def data_with_nulls():
    """Provides a DataFrame containing NaN values."""
    # Create a dictionary with some np.nan values in key columns like 'type' or 'amount'
    data = {
        'step': [1, 2, 3],
        'type': ['PAYMENT', 'TRANSFER', np.nan],
        'amount': [100.0, 200.0, np.nan],
        'oldbalanceDest': [0.0, 0.0, 100.0],
        'isFraud': [0, 1, 0]
    }
    return pd.DataFrame(data)

def test_build_features_normal_data(sample_data):
    """
    Tests that build_features correctlt engineers features from normal data. 
    """
    # Act: Call the function with your sample data
    features_df = build_features(sample_data)

    # Assert: Check if the results are correct
    # 1. Is the output a DataFrame?
    assert isinstance(features_df, pd.DataFrame)

    # 2. Does it have the right columns?
    expected_cols = set(MODEL_FEATURE_COLUMNS + ['isFraud'])
    assert set(features_df.columns) == expected_cols

    # 3.Are the calculated values correct? This is the most important part
    # Check a specific row. For the 'TRANSFER' row (index 1):
    # -'is_high_risk_type' should be 1
    # -'hour' should be 1
    # -'is_night' should be 0
    assert features_df.loc[1, 'is_high_rish_type'] == 1
    assert features_df.loc[1, 'hour'] == 1
    assert features_df.loc[1, 'is_night'] == 0

def test_build_features_empty_data(empty_data):
    """
    Tests that the function handles an emplty Dataframe without crashing.
    """ 


