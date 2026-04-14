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
    '''
    df = df.copy()

    #Tập trung vào TRANSFER,CASH_OUT
    df['is_transfer'] = (df['type'] == 'TRANSFER').astype(int)
    df['is_cashout'] = (df['type'] == 'CASH_OUT').astype(int)

    df['is_high_risk_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT'])

    #Giá trị giao dịch lớn
    df['log_amount'] = np.log1p(df['amount'])

    q95 = df['amount'].quantile(0.95)
    q90 = df['amount'].quantile(0.90)

    df['is_large_amount'] = (df['amount'] > q95).astype(int)
    df['large_transfer'] = (df['type'] == 'TRANSFER' & (df['amount'] > q90)).astype(int)


    #Hoạt động liên tục (không theo thời gian sinh học)
    df['hour'] = df['step'] % 24
    df['is_night'] = ((df['hour'] < 6) | (df['hour'] > 22)).astype(int)

    #Nhắm vào tài khoản nhận “rỗng” hoặc mới tạo
    df['is_dest_zero_balance'] = (df['oldbalanceDest'] == 0).astype(int)

    #Phá vỡ logic số dư để qua mặt hệ thống kiểm soát
    df['orig_error'] = (df['oldbalanceOrg'] - df['amount'] - df['newbalanceOrig'])
    df['dest_error'] = (df['oldbalanceDest'] + df['amount'] - df['newbalanceDest'])
    df['is_balance_error'] = ((df['orig_error'] != 0) | (df['dest_error'] != 0)).astype(int)
    
    #Tương tác high risk type + zero balance
    df['high_risk_combo'] = (df['is_high_risk_type'] == 1 & (df['is_dest_zero_balance'] == 1)).astype(int)

    #Xóa cột ID columns
    df = df.drop(columns=['nameOrig', 'nameDest'], errors='ignore')

    return 

def split_xy(df):
    X = df.drop(columns=['isFraud'])
    y = df['isFraud']
    return X,y
