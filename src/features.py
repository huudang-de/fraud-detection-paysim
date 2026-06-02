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
    """
    Build features for fraud detection model.
    
    Creates domain-specific features based on transaction patterns,
    temporal information, and account behavior. Features are engineered
    to capture fraud indicators: high-risk transaction types, nighttime
    activity, and suspicious recipient accounts.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe with raw transaction data.
        Required columns: type, amount, step, oldbalanceDest.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with engineered features and original isFraud target.
    
    Raises
    ------
    ValueError
        If required columns are missing from input dataframe.
    
    Examples
    --------
    >>> df = pd.read_csv('transactions.csv')
    >>> features = build_features(df)
    >>> features.shape
    (6362620, 7)
    
    Notes
    -----
    - High-risk types: TRANSFER, CASH_OUT
    - Night hours: 23:00-05:59 (peak fraud window)
    - Zero balance: Indicator of account depletion
    - T0-safe: Uses only pre-transaction information
    """
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
    
    """
    Safely splits a DataFrame into a feature matrix (X) and a target vector (y).

    This function acts as a risk control filter before feeding data into a model.
    It prevents data leakage from forward-looking information and ensures the 
    input matrix contains the exact required economic and financial variables.

    Parameters
    ----------
    df : pandas.DataFrame
        The raw or preprocessed dataset. Required conditions for the input:
        - Must contain the dependent variable column (defined in TARGET_COLUMN).
        - Must contain all core independent variables (defined in MODEL_FEATURE_COLUMNS).
        - Must strictly NOT contain any information-leaking columns (defined in LEAKAGE_PRONE_COLUMNS).

    Returns
    -------
    tuple
        X : pandas.DataFrame
            The explicitly extracted feature matrix. Irrelevant identifier columns
            (e.g., Customer ID, Branch Code) without quantitative analytical value
            are automatically excluded.
        Y : pandas.Series
            A 1-dimensional vector containing the target variable values (e.g.,
            default status, bankruptcy probability).
    
    Raises
    ------
    ValueError
        - If `df` contains any columns present in `LEAKAGE_PRONE_COLUMNS` (e.g.,
        finding a 'going_concern_audit_opinion' column when predicting future bankruptcy).
        - If `df` is missing any required economic/financial features listed in `MODEL_FEATURE_COLUMNS`.
        - If `df` does not contain the `TARGET_COLUMN`.
    
    Examples
    --------
    >>> # Assuming TARGET_COLUMN = 'is_bankrupt'
    >>> # Assuming MODEL_FEATURE_COLUMNS = ['ROA', 'Debt_to_Equity', 'interest_rate']
    >>> df = pd.DataFrame({
    ...     'ROA': [0.05, -0.02, 0.08],
    ...     'Debt_to_Equity': [1.2, 2.5, 0.8],
    ...     'interest_rate': [0.04, 0.05, 0.04],
    ...     'is_bankrupt': [0, 1, 0],
    ...     'Customer_ID': ['C01', 'C02', 'C03'] # Noisy identifier column
    ... })
    >>> X, y = split_xy(df)
    >>> X.columns.tolist()
    ['ROA', 'Debt_to_Equity', 'interest_rate']
    """
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
    return X, y
