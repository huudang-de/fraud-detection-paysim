def calculate_ev(prob_fraud, amount, clv_score):
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