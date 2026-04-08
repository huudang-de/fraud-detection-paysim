import pandas as pd
import os

def load_csv_data_pandas(file_path, delimiter=','):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    try:
        df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8-sig')
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc CSV: {e}")

    return df
if __name__ == "__main__":
    try:
        df=load_csv_data_pandas("D:/Công việc/DA + DE/Book DA/Data Science for Business/PaySim/fraud-detection-paysim/data/raw/Synthetic_Financial_datasets_log.csv")
        print(df.head())
    except Exception as e:
        print("Lỗi:",e)