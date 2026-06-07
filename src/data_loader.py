import pandas as pd
import numpy as np
import os

def load_paysim_data(file_path):
    """
    Load and memory-optimize the PaySim dataset from a CSV file.

    This function reads data from a specified CSV file path and automatically reduces 
    its memory footprint by downcasting data types. Integer columns are cast to the 
    smallest possible integer types (int8, int16, int32), floating-point numbers are 
    cast to `float32`, and the string column named 'type' is cast to a `category` type.

    Parameters
    ----------
    file_path : str
        The absolute or relative path to the CSV file to be loaded.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the data with optimized memory types.

    Raises
    ------
    FileNotFoundError
        If the file at the specified `file_path` does not exist.

    Examples
    --------
    >>> import pandas as pd
    >>> path = 'data/raw/Synthetic_Financial_datasets_log.csv'
    >>> df = load_paysim_data(path)
    --- Đang tải dữ liệu từ: data/raw/Synthetic_Financial_datasets_log.csv ---
    Bộ nhớ tiêu thụ ban đầu: 2834.50 MB
    Bộ nhớ tiêu thụ sau tối ưu: 600.20 MB
    Tiết kiệm được: 78.8%
    """
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
    """
    Sample the dataset for general Exploratory Data Analysis (EDA).

    This function addresses the severe class imbalance of the PaySim dataset by keeping 
    all fraudulent transactions (isFraud=1) and randomly downsampling the non-fraudulent
    transactions (isFraud=0) to a maxium of 24,639 records. The resulting subsets are 
    concatenated and shuffled to ceate a smaller, more balanced dataset suitable for 
    visualization and preliminary analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        The original PaySim DataFrame (must contain the 'isFraud' column).

    Returns
    -------
    pandas.DataFrame
        A sampled, more balanced, and randomly shuffled DataFrame.
    
    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming `data` is the loaded original massive DataFrame
    >>> sampled_df = get_sample_data(data)
    --- Đã tạo tập dữ liệu mẫu EDA: ... dòng ---
    """
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
    """
    Backward-compatible wrapper for selecting the modeling scope dataset.

    This function delegates to `filter_codeling_scope` to ratain ony the transactions
    that fall within the intended real-time scoring scope (e.g., TRANSFER, CASH_OUT).
    Importantly, it no longer performs target-aware sampling (by `isFraud`) prior to 
    the train/test split. Target-aware sampling at thí stage inflates offline metrics
    and can obscure data leakage.

    Parameters
    ----------
    df : pandas.DataFrame
        The original Paysim DataFrame.
    
    Retruns
    -------
    pandas.DataFrame
        A filtered DataFrame containing only the transactions relevant for modeling.
    
    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming `data` is the original DataFrame
    >>> modeling_df = get_sample_modeling(data)
    --- Đã tạo tập dữ liệu Modeling scope: ... dòng ---
    """
    focused_df = filter_modeling_scope(df)
    print(f"---Đã tạo tập dữ liệu Modeling scope: {len(focused_df)} dòng ---")
    return focused_df


def filter_modeling_scope(df, high_risk_only=True, customer_dest_only=True, time_col='step'):
    """
    Filter data to keep only rows thả are within the internded real-time scoring scope.

    This function simulates a real-word deployment scenatio by removing transactions
    that carry on fraud risk of fall outside the business scope. Filters must exclusively
    use fields available at the exact moment of the transaction (do not use the `isFraud`
    target variable or post-transaction balances). The output data is sorted chronologically.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the dataset to be filtered.
    high_risk_only : bool, optional
        If True, retains only transaction types known to have fraud risk (e.g.,
        'TRANSFER' and 'CASH_OUT'). Default is True.
    customer_dest_only : bool, optional
        If True, retains only transactions directed towards customer accounts
        (names strating with 'C'). Default is True.
    time_col : str, optional
        The name of the time column used to sort the data chronologically. Default is 'step'
    
    Returns
    -------
    pandas.DataFrame
        A filtered DataFrame, sorted chronologically by the time column.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming `df` contains various transaction types
    >>> scoped_df = filter_modeling_scope(df)
    >>> print(croped_df['type'].unique())
    ['TRANSFER', 'CASH_OUT']
    """
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
    """
    Split the dataset into train and test sets chronologically to prevent temporal leakage.

    This function sorts the data sequentially using the specified time column,
    determines a cutoff point based on the `test_size` ratio, and splits the data.
    Transactions occurring before the cutoff form the training set, while transactions
    occurring at or after the cutoff form the test set. This approach is critical for
    time-series and financial data to ensure the model does not "peek" into the future.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be split.
    test_size : float, optional
        The proportion of the dataset (between 0 and 1) to include in the test split.
        This will be the most recent data chronologically. Default is 0.2 (20%).
    time_col : str, optional
        The name of the column representing time for sorting. Default is 'step'.
    
    Returns
    -------
    tuple of pandas.DataFrame
        A tuple containing two DataFrames: (train_df, test_df).
    
    Raises
    ------
    ValueError
        If `test_size` is not between 0 and 1, if `time_col` is missing, or if
        the resulting train or test split is empty.
        
    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming `df` is already scoped data
    >>> train_df, test_df = split_by_time(df, test_size=0.2)
    >>> print(f"Train: {len(train_df)} rows, Test: {len(test_df)} rows")
    """
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
    """
    Downsample the majority class to balance the dataset. USE ONLY FOR TRAINING DATA.

    This function addresses class imbalance by retaining all minority class instances
    (fraud) and randomly sampling the majority class (non-fraud) based on a specified
    multiplier. Warning: This must only be applied to the Training set *after* splitting
    (e.g., using split_by_time). Do not apply this to the Test set, as testing must 
    reflect the natural distribution of the real world.

    Parameters
    ----------
    df : pandas.DataFrame
        The Training DataFrame to be balanced.
    target_col : str, optional
        The name of the target/label column. Defrault id 'isFraud'.
    negative_multiplier : int or float, optional
        The ratio of negative (non-fraud) instances to positive (fraud) instances
        to retain. For example, a multiplier of 3 means there will be 3 non-fraud rows
        for every 1 fraud row. Default is 3.
    random_state : int, optional
        Seed for reproducible random sampling. Default is 42.
    
    Returns
    -------
    pandas.DataFrame
        A class-balanced and randomly shuffled DataFrame.
    
    Raises
    ------
    ValueError
        If the `target_col` is not found in the DataFrame or if `negative_multiplier`
        is strictly less than 1.
    
    Examples
    --------
    >>> import pandas as pd
    >>> # train_df is obtained from split_by_time
    >>> balanced_train_df = balance_training_data(train_df, negative_multiplier=3)
    >>> print(balanced_train_df['isFraud'].value_counts())
    """
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
