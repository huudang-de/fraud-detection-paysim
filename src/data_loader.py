import pandas as pd
import numpy as np
import os

def load_paysim_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tim thấy file tại: {file_path}")

    print(f"--- Đang tải dữ liệu từ: {file_path} ---")

    df = pd.read_csv(file_path)

    # Tối ưu hóa kiểu dữ liệu
    start_mem = df.memory_usage().sum() / 1024**2
    print(f"Bộ nhớ tiêu thụ ban đầu: {start_mem:.2f} MB")
    
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int': # kiểm tra nếu là số nguyên 
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max: 
                    df[col] = df[col].astype(np.int8) # ép về int8
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16) # ép về int16
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)  # ép về int32
                pass

            else:
                df[col] = df[col].astype(np.float32) # ép cột số thực về float32
        
        else: 
            if col == 'type':
                df[col]=df[col].astype('category') # ép cột chuỗi(type) về category
    
    end_mem = df.memory_usage().sum() / 1024**2
    print(f"Bộ nhớ tiêu thụ sau tối ưu: {end_mem:.2f} MB")
    print(f"Tiết kiệm được: {100 * (start_mem - end_mem) / start_mem:.1f}%")

    return df


def get_sample_data(df):
    '''
    Hàm lấy mẫu từ TOÀN BỘ dữ liệu (Dùng cho EDA tổng quát)
    Tỷ lệ: Giữ nguyên toàn bộ Fraud và lấy mẫu Non-fraud tương ứng.
    '''
    fraud_df = df[df['isFraud'] == 1] # Lấy toàn bộ dòng gian lận
    non_fraud_df = df[df['isFraud'] ==0] # Lấy toàn bộ dòng bình thường

    # Lấy mẫu ngẫu nhiên 24639 giao dịch bình thường
    n_sample = min(len(non_fraud_df), 24639)
    non_fraud_sample  = non_fraud_df.sample(n=n_sample, random_state=42)
    
    # Gộp nhóm gian lận và nhóm bình thường đã lấy mẫu lại thành một DataFrame
    balanced_df = pd.concat([fraud_df, non_fraud_sample])
    
    # Xáo trộn dữ liệu để các dòng gian lận không nằm tập trung ở đầu
    balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"---Đã tạo tập dữ liệu mẫu EDA: {len(balanced_df)} dòng ---")
    return balanced_df

def get_sample_modeling(df):
    '''
    Backward-compatible wrapper for modeling scope selection.

    This function no longer samples by isFraud. Target-aware sampling before
    train/test split inflates offline metrics and can hide data leakage.
    '''
    focused_df = filter_modeling_scope(df)
    print(f"---Đã tạo tập dữ liệu Modeling scope: {len(focused_df)} dòng ---")
    return focused_df


def filter_modeling_scope(df, high_risk_only=True, customer_dest_only=True, time_col='step'):
    '''
    Keep only rows that are in the intended real-time scoring scope.

    Filters must use fields available at transaction time. Do not use isFraud
    or post-transaction balances here.
    '''
    mask = pd.Series(True, index=df.index)

    if high_risk_only:
        mask &= df['type'].isin(['TRANSFER', 'CASH_OUT'])

    if customer_dest_only:
        mask &= df['nameDest'].str.startswith('C')

    scoped_df = df.loc[mask].copy()

    if time_col in scoped_df.columns:
        scoped_df = scoped_df.sort_values(time_col)

    return scoped_df


def split_by_time(df, test_size=0.2, time_col='step'):
    '''
    Split train/test chronologically to avoid temporal leakage.
    '''
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    if time_col not in df.columns:
        raise ValueError(f"Missing time column: {time_col}")

    ordered_df = df.sort_values(time_col).copy()
    split_idx = int(len(ordered_df) * (1 - test_size))

    if split_idx <= 0 or split_idx >= len(ordered_df):
        raise ValueError("Not enough rows to create a non-empty train/test split")

    cutoff_value = ordered_df[time_col].iloc[split_idx]
    train_df = ordered_df[ordered_df[time_col] < cutoff_value].copy()
    test_df = ordered_df[ordered_df[time_col] >= cutoff_value].copy()

    if train_df.empty or test_df.empty:
        raise ValueError("Time split produced an empty train or test set")

    return train_df, test_df


def balance_training_data(df, target_col='isFraud', negative_multiplier=3, random_state=42):
    '''
    Downsample the majority class after splitting. Use only for training data.
    '''
    if target_col not in df.columns:
        raise ValueError(f"Missing target column: {target_col}")
    if negative_multiplier < 1:
        raise ValueError("negative_multiplier must be >= 1")
    
    fraud_df = df[df[target_col] == 1]
    non_fraud_df = df[df[target_col] == 0]

    if fraud_df.empty or non_fraud_df.empty:
        return df.copy()

    n_sample = min(len(non_fraud_df), len(fraud_df) * negative_multiplier)
    non_fraud_sample = non_fraud_df.sample(n=n_sample, random_state=random_state)

    balanced_df = pd.concat([fraud_df, non_fraud_sample], axis=0)
    balanced_df = balanced_df.sample(frac=1, random_state=random_state)

    return balanced_df

if __name__ == "__main__":
    path = r'D:/Công việc/DA + DE/Book DA/Data Science for Business/PaySim/fraud-detection-paysim\data/raw/Synthetic_Financial_datasets_log.csv'
    
    try:
        # load và tối ưu
        data = load_paysim_data(path) # load và tối ư
        
        # Lấy mẫu cho EDA
        balanced_data = get_sample_data(data) # lấy mẫu cân bằng
        print("\5 dòng đầu của dữ liệu đã cân bằng:")
        print(balanced_data.head())

        print("\n Tỷ lệ các lớp trong tập mẫu:") # kiểm tra tỷ lệ gian lận
        print(balanced_data['isFraud'].value_counts(normalize=True))

        # Lọc phạm vi modeling T0-safe
        balanced_data = get_sample_modeling(data)

        print("\n5 dòng đầu của dữ liệu đã lọc phạm vi modeling:")
        print(balanced_data.head())

        print("\nTỷ lệ các lớp trong tập mẫu:")
        print(balanced_data['isFraud'].value_counts(normalize=True))

        print("\nCác loại giao dịch còn lại trong tập mẫu:")
        print(balanced_data['type'].unique())
    except Exception as e:
        print(f"Lỗi: {e}")
