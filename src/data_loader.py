import pandas as pd
import numpy as np
import os

def load_paysim_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tim thấy file tại: {file_path}")

    print(f"--- Đang tải dữ liệu từ: {file_path} ---")

    df = pd.read_csv(file_path)

    start_mem = df.memory_usage().sum() /1024**2
    print(f"Bộ nhớ tiêu thụ ban đầu: {start_mem:.2f} MB")

    # Tối ưu hóa kiểu dữ liệu
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
    
    end_men = df.memory_usage().sum() / 1024**2
    print(f"Bộ nhớ tiêu thụ sau tối ưu: {end_men:.2f} MB")
    print(f"Tiết kiệm được: {100 *(start_mem - end_men)/ start_mem:.1f}")
    
    return df


def get_sample_data(df, fraud_df, non_fraud_df]):
    fraud_df = df[df['isFraud'] == 1] # Lấy toàn bộ dòng gian lận
    non_fraud_df = df[df['isFraud' ==0]] # Lấy toàn bộ dòng bình thường

    # Lấy mẫu ngẫu nhiên 24000 giao dịch bình thường
    



if __name__ == "__main":
    path = 'D:/Công việc/DA + DE/Book DA/Data Science for Business/PaySim/fraud-detection-paysim\data/raw/Synthetic_Financial_datasets_log.csv'
    try:
        data = load_paysim_data(path)
        print(data.head())
    except Exception as e:
        print(f"Lỗi: {e}")