import pytest
import pandas as pd
import numpy as np
from src.model_eval import (
    get_friction_level,
    calculate_ev,
    decision_loss,
    build_profit_curve,
    find_best_threshold,
    build_roc_curve,
    build_lift_curve,
)

# --- Tests for get_friction_level ---

@pytest.mark.parametrize(
    "probability, amount, clv_score, expected_level_str",
    [
        # (VI) Các kịch bản kiểm thử cho từng cấp độ
        # (EN) Test scenarios for each friction level
        (0.10, 5_000_000, 50_000_000, "Cấp 0: Phê duyệt tự động"),
        (0.25, 5_000_000, 50_000_000, "Cấp 1: Gửi SMS/Notification"),
        (0.55, 5_000_000, 50_000_000, "Cấp 2: Sinh trắc học FaceID"),
        (0.85, 5_000_000, 50_000_000, "Cấp 3: Video Call/Tạm dừng 30p"),
        (0.96, 5_000_000, 50_000_000, "Cấp 4: Đóng băng tài khoản"),
        # (VI) Trường hợp biên: xác suất thấp nhưng số tiền lớn, bị đẩy lên Cấp 2
        # (EN) Edge case: low probability but high amount, pushed to Level 2
        (0.10, 10_000_001, 50_000_000, "Cấp 2: Sinh trắc học FaceID"),
    ]
)
def test_get_friction_level(probability, amount, clv_score, expected_level_str):
    """Tests that get_friction_level correctly maps inputs to the right friction level."""
    # WHEN: Call the function with simulated data
    # (VI) KHI: Gọi hàm với dữ liệu giả lập
    actual_level = get_friction_level(probability, amount, clv_score)

    # THEN: Verify the result is as expected
    # (VI) THÌ: Xác minh kết quả trả về đúng như kỳ vọng
    assert actual_level == expected_level_str


# --- Tests for Profit Curve and Thresholding ---

@pytest.fixture
def profit_curve_data():
    """A fixture to provide simple, predictable data for profit curve tests."""
    # (VI) Dữ liệu giả lập để kiểm tra đường cong lợi nhuận
    # (EN) Simulated data to test the profit curve
    data = {
        'prob':   [0.9, 0.8, 0.2, 0.1],
        'isFraud': [1,   0,   1,   0],
        'amount': [1000, 500, 2000, 300]
    }
    df = pd.DataFrame(data)
    # (VI) Giả sử chi phí cho một dự đoán sai (FP) là 10
    # (EN) Assume the cost of a false positive (FP) is 10
    cost_fp = 10
    return df, cost_fp


def test_build_profit_curve_calculation(profit_curve_data):
    """Tests that the profit curve calculation is mathematically correct."""
    df, cost_fp = profit_curve_data

    # WHEN: Build the profit curve
    # (VI) KHI: Xây dựng đường cong lợi nhuận
    profit_df = build_profit_curve(df, cost_fp=cost_fp)

    # THEN: Check the structure and baseline
    # (VI) THÌ: Kiểm tra cấu trúc và giá trị baseline
    assert 'profit_vs_approve_all' in profit_df.columns
    # (VI) Lợi nhuận tại ngưỡng cao nhất (không báo động gì) phải bằng 0
    # (EN) Profit at the highest threshold (alerting nothing) must be 0
    assert profit_df['profit_vs_approve_all'].iloc[0] == pytest.approx(0)

    # THEN: Verify a specific calculation point
    # (VI) THÌ: Xác minh một điểm tính toán cụ thể
    # (VI) Tại ngưỡng > 0.5, chúng ta bắt các giao dịch có prob=0.9 và 0.8
    # (EN) At threshold > 0.5, we catch transactions with prob=0.9 and 0.8
    # TP: amount=1000 (saved)
    # FP: cost=10 (incurred)
    # FN: amount=2000 (missed)
    # Total fraud amount = 1000 + 2000 = 3000
    # Loss at this threshold = missed_fraud (2000) + fp_cost (10) = 2010
    # Profit vs approve all = total_fraud_amount - loss = 3000 - 2010 = 990
    profit_at_0_5 = profit_df[profit_df['threshold'] == 0.8]['profit_vs_approve_all'].iloc[0]
    assert profit_at_0_5 == pytest.approx(990)


def test_find_best_threshold(profit_curve_data):
    """Tests that the function finds the threshold with the maximum profit."""
    df, cost_fp = profit_curve_data
    profit_df = build_profit_curve(df, cost_fp=cost_fp)

    # WHEN: Find the best threshold
    # (VI) KHI: Tìm ngưỡng tốt nhất
    best_point = find_best_threshold(profit_df)

    # THEN: Verify that the found profit is the maximum in the DataFrame
    # (VI) THÌ: Xác minh rằng lợi nhuận tìm được là lớn nhất trong DataFrame
    assert isinstance(best_point, pd.Series)
    assert best_point['loss'] == profit_df['loss'].min()


# --- Tests for Error Handling ---

def test_build_profit_curve_missing_columns_raises_error():
    """Tests that build_profit_curve raises an error if a column is missing."""
    # GIVEN: Data is missing the 'amount' column
    # (VI) CHO: Dữ liệu bị thiếu cột 'amount'
    df = pd.DataFrame({'prob': [0.9], 'isFraud': [1]})

    # WHEN/THEN: Calling the function should raise a ValueError
    # (VI) KHI/THÌ: Gọi hàm sẽ gây ra lỗi ValueError
    with pytest.raises(ValueError, match="Missing columns for profit curve"):
        build_profit_curve(df)


def test_find_best_threshold_empty_input_raises_error():
    """Tests that find_best_threshold raises an error for an empty DataFrame."""
    # GIVEN: An empty DataFrame
    # (VI) CHO: Một DataFrame rỗng
    empty_df = pd.DataFrame()

    # WHEN/THEN: Calling the function should raise a ValueError
    # (VI) KHI/THÌ: Gọi hàm sẽ gây ra lỗi ValueError
    with pytest.raises(ValueError, match="profit_curve is empty"):
        find_best_threshold(empty_df)


# --- Tests for other evaluation metrics ---

def test_calculate_ev_positive():
    """Tests that EV is positive when intervening is the correct decision."""
    # GIVEN: High probability of fraud, high amount
    # (VI) CHO: Xác suất gian lận cao, số tiền lớn
    ev = calculate_ev(prob_fraud=0.8, amount=10_000_000, clv_score=5_000_000)
    # THEN: Expected value should be positive
    # (VI) THÌ: Giá trị kỳ vọng phải là số dương
    assert ev > 0


def test_calculate_ev_negative():
    """Tests that EV is negative when approving is the correct decision."""
    # GIVEN: Low probability of fraud, low amount
    # (VI) CHO: Xác suất gian lận thấp, số tiền nhỏ
    ev = calculate_ev(prob_fraud=0.01, amount=100_000, clv_score=5_000_000)
    # THEN: Expected value should be negative
    # (VI) THÌ: Giá trị kỳ vọng phải là số âm
    assert ev < 0


def test_build_roc_curve():
    """Tests the ROC curve calculation and AUC score."""
    y_true = [0, 0, 1, 1]
    y_scores = [0.1, 0.4, 0.35, 0.8]

    # WHEN: Build the ROC curve
    roc_df = build_roc_curve(y_true, y_scores)

    # THEN: Check the AUC value
    assert 'auc' in roc_df.columns
    assert roc_df['auc'].iloc[0] == pytest.approx(0.75)


def test_decision_loss():
    """Tests the decision_loss calculation."""
    df = pd.DataFrame({
        'isFraud': [1, 0, 1, 0],
        'predicted_decision': [1, 1, 0, 0],
        'amount': [100000, 50000, 200000, 30000]
    })
    result = decision_loss(df, 'predicted_decision', cost_fp=50000)
    assert result['loss'] == 250000.0
    assert result['loss_fn'] == 200000.0
    assert result['loss_fp'] == 50000.0
    assert result['tp'] == 1
    assert result['fp'] == 1
    assert result['fn'] == 1
    assert result['tn'] == 1


def test_build_lift_curve():
    """Tests the build_lift_curve function."""
    df = pd.DataFrame({
        'prob': [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05],
        'isFraud': [1, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    })
    lift_df = build_lift_curve(df, n_bins=2)
    assert 'cumulative_lift' in lift_df.columns
    assert len(lift_df) == 2


def test_build_lift_curve_errors():
    with pytest.raises(ValueError, match="n_bins must be >= 2"):
        build_lift_curve(pd.DataFrame({'prob': [1], 'isFraud': [1]}), n_bins=1)

    with pytest.raises(ValueError, match="Missing columns for lift curve"):
        build_lift_curve(pd.DataFrame({'prob': [1]}), n_bins=2)