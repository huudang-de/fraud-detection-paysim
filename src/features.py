import pandas as pd
import numpy as np

def build_fratures(df):
    '''
    Xây dựng các tính năng cho mô hình phát hiện gian lận
    Dựa trên phân tích dữ liệu khám phá (EDA):
    -Tập trung vào TRANSFER,CASH_OUT
    -Giá trị giao dịch lớn
    -Hoạt động liên tục (không theo thời gian sinh học)
    -Nhắm vào tài khoản nhận “rỗng” hoặc mới tạo
    -Phá vỡ logic số dư để qua mặt hệ thống kiểm soát
    -Không bị phát hiện bởi rule-based system 
    --> Xét T0 
    '''
    df = df.copy()

    #Tập trung vào TRANSFER,CASH_OUT
    df['is_high_risk_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)

    #Giá trị giao dịch lớn
    df['log_amount'] = np.log1p(df['amount'])

    #Hoạt động liên tục (không theo thời gian sinh học) --> Fraud cao vào đêm khuya
    df['hour'] = df['step'] % 24
    df['is_night'] = ((df['hour'] < 6) | (df['hour'] > 22)).astype(int)

    #Nhắm vào tài khoản nhận “rỗng” hoặc mới tạo
    df['is_dest_zero_balance'] = (df['oldbalanceDest'] == 0).astype(int)
    
    #Tương tác high risk type + zero balance
    df['high_risk_combo'] = df['is_high_risk_type'] * df['is_dest_zero_balance'] * df['is_night']

    #Xóa cột không dùng hay là thông tin quá khứ
    df = df.drop(columns=['nameOrig', 'nameDest','type','newbalanceOrig', 'newbalanceDest', # Gây leakage
        'isFlaggedFraud','oldbalanceOrg', 'step'], errors='ignore')

    return df

def split_xy(df):
    X = df.drop(columns=['isFraud'])
    y = df['isFraud']
    return X,y

