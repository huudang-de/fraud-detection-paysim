import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve


def calculate_ev(prob_fraud, amount, clv_score):
    """
    Calculate expected value for fraud intervention decision.

    Computes whether inntervening on a transaction has positive expected value using the formula:
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
        Expected value of intervention. Posiitve = intervene,
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

    Maps fraud probalitity and transaction amount to intervention level
    using Decision 2345 strategy. Creates 5 friction levels from auto-approval
    to acciunt freeze.

    Parameters
    ----------
    prob : float
        Fraud probability from model (0 to 1).
    amount : float
        Transaction amoint in VND.
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
    '''
    Cost-only evaluation matrix.

    False negative: missed fraud amount is lost.
    False positive: customer friction/operations cost is paid.
    True positive is not counted again as a positive benefit, avoiding double
    counting with the false-negative loss baseline.
    '''
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
    '''
    Sort transactions by score descending and evaluate every score threshold.

    The returned profit is relative to approving everything, where all fraud
    amounts are lost and no false-positive cost is paid.
    '''
    required_cols = {score_col, target_col, amount_col}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns for profit curve: {sorted(missing_cols)}")

    ordered = df[[score_col, target_col, amount_col]].sort_values(score_col, ascending=False).copy()
    ordered['_is_fraud'] = ordered[target_col] == 1
    ordered['_fraud_amount'] = np.where(ordered['_is_fraud'], ordered[amount_col], 0.0)
    ordered['_is_legit'] = ~ordered['_is_fraud']

    total_fraud_amount = float(ordered['_fraud_amount'].sum())

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

    grouped['alerted'] = grouped['transactions'].cumsum()
    grouped['tp'] = grouped['frauds'].cumsum().astype(int)
    grouped['fp'] = grouped['legit'].cumsum().astype(int)
    grouped['caught_fraud_amount'] = grouped['caught_fraud_amount'].cumsum()
    grouped['missed_fraud_amount'] = total_fraud_amount - grouped['caught_fraud_amount']
    grouped['loss_fp'] = grouped['fp'] * cost_fp
    grouped['loss'] = grouped['missed_fraud_amount'] + grouped['loss_fp']
    grouped['profit_vs_approve_all'] = total_fraud_amount - grouped['loss']
    grouped['alert_rate'] = grouped['alerted'] / len(ordered)

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

    return pd.concat([no_alert, grouped], ignore_index=True)


def find_best_threshold(profit_curve):
    '''
    Select the threshold with minimum realized loss.
    '''
    if profit_curve.empty:
        raise ValueError("profit_curve is empty")

    best_idx = profit_curve['loss'].idxmin()
    return profit_curve.loc[best_idx].copy()


def build_roc_curve(y_true, y_score):
    '''
    Build a ROC curve for monitoring rank separation independent of threshold.
    '''
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    return pd.DataFrame({
        'fpr': fpr,
        'tpr': tpr,
        'threshold': thresholds,
        'auc': roc_auc,
    })


def build_lift_curve(df, score_col='prob', target_col='isFraud', n_bins=10):
    '''
    Build a cumulative lift curve by score decile.

    Lift > 1 means the selected top-scored segment contains fraud at a higher
    rate than the full population.
    '''
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
