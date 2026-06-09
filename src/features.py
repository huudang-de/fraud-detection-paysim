import pandas as pd
import numpy as np

MODEL_FEATURE_COLUMNS = [
    'amount',
    'is_high_risk_type',
    'log_amount',
    'hour',
    'is_night',
    'is_dest_zero_balance',
    'high_risk_combo',
]

TARGET_COLUMN = 'isFraud'

LEAKAGE_PRONE_COLUMNS = {
    'oldbalanceOrg',
    'newbalanceOrig',
    'oldbalanceDest',
    'newbalanceDest',
    'isFlaggedFraud',
}

def build_features(df):
    '''
    Build only T0-safe features for real-time fraud scoring.

    Balance columns are intentionally not passed through as raw model inputs.
    is_dest_zero_balance is retained as a business hypothesis, but it must be
    backed by a pre-authorization balance snapshot in production.
    '''
    df = df.copy()

    required_columns = {'type', 'amount', 'step', 'oldbalanceDest'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns for feature engineering: {sorted(missing_columns)}")

    df['is_high_risk_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)

    df['log_amount'] = np.log1p(df['amount'])

    df['hour'] = df['step'] % 24
    df['is_night'] = ((df['hour'] < 6) | (df['hour'] > 22)).astype(int)

    df['is_dest_zero_balance'] = (df['oldbalanceDest'] == 0).astype(int)

    df['high_risk_combo'] = df['is_high_risk_type'] * df['is_dest_zero_balance'] * df['is_night']

    output_columns = MODEL_FEATURE_COLUMNS.copy()
    if TARGET_COLUMN in df.columns:
        output_columns.append(TARGET_COLUMN)

    return df[output_columns]

def split_xy(df):
    unexpected_leakage_columns = LEAKAGE_PRONE_COLUMNS.intersection(df.columns)
    if unexpected_leakage_columns:
        raise ValueError(
            "Leakage-prone columns found in model frame: "
            f"{sorted(unexpected_leakage_columns)}"
        )

    missing_features = set(MODEL_FEATURE_COLUMNS) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing model features: {sorted(missing_features)}")
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    X = df[MODEL_FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X,y
