import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve


def calculate_ev(prob_fraud, amount, clv_score):
    """
    Calculate expected value for fraud intervention decision.
 
    Computes whether intervening on a transaction has positive expected value using the formula:
    EV = P(fraud) * amount - P(not fraud) * cost_false_positive

    Parameters
    ----------
    prob_fraud: float
        Fraud probability from model (0 to 1).
    amount : float
        Transaction amount in VND.
    clv_score: float
        Customer lifetime value (CLV) in VND.
        Used to calculate churn loss if customer is falsely blocked.

    Returns
    -------
    float
        Expected value of intervention. Positive = intervene,
        Negative = allow transaction
    
    Examples
    --------
    >>> ev = calculate_ev(prob_fraud=0.8, amount=5000000, clv_score=50000000)
    >>> ev > 0
    True

    Notes
    -----
    - Cost of operation: 50,000 VND per intervention
    - Churn rate if falsely blocked: 10%
    - Only fraud loss considered (ignores fraud catch rewards)
    - Use in Decision 2345 fraud intervention strategy
    """
    # Giả định các tham số chi phí 
    cost_operation = 50000 
    p_churn_if_blocked = 0.1 # 1% xác suất mất khách hàng nếu chặn nhầm

    # Tính CFP linh hoạt theo CLV
    cfp = cost_operation + (p_churn_if_blocked * clv_score)

    # EV = P(G) * VG - P(H) * CFP (Bỏ qua CFR cho đơn giản)
    ev = (prob_fraud * amount) - ((1 - prob_fraud) * cfp)

    return ev 

# Quyết định: Nếu EV > 0 thì can thiệp, nếu EV <= 0 thì cho qua

def get_friction_level(prob, amount, clv_score):
    """
    Determine friction level for transaction based on fraud risk.

    Maps fraud probability and transaction amount to intervention level
    using Decision 2345 strategy. Creates 5 friction levels from auto-approval
    to account freeze.

    Parameters
    ----------
    prob : float
        Fraud probability from model (0 to 1).
    amount : float
        Transaction amount in VND.
    clv_score: float
        Customer lifetime value in VND (used for context).

    Returns
    -------
    str
        Friction level name. One of:
        - "Cấp 0: Phê duyệt tự động" (Auto-approve)
        - "Cấp 1: Gửi SMS/Notification" (Send SMS)
        - "Cấp 2: Sinh trắc học FaceID" (FaceID request)
        - "Cấp 3: Video Call/Tạm dừng 30p" (Video call + pause)
        - "Cấp 4: Đóng băng tài khoản" (Freeze account)

    Examples
    --------
    >>> level = get_friction_level(prob=0.9, amount=5000000, clv_score=50000000)
    >>> level
    'Cấp 3: Video Call/Tạm dừng 30p'

    Notes
    -----
    - Decision 2345 threshold: 10 triệu VND
    - Probability thresholds: 0.95, 0.8, 0.5, 0.2
    - Friction increases with both probability and amount
    - Used in production fraud intervention system
    """
    # Kết hợp Xác suất và Quyết định 2345 (Ngưỡng 10 triệu)
    if prob >= 0.95:
        return "Cấp 4: Đóng băng tài khoản"
    elif prob >= 0.8:
        return "Cấp 3: Video Call/Tạm dừng 30p"
    elif prob >= 0.5 or amount >= 10000000: # QĐ 2345
        return "Cấp 2: Sinh trắc học FaceID"
    elif prob >= 0.2:
        return "Cấp 1: Gửi SMS/Notification"
    else:
        return "Cấp 0: Phê duyệt tự động"


def decision_loss(df, decision_col, target_col='isFraud', amount_col='amount', cost_fp=5050000):
    """
    Calculates the total financial loss based on the decisions of a fraud detection model.
 
    This function evaluates the performance of a classification model by mapping
    technical errors (missed frauds and false alarms) to actual monetary costs.
    This approach helps organizations optimize their decision threshold based on 
    real-world cost efficiency rather than purely technical metrics.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataset containing transaction history and predicted labels.
    decision_col : str
        The name of the column containing the predicted decisions
        (1: Block transaction, 0: Allow transaction).
    target_col : str, optional
        The name of the column containing the actual label
        (1: Actual fraud, 0: Legitimate transaction). Defaults to 'isFraud'.
    amount_col : str, optional 
        The name of the column representing the transaction amount. Used to
        calculate the financial damage when a fraudulent transaction is missed.
        Defaults to 'amount'.
    cost_fp : int or float, optional
        The estimated average operational cost for a single false alarm (False Positive). 
        This includes personnel costs for verification calls, complaint handling,
        and losses due to disrupted customer experience. Defaults to 5,050,000.

    Returns
    -------
    dict
        A dictionary containing the financial loss and evaluation metrics:
        - 'loss': Total financial loss (loss_fn + loss_fp)
        - 'loss_fn': Loss due to missed frauds (False Negatives).
        - 'loss_fp': Loss due to false alarms (False Positives).
        - 'tp': Count of True Positives (correctly blocked frauds).
        - 'fp': Count of False Positives (incorrectly blocked legitimate transactions).
        - 'fn': Count of False Negatives (missed frauds).
        - 'tn': Count of True Negatives (correctly allowed legitimate transactions).
    
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'isFraud': [1, 0, 1, 0],
    ...     'predicted_decision': [1, 1, 0, 0],
    ...     'amount': [100000, 50000, 200000, 30000]
    ... })
    >>> decision_loss(df, 'predicted_decision', cost_fp=50000)
    {'loss': 250000.0, 'loss_fn': 200000.0, 'loss_fp': 50000.0, 'tp': 1, 'fp': 1, 'fn': 1, 'tn': 1}
    """
    fraud = df[target_col] == 1
    alerted = df[decision_col] == 1

    loss_fn = df.loc[fraud & ~alerted, amount_col].sum()
    loss_fp = int((~fraud & alerted).sum()) * cost_fp

    return {
        'loss': float(loss_fn + loss_fp),
        'loss_fn': float(loss_fn),
        'loss_fp': float(loss_fp),
        'tp': int((fraud & alerted).sum()),
        'fp': int((~fraud & alerted).sum()),
        'fn': int((fraud & ~alerted).sum()),
        'tn': int((~fraud & ~alerted).sum()),
    }


def build_profit_curve(df, score_col='prob', target_col='isFraud', amount_col='amount', cost_fp=5050000):
    """
    Builds a profit curve by evaluating financial outcomes across all score thresholds.

    Sorts transactions by predicted score in descending order and evaluates the 
    financial impact of setting the decision threshold at every possible score.
    The returned profit is relative to a baseline of "approving everything,"
    where all fraud amounts are lost and no false-positive costs are incurred.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataset containing predictions, actual labels, and transaction amounts.
    score_col : str, optional
        The name of the column containing the predicted fraud probabilities or scores.
        Defaults to 'prob'.
    target_col : str, optional
        The name of the column containing the actual ground truth labels
        (1 for fraud, 0 for legitimate). Defaults to 'isFraud'.
    amount_col : str, optional
        The name of the column representing the transaction monetary amount.
        Defaults to 'amount'.
    cost_fp : int or float, optional
        The estimated average operational cost for a single false alarm (False Positive).
        Defaults to 5050000.

    Returns
    ------
    pandas.DataFrame 
        A DataFrame containing the cumulative evaluation metrics at each threshold level: 
        - 'threshold': The decision threshold score.
        - 'transactions': Number of transactions alerted.
        - 'tp': Cumulative True Positive (correctly caught frauds).
        - 'fp': Cumulative False Positives (incorrectly flagged legitimate transactions).
        - 'caught_fraud_amount': Total monetary amount of fraud prevented.
        - 'missed_fraud_amount': Total monetary amount of fraud missed.
        - 'loss_fp': Total operational cost from false alarms.
        - 'loss': Total financial loss (missed_fraud_amount + loss_fp)
        - 'profit_vs_approve_all': Net savings compared to not having a model.
        - 'alert_rate': Percentage of total transactions flagged at this threshold.

    Raises
    ------
    ValueError
        If required columns ('score_col', 'target_col', or 'amount_col') are missing from 'df'.
    
    Examples
    --------
    >>> data = {
    ...     'prob': [0.9, 0.8, 0.7, 0.6, 0.1],
    ...     'isFraud': [1, 0, 1, 0, 0],
    ...     'amount': [1000, 200, 800, 150, 50]
    ... }
    >>> df = pd.DataFrame(data)
    >>> curve = build_profit_curve(df, cost_fp=100)
    >>> print(curve[['threshold', 'loss', 'profit_vs_approve_all']].round(2).tail())
       threshold   loss  profit_vs_approve_all
    1       0.9  900.0                  900.0
    2       0.8 1000.0                  800.0
    3       0.7  200.0                 1600.0
    4       0.6  300.0                 1500.0
    5       0.1   400.0                 1400.0
    """
    # Check if the input contains all the necessary columns.
    required_cols = {score_col, target_col, amount_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns for profit curve: {sorted(missing_cols)}")

    # Sort the data by descening fraud prediction score.
    ordered = df[[score_col, target_col, amount_col]].sort_values(score_col, ascending=False).copy()
    ordered['_is_fraud'] = ordered[target_col] == 1
    ordered['_fraud_amount'] = np.where(ordered['_is_fraud'], ordered[amount_col], 0.0)
    ordered['_is_legit'] = ~ordered['_is_fraud']

    total_fraud_amount = float(ordered['_fraud_amount'].sum())

    # Group the transactions by score level.
    grouped = (
        ordered
        .groupby(score_col, sort=False)
        .agg(
            transactions=(target_col, 'size'),
            frauds=('_is_fraud', 'sum'),
            legit=('_is_legit', 'sum'),
            caught_fraud_amount=('_fraud_amount', 'sum'),
        )
        .reset_index()
        .rename(columns={score_col: 'threshold'})
    )

    # Summarize the indicators from top to bottom for each threshold.
    grouped['alerted'] = grouped['transactions'].cumsum()
    grouped['tp'] = grouped['frauds'].cumsum().astype(int)
    grouped['fp'] = grouped['legit'].cumsum().astype(int)
    grouped['caught_fraud_amount'] = grouped['caught_fraud_amount'].cumsum()

    # Calculate the  loss and profit.
    grouped['missed_fraud_amount'] = total_fraud_amount - grouped['caught_fraud_amount']
    grouped['loss_fp'] = grouped['fp'] * cost_fp
    grouped['loss'] = grouped['missed_fraud_amount'] + grouped['loss_fp']
    grouped['profit_vs_approve_all'] = total_fraud_amount - grouped['loss']
    grouped['alert_rate'] = grouped['alerted'] / len(ordered)

    # Another baseline scenario: Catch nothing (infinite threshold).
    no_alert = pd.DataFrame([{
        'threshold': np.nextafter(float(ordered[score_col].max()), np.inf),
        'transactions': 0,
        'frauds': 0,
        'legit': 0,
        'alerted': 0,
        'tp': 0,
        'fp': 0,
        'caught_fraud_amount': 0.0,
        'missed_fraud_amount': total_fraud_amount,
        'loss_fp': 0.0,
        'loss': total_fraud_amount,
        'profit_vs_approve_all': 0.0,
        'alert_rate': 0.0,
    }])

    # Connect the scenario into the result table and the results.
    return pd.concat([no_alert, grouped], ignore_index=True)


def find_best_threshold(profit_curve):
    """
    Find the best threshold from a profit curve.

    This function takes a profit curve DataFrame generated by `build_profit_curve`
    and identifies the threshold that results in the minimum total financial loss.

    Parameters
    ----------
    profit_curve : pandas.DataFrame
        The profit curve DataFrame, which must contain a 'loss' column.

    Returns
    -------
    pandas.Series
        A Series containing all information for the row with the minimum loss,
        including the optimal 'threshold', 'loss', 'profit_vs_approve_all',
        and 'alert_rate'.
    
    Raises
    ------
    ValueError
        If the input `profit_curve` DataFrame is empty.
    
    Examples
    --------
    >>> data = {
    ...     'prob': [0.9, 0.8, 0.7, 0.6, 0.1],
    ...     'isFraud': [1, 0, 1, 0, 0],
    ...     'amount': [1000, 200, 800, 150, 50]
    ... }
    >>> df = pd.DataFrame(data)
    >>> curve = build_profit_curve(df, cost_fp=100)
    >>> best_point = find_best_threshold(curve)
    >>> print(f"Optimal Threshold: {best_point['threshold']:.2f}")
    Optimal Threshold: 0.70
    >>> print(f"Minimum Loss: {best_point['loss']:.2f}")
    Minimum Loss: 200.00
    """
    if profit_curve.empty:
        raise ValueError("profit_curve is empty")

    best_idx = profit_curve['loss'].idxmin()
    return profit_curve.loc[best_idx].copy()


def build_roc_curve(y_true, y_score):
    """
    Build a ROC curve and calculate its AUC.

    This function computes the Receiver Operating Characteristic (ROC) curve
    and the Area Under the Curve (AUC) from true labels and predicted scores.
    It is used for monitoring rank separation independent of a decision threshold.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary labels (0 or 1).
    y_score : array-like of shape (n_samples,)
        Predicted probabilities or decision function scores for the positive class.

    Returns
    ------
    pandas.DataFrame
        A DataFrame containing the ROC curve components:
        - 'fpr': False Positive Rate.
        - 'tpr': True Positive Rate.
        - 'thresholds': Thresholds used to compute fpr and tpr.
        - 'auc': The overall Area Under the ROC Curve.
    
    Examples
    --------
    >>> y_true = [0, 0, 1, 1]
    >>> y_scores = [0.1, 0.4, 0.35, 0.8]
    >>> roc_df = build_roc_curve(y_true, y_scores)
    >>> print(roc_df.auc.iloc[0])
    0.75
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    return pd.DataFrame({
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': thresholds,
        'auc': roc_auc,
    })


def build_lift_curve(df, score_col='prob', target_col='isFraud', n_bins=10):
    """
    Build a cumulative lift curve by score quantiles.

    This function measures the effectiveness of a model by showing how much
    more likely we are to find fraud cases in a high-scoring segment compared
    to the overall population average. A lift greater than 1 indicates the
    model has predictive power.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing scores and true labels.
    score_col : str, optional
        The name of the column with model scores. Defaults to 'prob'.
    target_col : str, optional
        The name of the column with true binary labels. Defaults to 'isFraud'.
    n_bins : int, optional
        The number of bins (quantiles) to divide the population into.
        Defaults to 10 (deciles). 
    
    Returns
    -------
    pandas.DataFrame
        A DataFrame summarizing the lift metrics for each bin:
        - 'bin': The quantile number (e.g., 1 to 10 for deciles).
        - 'min_score', 'max_score': Score range for the bin.
        - 'transactions': Number of transactions in the bin.
        - 'events': Number of fraud events in the bin.
        - 'population_pct': Cumulative percentage of the population.
        - 'event_rate': The rate of fraud within that specific bin.
        - 'cumulative_lift': The lift achieved by selecting all bins up to the current one.

    Raises
    ------
    ValueError
        If `n_bins` is less than 2 or if required columns are missing.
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = {'prob': np.random.rand(100), 'isFraud': np.random.randint(0, 2, 100)}
    >>> df = pd.DataFrame(data)
    >>> lift_df = build_lift_curve(df)
    >>> 'cumulative_lift' in lift_df.columns
    True 
    
    """
    if n_bins < 2:
        raise ValueError("n_bins must be >= 2")

    required_cols = {score_col, target_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns for lift curve: {sorted(missing_cols)}")

    ordered = df[[score_col, target_col]].sort_values(score_col, ascending=False).copy()
    ordered['rank'] = np.arange(1, len(ordered) + 1)
    ordered['bin'] = np.ceil(ordered['rank'] / len(ordered) * n_bins).astype(int)
    ordered['bin'] = ordered['bin'].clip(1, n_bins)

    total_events = ordered[target_col].sum()
    base_rate = ordered[target_col].mean()

    grouped = (
        ordered
        .groupby('bin', as_index=False)
        .agg(
            min_score=(score_col, 'min'),
            max_score=(score_col, 'max'),
            transactions=(target_col, 'size'),
            events=(target_col, 'sum'),
        )
    )

    grouped['population_pct'] = grouped['transactions'].cumsum() / len(ordered)
    grouped['event_rate'] = grouped['events'] / grouped['transactions']
    grouped['cumulative_events'] = grouped['events'].cumsum()
    grouped['cumulative_event_rate'] = grouped['cumulative_events'] / grouped['transactions'].cumsum()
    grouped['cumulative_capture_rate'] = np.where(
        total_events > 0,
        grouped['cumulative_events'] / total_events,
        0.0,
    )
    grouped['lift'] = np.where(base_rate > 0, grouped['event_rate'] / base_rate, 0.0)
    grouped['cumulative_lift'] = np.where(
        base_rate > 0,
        grouped['cumulative_event_rate'] / base_rate,
        0.0,
    )

    return grouped
