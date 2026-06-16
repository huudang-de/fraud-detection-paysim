import pytest
import pandas as pd
from lightgbm import LGBMClassifier

from src.data_loader import (
    load_paysim_data,
    filter_modeling_scope,
    split_by_time,
    balance_training_data
)
from src.features import build_features, split_xy
from src.model_eval import build_profit_curve, find_best_threshold

@pytest.fixture(scope="module")
def raw_data_path(tmp_path_factory):
    """
    Creates a small, temporary raw CSV file to simulate the real data source.
    This fixture runs only once per test module.
    """
    # Create a temporary directory for the test data
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "raw_paysim.csv"

    # Creare a small but representative DataFrame
    data = {
        'step': list(range(1, 21)),
        'type': ['PAYMENT', 'TRANSFER', 'CASH_OUT'] * 6 + ['TRANSFER', 'CASH_OUT'],
        'amount': [100.0] * 20,
        'nameOrig': ['C123'] * 20,
        'oldbalanceOrg': [1000.0] * 20,
        'newbalanceOrig': [900.0] * 20,
        'nameDest': ['M123'] * 10 + ['C456'] * 10,
        'oldbalanceDest': [0.0] * 20,
        'newbalanceDest': [100.0] * 20,
        'isFraud': [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        'isFlaggedFraud': [0] * 20
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return str(file_path)

def test_full_pipeline(raw_data_path):
    """
    Test the full data processing and modeling pipeline from end to end.
    This test ensures that all components (data loading, feature engineering,
    training, evaluation) connect and run without error.
    """ 
    # Data loading and Preprocessing
    raw_df = load_paysim_data(raw_data_path)
    scoped_df = filter_modeling_scope(raw_df)
    train_df, test_df = split_by_time(scoped_df, test_size=0.3)
    balanced_train_df = balance_training_data(train_df)

    # Assert that the dataframes are created and not empty
    assert not raw_df.empty
    assert not scoped_df.empty
    assert not train_df.empty
    assert not test_df.empty
    assert not balanced_train_df.empty

    # Feature engineering
    train_features = build_features(balanced_train_df)
    test_features = build_features(test_df)
    X_train, y_train = split_xy(train_features)
    X_test, y_test = split_xy(test_features)

    # Assert that features and targets are correctly split
    assert not X_train.empty
    assert not y_train.empty

    # Model training and Prediction
    model = LGBMClassifier(random_state=42)
    model.fit(X_train, y_train)
    test_df['prob'] = model.predict_proba(X_test)[:, 1]

    # Evaluation
    profit_curve = build_profit_curve(test_df)
    best_point = find_best_threshold(profit_curve)

    # Assert that the evaluation ran and produced results
    assert isinstance(profit_curve, pd.DataFrame)
    assert not profit_curve.empty
    assert 'profit_vs_approve_all' in best_point