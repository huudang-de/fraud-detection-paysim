# 📊 Fraud Detection System: Tối ưu hóa Giá trị kỳ vọng (EV) trong Thanh toán số

## 📝 Giới thiệu dự án
Dự án này tập trung vào việc xây dựng hệ thống phát hiện gian lận dựa trên dữ liệu mô phỏng **PaySim**. Khác với các mô hình Machine Learning thuần túy chỉ tối ưu hóa độ chính xác kỹ thuật (Accuracy), hệ thống này được thiết kế để giải quyết bài toán kinh tế cốt lõi trong ngành Ngân hàng: **Cân bằng giữa An toàn bảo mật và Trải nghiệm người dùng (Frictionless CX).**

## 🎯 Mục tiêu chiến lược
1. **Tối ưu hóa Giá trị kỳ vọng (Expected Value - EV):** Áp dụng lý thuyết của *Provost & Fawcett (2013)* để xây dựng ma trận chi phí bất đối xứng, tích hợp **Giá trị vòng đời khách hàng (CLV)** vào ngưỡng ra quyết định.
2. **Tuân thủ Pháp lý (Compliance):** Tích hợp logic kiểm soát theo **Quyết định 2345/QĐ-NHNN** của Ngân hàng Nhà nước Việt Nam về xác thực sinh trắc học đối với giao dịch trên 10 triệu VNĐ.
3. **Giảm thiểu Ma sát (Friction Reduction):** Phân bổ linh hoạt các điểm ma sát (OTP, FaceID, Call xác thực) dựa trên xác suất rủi ro thay vì chặn giao dịch một cách máy móc.

## 🛠️ Kỹ thuật Đặc trưng (Feature Engineering)
Dự án tập trung vào việc phái sinh các biến số có ý nghĩa kinh tế cao từ tập dữ liệu PaySim:
* **Account Depletion Ratio:** Tỷ lệ số tiền giao dịch trên số dư tài khoản (nhận diện hành vi vét cạn tiền).
* **Temporal Features:** Phân tích chu kỳ giao dịch theo giờ trong ngày để phát hiện các truy cập bất thường vào khung giờ nhạy cảm.
* **Error Balance Logic:** Kiểm tra tính cân đối kế toán giữa tài khoản nguồn và tài khoản đích để phát hiện lỗi hệ thống hoặc can thiệp dữ liệu trái phép.

## 🚀 Cấu trúc dự án
```text
├── data/           # Raw & Processed data (PaySim)
├── notebooks/      # EDA & Model Experiments
├── src/            # Production code (Feature Eng, Scoring)
├── models/         # Saved models (Random Forest, XGBoost)
└── reports/        # Analysis & Visualizations
```

## 📚 Tài liệu tham khảo
* Gupta, S., & Lehmann, D. R. (2003). Customers as assets. *Journal of Interactive Marketing*.
* Quyết định 2345/QĐ-NHNN về an toàn, bảo mật trong thanh toán trực tuyến.